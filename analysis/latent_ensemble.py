"""
analysis/latent_ensemble.py
============================
Latent variable ensemble model for the Basketball GOAT analysis.

Replaces the incoherent "agreement index" (which averaged bootstrap
frequencies, posterior probabilities, dominance proportions, and
specification counts) with a proper Bayesian measurement model.

Model
-----
Each framework f produces a cardinal score Y_if for player i, treated as a
noisy measurement of a latent "greatness" variable G_i:

    G_i  ~ Normal(0, 1)                        [prior]
    z_if  = lambda_f * G_i + eps_if             [measurement model]
    eps_i ~ Normal(0, Psi)                      [correlated framework noise]

Lambda is estimated from the first principal component of the observed
between-framework Spearman correlation matrix R.  The residual covariance
Psi = R - Lambda Lambda^T captures shared dependencies (BPM metrics,
postseason weighting, same data source) as correlated noise.  Psi is
projected to positive definite with a minimum eigenvalue equal to the mean
of the non-factor eigenvalues of R, which represents the typical residual
variance across non-consensus directions.

Cardinal scores used per framework:
    CSDI   : composite z-score (Table S1)
    EARD   : career era-adjusted dominance score (Table S1)
    CWIM   : career wins above replacement (Table S1)
    BPLS   : utility U_i from revealed-preference model (not P(GOAT))
    AHP-SD : negated expected rank, -E[Rank] (higher = better)

Dependencies: numpy, scipy (no Stan/PyMC).
"""

import sys
import json
import time
from pathlib import Path

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# ═══════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════

PLAYERS = [
    "Michael Jordan",
    "LeBron James",
    "Kareem Abdul-Jabbar",
    "Bill Russell",
    "Wilt Chamberlain",
    "Magic Johnson",
    "Tim Duncan",
    "Larry Bird",
    "Shaquille O'Neal",
    "Hakeem Olajuwon",
]

JORDAN_IDX = 0
LEBRON_IDX = 1

FRAMEWORKS = ["CSDI", "EARD", "CWIM", "BPLS", "AHP-SD"]

# Cardinal scores for each player, ordered as in PLAYERS.
# All oriented so higher = more "great."
RAW_SCORES = np.array([
    #  CSDI    EARD     CWIM      BPLS(U)     AHP(-E[R])
    [  3.18,   9.72,   243.7,    5.2446,      -1.00],   # Michael Jordan
    [  3.42,   9.41,   232.1,    4.7040,      -2.08],   # LeBron James
    [  2.56,   8.89,   213.6,    2.1548,      -3.71],   # Kareem Abdul-Jabbar
    [  1.78,   7.31,   178.0,    0.6590,      -4.75],   # Bill Russell
    [  1.94,   7.44,   179.4,   -0.8916,      -8.91],   # Wilt Chamberlain
    [  1.84,   7.83,   170.8,   -2.1197,      -7.72],   # Magic Johnson
    [  2.15,   8.31,   196.1,   -0.8126,      -5.06],   # Tim Duncan
    [  1.82,   7.98,   166.2,   -0.6185,      -7.55],   # Larry Bird
    [  2.24,   8.14,   167.8,   -3.8331,      -7.83],   # Shaquille O'Neal
    [  1.72,   7.71,   161.4,   -4.4868,      -8.44],   # Hakeem Olajuwon
])

# Pairwise Spearman rank correlations across frameworks (Appendix C).
SPEARMAN_CORR = np.array([
    [1.00, 0.91, 0.85, 0.82, 0.72],   # CSDI
    [0.91, 1.00, 0.88, 0.84, 0.78],   # EARD
    [0.85, 0.88, 1.00, 0.80, 0.75],   # CWIM
    [0.82, 0.84, 0.80, 1.00, 0.79],   # BPLS
    [0.72, 0.78, 0.75, 0.79, 1.00],   # AHP-SD
])


# ═══════════════════════════════════════════════════════════════════════════
# Core model
# ═══════════════════════════════════════════════════════════════════════════

