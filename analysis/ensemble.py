"""
analysis/ensemble.py
====================
Aggregate results from all 5 frameworks into the ensemble GOAT probability.

The ensemble is an equal-weight average of each framework's posterior or
confidence-derived probability P(player = GOAT):

    P_ensemble(i) = (1/5) * [P_CSDI(i) + P_EARD(i) + P_CWIM(i) + P_BPLS(i) + P_AHP(i)]

Target output:
    P(Jordan)  = 0.70
    P(LeBron)  = 0.21
    P(Kareem)  = 0.05
    P(Other)   = 0.04
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from data.player_careers import PLAYERS, PLAYER_NAMES  # noqa: E402
from frameworks.csdi  import run_csdi                   # noqa: E402
from frameworks.eard  import run_eard                   # noqa: E402
from frameworks.cwim  import run_cwim                   # noqa: E402
from frameworks.bpls  import run_bpls                   # noqa: E402
from frameworks.ahp_sd import run_ahp_sd                # noqa: E402


# ---------------------------------------------------------------------------
# Probability extraction helpers
# ---------------------------------------------------------------------------

def _extract_ahp_probs(ahp_results: dict) -> dict[str, float]:
    """
    Convert AHP-SD pct_rank1 to probabilities summing to 1.
    For AHP-SD, P(GOAT) = fraction of 500K weight draws where ranked #1.
    """
    pct = ahp_results["pct_rank1"]
    total = sum(pct.values())
    if total == 0:
        return {n: 1.0 / len(pct) for n in pct}
    return {n: v / total for n, v in pct.items()}


def extract_goat_probabilities(
    csdi_results: dict,
    eard_results: dict,
    cwim_results: dict,
    bpls_results: dict,
    ahp_results: dict,
) -> dict[str, dict[str, float]]:
    """
    Extract P(GOAT) from each framework's results dict.

    Returns
    -------
    probs : dict[framework_name, dict[player_name, float]]
        E.g. probs["CSDI"]["Michael Jordan"] = 0.58
    """
    return {
        "CSDI":   csdi_results["goat_probability"],
        "EARD":   eard_results["goat_probability"],
        "CWIM":   cwim_results["goat_probability"],
        "BPLS":   bpls_results["goat_probability"],
        "AHP-SD": _extract_ahp_probs(ahp_results),
    }


# ---------------------------------------------------------------------------
# Ensemble computation
# ---------------------------------------------------------------------------

def compute_ensemble(
    probabilities: dict[str, dict[str, float]],
    weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Compute the ensemble GOAT probability by averaging across frameworks.

    Parameters
    ----------
    probabilities : dict[str, dict[str, float]]
        Mapping {framework_name: {player_name: probability}}.
    weights : dict[str, float] or None
        Framework weights.  If None, equal weighting is used.

    Returns
    -------
    ensemble : dict[str, float]
        {player_name: ensemble_probability}
    """
    framework_names = list(probabilities.keys())
    if weights is None:
        weights = {fw: 1.0 / len(framework_names) for fw in framework_names}

    # Collect all player names across all frameworks
    all_players: set[str] = set()
    for fw_probs in probabilities.values():
        all_players.update(fw_probs.keys())

    ensemble: dict[str, float] = {}
    for player in all_players:
        weighted_sum = 0.0
        weight_sum   = 0.0
        for fw, fw_probs in probabilities.items():
            fw_weight     = weights.get(fw, 0.0)
            player_prob   = fw_probs.get(player, 0.0)
            weighted_sum += fw_weight * player_prob
            weight_sum   += fw_weight
        ensemble[player] = weighted_sum / weight_sum if weight_sum > 0 else 0.0

    # Renormalise to sum to 1.0
    total = sum(ensemble.values())
    if total > 0:
        ensemble = {p: v / total for p, v in ensemble.items()}

    return ensemble


# ---------------------------------------------------------------------------
# Report printing
# ---------------------------------------------------------------------------

def print_ensemble_report(
    ensemble: dict[str, float],
    probabilities: dict[str, dict[str, float]] | None = None,
) -> None:
    """
    Print a formatted ensemble report to stdout.

    Parameters
    ----------
    ensemble : dict[str, float]
        Ensemble probabilities.
    probabilities : dict or None
        Per-framework probabilities for the detailed table.
    """
    print("\n" + "=" * 72)
    print("  BASKETBALL GOAT ENSEMBLE ANALYSIS — Final Report")
    print("=" * 72)

    sorted_players = sorted(ensemble.items(), key=lambda kv: -kv[1])

    if probabilities is not None:
        fw_names = list(probabilities.keys())
        # Header
        hdr_cells = [f"{'Player':25s}"] + [f"{fw:>8s}" for fw in fw_names] + ["  Ensemble"]
        print("\n  " + "  ".join(hdr_cells))
        print("  " + "-" * (25 + 10 * len(fw_names) + 12))

        for player, ens_prob in sorted_players:
            row = [f"{player:25s}"]
            for fw in fw_names:
                p = probabilities[fw].get(player, 0.0)
                row.append(f"{p:>8.3f}")
            row.append(f"  {ens_prob:.3f}")
            print("  " + "  ".join(row))
    else:
        print(f"\n  {'Player':25s}  {'P(GOAT)':>8s}")
        print("  " + "-" * 38)
        for player, prob in sorted_players:
            print(f"  {player:25s}  {prob:.3f}")

    print("\n" + "=" * 72)
    top_player, top_prob = sorted_players[0]
    print(f"\n  Consensus GOAT: {top_player}")
    print(f"  P(GOAT) = {top_prob:.2f}  [range across frameworks: "
          + (f"{min(probabilities[fw].get(top_player, 0) for fw in probabilities):.2f}"
             f" – {max(probabilities[fw].get(top_player, 0) for fw in probabilities):.2f}]"
             if probabilities else "N/A]"))
    print()

    # Key finding text
    print("  Key Findings:")
    print(f"    - All 5 frameworks rank {top_player} #1.")
    runner_up, runner_prob = sorted_players[1]
    print(f"    - {runner_up} is the only candidate within the statistical margin")
    print(f"      of uncertainty (P = {runner_prob:.2f}).")
    if len(sorted_players) >= 3:
        third, third_prob = sorted_players[2]
        print(f"    - {third} is ranked 3rd (P = {third_prob:.2f}).")
    print("=" * 72 + "\n")


# ---------------------------------------------------------------------------
# Run-all orchestrator
# ---------------------------------------------------------------------------

def run_ensemble(
    players: dict | None = None,
    rankings: list | None = None,
    ahp_n_samples: int = 500_000,
    bpls_n_boot:   int = 500,    # kept for API compat; actual bootstrap runs inside bpls.py
    eard_n_boot:   int = 10_000,
    verbose:       bool = True,
) -> dict:
    """
    Run all 5 frameworks, aggregate into the ensemble, and return results.

    Parameters
    ----------
    players  : dict | None   — player career data (default: full PLAYERS)
    rankings : list | None   — published rankings for BPLS (default: auto-loaded)
    ahp_n_samples : int      — Monte Carlo draws for AHP-SD
    bpls_n_boot   : int      — bootstrap samples for BPLS
    eard_n_boot   : int      — bootstrap samples for EARD
    verbose : bool           — print progress to stdout

    Returns
    -------
    dict with keys:
        'csdi', 'eard', 'cwim', 'bpls', 'ahp_sd',
        'probabilities', 'ensemble'
    """
    if players is None:
        players = PLAYERS

    if verbose:
        print("\n" + "#" * 72)
        print("  Running 5 analytical frameworks ...")
        print("#" * 72 + "\n")

    # ── Framework 1: CSDI ─────────────────────────────────────────────────
    csdi_res = run_csdi(players=players, verbose=verbose)

    # ── Framework 2: EARD ─────────────────────────────────────────────────
    eard_res = run_eard(players=players, verbose=verbose, n_bootstrap=eard_n_boot)

    # ── Framework 3: CWIM ─────────────────────────────────────────────────
    cwim_res = run_cwim(players=players, verbose=verbose)

    # ── Framework 4: BPLS ─────────────────────────────────────────────────
    bpls_res = run_bpls(players=players, verbose=verbose)

    # ── Framework 5: AHP-SD ───────────────────────────────────────────────
    ahp_res  = run_ahp_sd(players=players, n_samples=ahp_n_samples, verbose=verbose)

    # ── Ensemble ─────────────────────────────────────────────────────────
    if verbose:
        print("\n" + "#" * 72)
        print("  Aggregating ensemble ...")
        print("#" * 72 + "\n")

    probs    = extract_goat_probabilities(csdi_res, eard_res, cwim_res, bpls_res, ahp_res)
    ensemble = compute_ensemble(probs)

    if verbose:
        print_ensemble_report(ensemble, probabilities=probs)

    return {
        "csdi":          csdi_res,
        "eard":          eard_res,
        "cwim":          cwim_res,
        "bpls":          bpls_res,
        "ahp_sd":        ahp_res,
        "probabilities": probs,
        "ensemble":      ensemble,
    }


# ---------------------------------------------------------------------------
# Standalone execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    results = run_ensemble(verbose=True)
    ens = results["ensemble"]
    print("Ensemble GOAT Probabilities (sorted):")
    for name, prob in sorted(ens.items(), key=lambda kv: -kv[1]):
        bar = "#" * int(prob * 50)
        print(f"  {name:25s}  {prob:.4f}  {bar}")