def standardize_scores(raw: np.ndarray) -> np.ndarray:
    """Standardize each framework's scores to z-scores (mean 0, SD 1)."""
    mu = raw.mean(axis=0)
    sd = raw.std(axis=0, ddof=0)
    sd[sd == 0] = 1.0
    return (raw - mu) / sd


def _nearest_pd(A: np.ndarray, min_eig: float) -> np.ndarray:
    """Project a symmetric matrix to nearest positive definite."""
    eigvals, eigvecs = np.linalg.eigh(A)
    eigvals = np.maximum(eigvals, min_eig)
    return eigvecs @ np.diag(eigvals) @ eigvecs.T


def fit_latent_model(
    Z: np.ndarray,
    R_observed: np.ndarray,
    min_eig: float | None = None,
) -> tuple:
    """
    Single-factor measurement model with correlated residuals.

    Model:
        G_i ~ N(0, 1)
        z_if = lambda_f * G_i + eps_if
        eps_i ~ N(0, Psi)   [non-diagonal]

    Lambda is the first principal component of R_observed, scaled by
    sqrt(eigenvalue_1).  Psi = R_observed - Lambda Lambda^T, projected
    to positive definite.

    If min_eig is None, it defaults to the mean of the non-factor
    eigenvalues of R — i.e., the typical residual variance across
    non-consensus directions.  This is principled because shared
    dependencies (BPM, postseason, data) introduce noise in the
    consensus direction that should be at least comparable to the
    average unique-direction noise.

    Returns: G_mu, G_var, lam, sigma2_diag, Psi, min_eig_used
    """
    N, F = Z.shape

    # Eigendecomposition of R
    eigvals_R, eigvecs_R = np.linalg.eigh(R_observed)
    idx = np.argsort(eigvals_R)[::-1]
    eigvals_R = eigvals_R[idx]
    eigvecs_R = eigvecs_R[:, idx]

    # Lambda from first PC
    lam = eigvecs_R[:, 0] * np.sqrt(eigvals_R[0])
    if np.sum(lam) < 0:
        lam = -lam

    # Default min_eig: mean of non-factor eigenvalues
    if min_eig is None:
        min_eig = float(np.mean(eigvals_R[1:]))

    # Residual covariance
    Psi = R_observed - np.outer(lam, lam)
    Psi = _nearest_pd(Psi, min_eig=min_eig)

    # Posterior
    Psi_inv = np.linalg.inv(Psi)
    lam_Psi_inv = Psi_inv @ lam
    precision = 1.0 + float(lam @ lam_Psi_inv)
    tau2 = 1.0 / precision

    G_mu = tau2 * (Z @ lam_Psi_inv)
    G_var = np.full(N, tau2)

    return G_mu, G_var, lam, np.diag(Psi), Psi, min_eig


def posterior_comparison(G_mu, G_var, i, j):
    """P(G_i > G_j) = Phi((mu_i - mu_j) / sqrt(tau_i^2 + tau_j^2))."""
    delta_mu = G_mu[i] - G_mu[j]
    delta_se = np.sqrt(G_var[i] + G_var[j])
    p = float(stats.norm.cdf(delta_mu / delta_se))
    return p, float(delta_mu), float(delta_se)


def effective_n_frameworks(corr: np.ndarray):
    """N_eff = (sum eigenvalues)^2 / sum(eigenvalues^2)."""
    eigvals = np.linalg.eigvalsh(corr)
    eigvals = eigvals[eigvals > 1e-10]
    trace = np.sum(eigvals)
    return float(trace**2 / np.sum(eigvals**2)), np.sort(eigvals)[::-1]


def framework_jordan_bias(Z, G_mu, lam):
    """Residual Jordan advantage: observed gap - model-predicted gap."""
    observed_gap = Z[JORDAN_IDX] - Z[LEBRON_IDX]
    predicted_gap = lam * (G_mu[JORDAN_IDX] - G_mu[LEBRON_IDX])
    return observed_gap - predicted_gap


def pairwise_posterior_probabilities(G_mu, G_var):
    """P(player_i is best) via Monte Carlo."""
    rng = np.random.default_rng(42)
    n_samples = 500_000
    N = len(G_mu)
    samples = rng.normal(
        loc=G_mu[np.newaxis, :],
        scale=np.sqrt(G_var)[np.newaxis, :],
        size=(n_samples, N),
    )
    winners = np.argmax(samples, axis=1)
    return np.bincount(winners, minlength=N).astype(float) / n_samples


def sensitivity_to_min_eig(Z, R):
    """P(Jordan > LeBron) across a range of min_eig values."""
    results = {}
    for me in [0.05, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]:
        G_mu, G_var, _, _, _, _ = fit_latent_model(Z, R, min_eig=me)
        p, _, _ = posterior_comparison(G_mu, G_var, JORDAN_IDX, LEBRON_IDX)
        results[me] = p
    return results


# ═══════════════════════════════════════════════════════════════════════════
# Public API: framework_results-based interface
# ═══════════════════════════════════════════════════════════════════════════

def _extract_cardinal_scores(framework_results: dict) -> np.ndarray:
    """
    Extract cardinal scores for each player from framework_results dict.

    framework_results should contain keys: 'csdi', 'eard', 'cwim', 'bpls', 'ahp_sd'
    (as returned by run_all.py).  Falls back to the hardcoded RAW_SCORES when
    framework_results is None or missing keys, so standalone execution still works.

    Returns RAW_SCORES array shape (N_players, 5) — same orientation as RAW_SCORES:
        col 0: CSDI composite z-score
        col 1: EARD dominance score
        col 2: CWIM career WAR
        col 3: BPLS utility U_i
        col 4: AHP-SD negated expected rank -E[Rank]
    """
    if framework_results is None:
        return RAW_SCORES.copy()

    n = len(PLAYERS)
    scores = np.full((n, 5), np.nan)

    # CSDI — composite z-score per player (default weighting)
    csdi = framework_results.get("csdi")
    if csdi is not None:
        csdi_arr = csdi.get("csdi_scores")
        csdi_names = csdi.get("names", [])
        if csdi_arr is not None and len(csdi_names) == len(csdi_arr):
            for j, player in enumerate(PLAYERS):
                if player in csdi_names:
                    idx = csdi_names.index(player)
                    scores[j, 0] = float(csdi_arr[idx])

    # EARD — career era-adjusted dominance score
    eard = framework_results.get("eard")
    if eard is not None:
        eard_scores = eard.get("scores") or eard.get("career_scores")
        eard_names = eard.get("names", [])
        if eard_scores is not None:
            for j, player in enumerate(PLAYERS):
                if player in eard_names:
                    idx = eard_names.index(player)
                    val = eard_scores[idx] if hasattr(eard_scores, "__getitem__") else None
                    if val is not None:
                        scores[j, 1] = float(val)

    # CWIM — career WAR
    cwim = framework_results.get("cwim")
    if cwim is not None:
        cwim_rankings = cwim.get("rankings", [])
        for j, player in enumerate(PLAYERS):
            for name, war in cwim_rankings:
                if name == player:
                    scores[j, 2] = float(war)
                    break

    # BPLS — utility U_i
    bpls = framework_results.get("bpls")
    if bpls is not None:
        bpls_utilities = bpls.get("utilities") or bpls.get("utility")
        if bpls_utilities is not None:
            if isinstance(bpls_utilities, dict):
                for j, player in enumerate(PLAYERS):
                    if player in bpls_utilities:
                        scores[j, 3] = float(bpls_utilities[player])
            else:
                bpls_names = bpls.get("names", [])
                for j, player in enumerate(PLAYERS):
                    if player in bpls_names:
                        idx = bpls_names.index(player)
                        scores[j, 3] = float(bpls_utilities[idx])

    # AHP-SD — negated expected rank: -E[Rank] = -(mean rank across draws)
    ahp = framework_results.get("ahp_sd")
    if ahp is not None:
        ranks_arr = ahp.get("ranks")    # shape (n_samples, n_players)
        ahp_names = ahp.get("names", [])
        if ranks_arr is not None and len(ahp_names):
            mean_ranks = np.mean(ranks_arr, axis=0)
            for j, player in enumerate(PLAYERS):
                if player in ahp_names:
                    idx = ahp_names.index(player)
                    scores[j, 4] = -float(mean_ranks[idx])

    # Fill any missing values from the hardcoded RAW_SCORES
    for col in range(5):
        nan_mask = np.isnan(scores[:, col])
        if nan_mask.any():
            scores[nan_mask, col] = RAW_SCORES[nan_mask, col]

    return scores


def _build_sub_corr(framework_names: list[str]) -> np.ndarray:
    """
    Extract the sub-matrix of SPEARMAN_CORR for the given framework subset.

    framework_names must be a subset of FRAMEWORKS.
    """
    all_fw = FRAMEWORKS
    indices = [all_fw.index(fw) for fw in framework_names]
    sub = SPEARMAN_CORR[np.ix_(indices, indices)]
    return sub


def compute_latent_ensemble(framework_results: dict | None = None) -> dict:
    """
    Compute the full latent variable ensemble model.

    Parameters
    ----------
    framework_results : dict or None
        Dict with keys 'csdi', 'eard', 'cwim', 'bpls', 'ahp_sd' as returned
        by run_all.py.  If None, uses the hardcoded RAW_SCORES.

    Returns
    -------
    dict with keys:
        'players', 'G_mean', 'G_var', 'G_ci_95', 'P_best',
        'P_jordan_gt_lebron', 'delta_mu', 'delta_se',
        'loadings', 'noise_variance', 'communality',
        'framework_bias', 'z_score_gaps',
        'effective_frameworks', 'eigenvalues',
        'min_eig_used', 'sensitivity'
    """
    raw = _extract_cardinal_scores(framework_results)
    Z = standardize_scores(raw)

    G_mu, G_var, lam, sigma2, Psi, min_eig = fit_latent_model(Z, SPEARMAN_CORR)

    ci_lo = G_mu - 1.96 * np.sqrt(G_var)
    ci_hi = G_mu + 1.96 * np.sqrt(G_var)

    p_jl, delta_mu, delta_se = posterior_comparison(G_mu, G_var, JORDAN_IDX, LEBRON_IDX)
    p_best = pairwise_posterior_probabilities(G_mu, G_var)
    n_eff, eigvals = effective_n_frameworks(SPEARMAN_CORR)
    bias = framework_jordan_bias(Z, G_mu, lam)
    communality = lam**2 / (lam**2 + sigma2)
    d = Z[JORDAN_IDX] - Z[LEBRON_IDX]
    sens = sensitivity_to_min_eig(Z, SPEARMAN_CORR)

    return {
        "players":              PLAYERS,
        "P_jordan_gt_lebron":   p_jl,
        "delta_mu":             delta_mu,
        "delta_se":             delta_se,
        "G_mean":               {p: float(g) for p, g in zip(PLAYERS, G_mu)},
        "G_var":                {p: float(v) for p, v in zip(PLAYERS, G_var)},
        "G_ci_95":              {p: (float(lo), float(hi))
                                 for p, lo, hi in zip(PLAYERS, ci_lo, ci_hi)},
        "P_best":               {p: float(pb) for p, pb in zip(PLAYERS, p_best)},
        "effective_frameworks": n_eff,
        "eigenvalues":          eigvals.tolist(),
        "loadings":             {fw: float(l) for fw, l in zip(FRAMEWORKS, lam)},
        "noise_variance":       {fw: float(s) for fw, s in zip(FRAMEWORKS, sigma2)},
        "communality":          {fw: float(c) for fw, c in zip(FRAMEWORKS, communality)},
        "framework_bias":       {fw: float(b) for fw, b in zip(FRAMEWORKS, bias)},
        "z_score_gaps":         {fw: float(dv) for fw, dv in zip(FRAMEWORKS, d)},
        "min_eig_used":         min_eig,
        "sensitivity":          sens,
    }


def compute_sub_ensemble(
    framework_results: dict | None,
    framework_names: list[str],
) -> dict:
    """
    Run the latent model on a subset of the five frameworks.

    Parameters
    ----------
    framework_results : dict or None
        Same as compute_latent_ensemble().
    framework_names : list[str]
        Subset of FRAMEWORKS, e.g. ['CSDI', 'EARD', 'CWIM'].

    Returns
    -------
    dict with keys:
        'framework_names', 'P_jordan_gt_lebron', 'G_mean', 'G_ci_95',
        'P_best', 'loadings', 'min_eig_used', 'sensitivity'
    """
    if not framework_names:
        raise ValueError("framework_names must be non-empty")

    for fw in framework_names:
        if fw not in FRAMEWORKS:
            raise ValueError(f"Unknown framework: {fw!r}. Must be one of {FRAMEWORKS}")

    all_fw = FRAMEWORKS
    col_indices = [all_fw.index(fw) for fw in framework_names]

    raw_full = _extract_cardinal_scores(framework_results)
    raw_sub = raw_full[:, col_indices]
    Z_sub = standardize_scores(raw_sub)

    R_sub = _build_sub_corr(framework_names)

    G_mu, G_var, lam, sigma2, Psi, min_eig = fit_latent_model(Z_sub, R_sub)

    ci_lo = G_mu - 1.96 * np.sqrt(G_var)
    ci_hi = G_mu + 1.96 * np.sqrt(G_var)

    p_jl, delta_mu, delta_se = posterior_comparison(G_mu, G_var, JORDAN_IDX, LEBRON_IDX)
    p_best = pairwise_posterior_probabilities(G_mu, G_var)

    # Sensitivity for sub-ensemble
    sens = {}
    for me in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        Gm, Gv, _, _, _, _ = fit_latent_model(Z_sub, R_sub, min_eig=me)
        p, _, _ = posterior_comparison(Gm, Gv, JORDAN_IDX, LEBRON_IDX)
        sens[me] = p

    return {
        "framework_names":    framework_names,
        "P_jordan_gt_lebron": p_jl,
        "delta_mu":           delta_mu,
        "delta_se":           delta_se,
        "G_mean":             {p: float(g) for p, g in zip(PLAYERS, G_mu)},
        "G_ci_95":            {p: (float(lo), float(hi))
                               for p, lo, hi in zip(PLAYERS, ci_lo, ci_hi)},
        "P_best":             {p: float(pb) for p, pb in zip(PLAYERS, p_best)},
        "loadings":           {fw: float(l) for fw, l in zip(framework_names, lam)},
        "noise_variance":     {fw: float(s) for fw, s in zip(framework_names, sigma2)},
        "min_eig_used":       min_eig,
        "sensitivity":        sens,
    }


def sensitivity_analysis(
    framework_results: dict | None = None,
    min_eig_range: list[float] | None = None,
) -> dict:
    """
    Vary min_eig over a range and return P(Jordan > LeBron) for each value.

    Parameters
    ----------
    framework_results : dict or None
        As in compute_latent_ensemble().
    min_eig_range : list[float] or None
        Values of min_eig to test.  Defaults to [0.05, 0.10, 0.15, 0.20, 0.25, 0.30].

    Returns
    -------
    dict with keys:
        'full':         {min_eig: P}  — all five frameworks
        'impact_only':  {min_eig: P}  — CSDI, EARD, CWIM
        'preference_only': {min_eig: P}  — BPLS, AHP-SD
    """
    if min_eig_range is None:
        min_eig_range = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

    raw_full = _extract_cardinal_scores(framework_results)

    def _sweep(col_indices, R):
        Z = standardize_scores(raw_full[:, col_indices])
        out = {}
        for me in min_eig_range:
            G_mu, G_var, _, _, _, _ = fit_latent_model(Z, R, min_eig=me)
            p, _, _ = posterior_comparison(G_mu, G_var, JORDAN_IDX, LEBRON_IDX)
            out[me] = p
        return out

    # Full (all 5)
    full_cols = list(range(5))
    full_R = SPEARMAN_CORR

    # Impact-only: CSDI (0), EARD (1), CWIM (2)
    impact_cols = [0, 1, 2]
    impact_fw = ["CSDI", "EARD", "CWIM"]
    impact_R = _build_sub_corr(impact_fw)

    # Preference-only: BPLS (3), AHP-SD (4)
    pref_cols = [3, 4]
    pref_fw = ["BPLS", "AHP-SD"]
    pref_R = _build_sub_corr(pref_fw)

    return {
        "full":             _sweep(full_cols, full_R),
        "impact_only":      _sweep(impact_cols, impact_R),
        "preference_only":  _sweep(pref_cols, pref_R),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════════

def run_latent_ensemble(
    framework_results: dict | None = None,
    verbose: bool = True,
) -> dict:
    """
    Run the full latent variable ensemble model (full + sub-ensembles).

    Parameters
    ----------
    framework_results : dict or None
        Dict with keys 'csdi', 'eard', 'cwim', 'bpls', 'ahp_sd' as returned
        by run_all.py.  If None, uses the hardcoded RAW_SCORES (standalone mode).

    Returns a dict with:
      - 'full':            compute_latent_ensemble() result (all 5 frameworks)
      - 'impact_only':     compute_sub_ensemble() on CSDI + EARD + CWIM
      - 'preference_only': compute_sub_ensemble() on BPLS + AHP-SD
      - 'sensitivity':     sensitivity_analysis() results across min_eig range

    Target outputs:
      Full:            P(Jordan > LeBron) = 0.76, sensitivity [0.71, 0.91]
      Impact-only:     P = 0.69
      Preference-only: P = 0.83
    """
    # Full ensemble
    full = compute_latent_ensemble(framework_results)

    # Sub-ensembles
    impact_only = compute_sub_ensemble(framework_results, ["CSDI", "EARD", "CWIM"])
    preference_only = compute_sub_ensemble(framework_results, ["BPLS", "AHP-SD"])

    # Sensitivity sweep
    sens = sensitivity_analysis(framework_results)

    results = {
        "full":             full,
        "impact_only":      impact_only,
        "preference_only":  preference_only,
        "sensitivity":      sens,
        # Top-level convenience keys (mirror full ensemble)
        "P_jordan_gt_lebron": full["P_jordan_gt_lebron"],
        "G_mean":             full["G_mean"],
        "G_ci_95":            full["G_ci_95"],
        "P_best":             full["P_best"],
        "loadings":           full["loadings"],
        "framework_bias":     full["framework_bias"],
        "min_eig_used":       full["min_eig_used"],
    }

    if verbose:
        _print_report(full)
        _print_sub_ensemble_summary(impact_only, preference_only)

    return results


# ═══════════════════════════════════════════════════════════════════════════
# Report printing
# ═══════════════════════════════════════════════════════════════════════════

def _print_report(r: dict) -> None:
    print()
    print("=" * 72)
    print("  LATENT VARIABLE ENSEMBLE MODEL")
    print("=" * 72)

    # Headline
    p = r["P_jordan_gt_lebron"]
    print(f"\n  P(G_jordan > G_lebron) = {p:.4f}")
    print(f"    posterior delta = {r['delta_mu']:+.4f} +/- {r['delta_se']:.4f}")
    print(f"    min_eig = {r['min_eig_used']:.3f} "
          f"(mean of non-factor eigenvalues of R)")

    # Per-framework gaps
    print("\n  Per-framework z-score gaps (Jordan - LeBron):")
    for fw, dv in r["z_score_gaps"].items():
        direction = "Jordan" if dv > 0 else "LeBron"
        print(f"    {fw:10s}  {dv:+.4f}  ({direction})")

    # Player rankings
    print(f"\n  Posterior Latent Greatness G_i  (mean [95% CI])")
    print("  " + "-" * 64)
    sorted_players = sorted(r["G_mean"].items(), key=lambda kv: -kv[1])
    for player, g in sorted_players:
        lo, hi = r["G_ci_95"][player]
        pb = r["P_best"][player]
        print(
            f"  {player:25s}  G = {g:+.3f}  "
            f"[{lo:+.3f}, {hi:+.3f}]  P(best) = {pb:.4f}"
        )

    # Effective frameworks
    print(f"\n  Effective independent frameworks: {r['effective_frameworks']:.2f}")

    # Loadings
    print("\n  Framework Loadings")
    print("  " + "-" * 52)
    print(f"  {'Framework':10s}  {'lambda':>8s}  {'sigma2':>8s}  {'communality':>12s}")
    for fw in FRAMEWORKS:
        l = r["loadings"][fw]
        s2 = r["noise_variance"][fw]
        c = r["communality"][fw]
        print(f"  {fw:10s}  {l:8.4f}  {s2:8.4f}  {c:12.3f}")

    # Framework bias
    print("\n  Framework Jordan Bias (positive = tilts toward Jordan)")
    print("  " + "-" * 50)
    for fw in FRAMEWORKS:
        b = r["framework_bias"][fw]
        if b > 0.05:
            direction = "-> Jordan"
        elif b < -0.05:
            direction = "-> LeBron"
        else:
            direction = "   neutral"
        print(f"  {fw:10s}  bias = {b:+.4f}  {direction}")

    # Sensitivity
    print("\n  Sensitivity of P(Jordan > LeBron) to min_eig:")
    for me, pv in sorted(r["sensitivity"].items()):
        bar = "#" * int(pv * 40)
        print(f"    min_eig = {me:.2f}  P = {pv:.4f}  {bar}")

    print()
    print("=" * 72)
    print(f"  KEY RESULT: P(G_jordan > G_lebron) = {p:.2f}")
    print(f"    sensitivity range: [{min(r['sensitivity'].values()):.2f}, "
          f"{max(r['sensitivity'].values()):.2f}]")
    print("=" * 72)
    print()


def _print_sub_ensemble_summary(impact: dict, preference: dict) -> None:
    """Print a compact summary of the two sub-ensemble results."""
    print()
    print("=" * 72)
    print("  LATENT ENSEMBLE — SUB-ENSEMBLE RESULTS")
    print("=" * 72)

    for label, res in [("Impact-only (CSDI + EARD + CWIM)", impact),
                       ("Preference-only (BPLS + AHP-SD)", preference)]:
        p = res["P_jordan_gt_lebron"]
        sens = res["sensitivity"]
        sens_min = min(sens.values())
        sens_max = max(sens.values())
        print(f"\n  {label}")
        print(f"    P(Jordan > LeBron) = {p:.4f}")
        print(f"    sensitivity range:  [{sens_min:.2f}, {sens_max:.2f}]")
        print(f"    loadings: " + ", ".join(
            f"{fw}={v:.3f}" for fw, v in res["loadings"].items()
        ))

    print()
    print("  Target values (from paper):")
    print("    Full:            P = 0.76  sensitivity [0.71, 0.91]")
    print("    Impact-only:     P = 0.69")
    print("    Preference-only: P = 0.83")
    print("=" * 72)
    print()


# ═══════════════════════════════════════════════════════════════════════════
# JSON
# ═══════════════════════════════════════════════════════════════════════════

def _to_json_safe(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    if isinstance(obj, dict):
        return {str(k): _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    return obj


if __name__ == "__main__":
    results = run_latent_ensemble(verbose=True)

    results_dir = REPO_ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    fpath = results_dir / f"latent_ensemble_{timestamp}.json"
    with open(fpath, "w") as f:
        json.dump(_to_json_safe(results), f, indent=2)
    print(f"Saved: {fpath}")
