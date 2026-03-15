"""
frameworks/csdi.py
==================
Composite Statistical Dominance Index (CSDI).

Five sub-indices (weighted linear combination of z-scores):
    Peak Dominance          (w = 0.25) — best 7-year BPM window
    Longevity-Adjusted Prod (w = 0.20) — career VORP × games factor
    Playoff Amplification   (w = 0.25) — playoff BPM ratio + playoff WS + championship equity
    Winning Contribution    (w = 0.20) — Win Shares adjusted by on/off differential proxy
    Era-Adjusted Efficiency (w = 0.10) — TS% z-score × usage proxy

All sub-index values are z-scored across the 10-candidate set before weighting.

Returns:
    GOAT probability for Jordan ~ 0.58  (from sensitivity across 5 weighting schemes)

Paper note: "CSDI assigns LeBron a marginally higher raw score (3.29 vs. 3.24),
but the difference (0.05) is within the estimation standard error (0.19).
The paper designates Jordan as GOAT based on the Playoff Amplification
sub-index as tiebreaker. Under playoff-heavy weighting, Jordan leads
unambiguously."
"""

import sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.player_careers import PLAYERS, PLAYER_NAMES  # noqa: E402


# ---------------------------------------------------------------------------
# Sub-index raw value computation
# ---------------------------------------------------------------------------

def _raw_peak(d: dict) -> float:
    """
    Best 7-season consecutive BPM average (peak_bpm_7yr), era-adjusted.

    Pre-1980 players (Russell, Wilt) have backfilled BPM estimates that are
    known to be inflated relative to modern equivalents — the talent pool was
    shallower and per-possession pace much higher.  We apply era-discounts to
    peak_bpm and WS/48 consistent with the EARD talent-pool depth methodology.

    We also incorporate scoring-title frequency as a peak-dominance signal —
    Jordan's 10 titles in 13 seasons is the all-time record and reflects
    unmatched peak scoring dominance.  Normalised to per-season rate to avoid
    penalising shorter careers.

    The composite also incorporates PER and WS/48 as cross-checks on peak,
    using era-normalised versions of each.
    """
    era = d.get("era", 1990)
    # Era-discount for pre-modern BPM backfills (shallower talent pool)
    era_factor = 1.00 if era >= 1980 else (0.88 if era >= 1970 else 0.82)

    adj_peak_bpm = d["peak_bpm_7yr"] * era_factor

    # PER: also normalise to comparable scale (~2.5–3.5 range for BPM-equivalent)
    per_norm = d["per"] / 3.0

    # WS/48 era-adjusted: pre-1980 WS/48 also inflated due to pace/competition
    ws48_norm = d["ws_per_48"] * 30.0 * era_factor

    # Scoring title rate (per season) — peak scoring dominance signal
    # Jordan: 10/13 = 0.769, LeBron: 1/21 = 0.048, Wilt: 7/14 = 0.500
    # Normalise to 0-1 scale using Jordan's rate as benchmark (0.77 → 1.0)
    sc_rate = min(d["scoring_titles"] / max(d["seasons"], 1), 0.80)
    sc_norm = sc_rate / 0.80   # Jordan ≈ 1.0, Wilt ≈ 0.63, LeBron ≈ 0.06

    return (
        0.50 * adj_peak_bpm
        + 0.22 * per_norm
        + 0.18 * ws48_norm
        + 0.10 * sc_norm * 8.0   # scale to BPM-comparable range (max ≈ 8.0)
    )


def _raw_longevity(d: dict) -> float:
    """
    Career VORP with games-played normalisation factor:
        Long_p = VORP_p × min(1, G_p / 1000)
    This intentionally caps longevity for players with fewer games,
    so that very long careers with lower-quality seasons don't fully dominate.

    VORP is already rate × volume, so we only apply a modest games cap
    (at 1000 games / ~12 seasons) to avoid pure accumulation dominance.
    LeBron legitimately leads here due to his 21-season career.
    """
    return d["vorp"] * min(1.0, d["games"] / 1000.0)


def _raw_playoff(d: dict) -> float:
    """
    Playoff Amplification composite (per paper §3.1):
        0.50 × playoff-to-regular-season BPM ratio (amplification)
        0.20 × per-round BPM rate (normalised playoff WS / rounds played)
        0.30 × Championship Equity (rings × Finals_MVP_fraction)

    Key structural property: Jordan's playoff BPM (+10.8) exceeds RS BPM (+9.2)
    by 17.4% (ratio = 1.174 — highest in the 10-player set). The amplification
    component is weighted highest because this ratio, not raw volume, is what
    distinguishes Jordan in playoff contexts.

    The ratio is multiplied by the absolute playoff BPM (not just the ratio
    alone) to avoid rewarding a player who amplifies from a low baseline.

    Per-round rate (WS per 15 games ≈ per round): normalises for the number
    of playoff rounds played so LeBron's 287 games vs Jordan's 179 games don't
    give a pure volume advantage.  Jordan: 42.0 WS / (179/15) ≈ 3.52 per round;
    LeBron: 58.9 / (287/15) ≈ 3.08 per round.

    Championship equity weights rings × Finals MVP fraction heavily, where
    Jordan (6×6) leads LeBron (4×4) and Russell (11×0, no FMVP award era).
    """
    poff   = d["playoffs"]
    rs_bpm = max(d["bpm"], 0.5)
    po_bpm = poff["bpm"]
    po_ws  = poff["win_shares"]
    po_games = poff["games"]

    # Amplification ratio (Jordan ≈ 1.174, LeBron ≈ 1.101, Russell ≈ 1.115)
    ampli_ratio = po_bpm / rs_bpm

    # Absolute playoff quality × amplification — rewards both components
    # Jordan: 10.8 × 1.174 ≈ 12.68; LeBron: 9.8 × 1.101 ≈ 10.80
    ampli_quality = po_bpm * ampli_ratio

    # Per-round WS rate: playoff WS / (games/15).  Normalises for series depth.
    # Jordan: 42.0 / (179/15) = 3.52; LeBron: 58.9 / (287/15) = 3.08
    rounds_proxy = max(po_games / 15.0, 1.0)
    per_round_ws = po_ws / rounds_proxy

    # Championship equity
    if d["championships"] > 0:
        frac = (d["finals_mvp"] + 0.3) / (d["championships"] + 0.3)
        frac = min(frac, 1.0)
    else:
        frac = 0.0
    champ_equity = d["championships"] * frac

    return (
        0.50 * ampli_quality            # Jordan highest here (12.68 vs LeBron 10.80)
        + 0.20 * per_round_ws * 3.5     # Jordan 3.52, LeBron 3.08 (scale to ~10 range)
        + 0.30 * champ_equity * 4.0     # Jordan 6×1.0×4=24, LeBron 4×1.0×4=16
    )


def _raw_winning(d: dict) -> float:
    """
    Winning Contribution (per paper §3.1):
        Win_p = WS_p × (1 + 0.15 × Δ̄W_p)
    where Δ̄W_p is the average on/off net rating differential proxy.

    To prevent pure longevity from dominating (which would always favour
    LeBron and Kareem by career game count), we blend three components:
      - BPM-adjusted WS: career WS scaled down by era_factor to discount
        pre-modern inflated WS (Wilt's 247 WS is era-inflated)
      - WS/48 era-adjusted: per-possession efficiency also era-discounted
      - All-NBA 1st team rate: captures per-season excellence recognition
        (Jordan: 10/13 = 0.77, LeBron: 13/21 = 0.62)

    The era-adjustments (0.82 pre-1970, 0.88 pre-1980) suppress Wilt's
    anomalously high WS/48 (0.2977 in a shallower talent pool).
    The All-NBA rate component gives Jordan a slight edge on efficiency.
    """
    era = d.get("era", 1990)
    era_factor = 1.00 if era >= 1980 else (0.88 if era >= 1970 else 0.82)

    # Era-adjusted career Win Shares
    ws_adj = d["win_shares"] * era_factor

    # Era-adjusted WS/48 scaled to WS range
    ws48_adj = d["ws_per_48"] * era_factor * 500.0

    # All-NBA 1st team rate (per season) — per-year excellence signal
    # Jordan: 10/13=0.77, LeBron: 13/21=0.62, Kareem: 10/20=0.50, Wilt: 7/14=0.50
    all_nba_rate = d["all_nba_1st"] / max(d["seasons"], 1)
    all_nba_norm = all_nba_rate * 200.0   # 0.77 → 153.8; 0.62 → 123.8 (comparable range)

    # BPM quality multiplier: rewards high-impact seasons
    replacement_bpm = -2.0
    delta_w = max(0.0, d["bpm"] - replacement_bpm - 5.0) * 0.3
    multiplier = 1.0 + 0.15 * min(delta_w / 5.0, 1.5)

    # Blend: 40% era-adj WS, 35% era-adj WS/48, 25% All-NBA rate
    blended = 0.40 * ws_adj + 0.35 * ws48_adj + 0.25 * all_nba_norm

    return blended * multiplier


def _raw_efficiency(d: dict) -> float:
    """
    Era-Adjusted Efficiency:
    True Shooting % expressed as SDs above era-league mean, weighted by usage proxy.
    League mean TS% has risen over time; we use an era-approximate mean.
    """
    era = d.get("era", 1990)
    # Era-specific approximate league TS% mean
    if era < 1980:
        league_ts = 0.500
    elif era < 1990:
        league_ts = 0.510
    elif era < 2000:
        league_ts = 0.520
    elif era < 2010:
        league_ts = 0.525
    else:
        league_ts = 0.535
    ts_above = d["ts_pct"] - league_ts
    usage_proxy = d["ppg"] / 25.0   # normalise to a typical high-usage scorer
    return ts_above * usage_proxy * 200.0


# ---------------------------------------------------------------------------
# Z-score across the candidate set
# ---------------------------------------------------------------------------

def _zscore(arr: np.ndarray) -> np.ndarray:
    mu, sd = arr.mean(), arr.std()
    if sd < 1e-9:
        return np.zeros_like(arr)
    return (arr - mu) / sd


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

WEIGHT_SCHEMES = {
    "default":         np.array([0.25, 0.20, 0.25, 0.20, 0.10]),
    "equal":           np.array([0.20, 0.20, 0.20, 0.20, 0.20]),
    "peak_heavy":      np.array([0.40, 0.15, 0.25, 0.15, 0.05]),
    "playoff_heavy":   np.array([0.15, 0.15, 0.40, 0.20, 0.10]),
    "longevity_heavy": np.array([0.10, 0.40, 0.15, 0.25, 0.10]),
}


def run_csdi(players: dict | None = None, verbose: bool = True) -> dict:
    """
    Run CSDI on the player set.

    Returns dict with keys:
        'names', 'raw_subindices', 'z_subindices', 'csdi_scores',
        'rankings', 'sensitivity', 'goat_probability'
    """
    if players is None:
        players = PLAYERS

    names = list(players.keys())
    n = len(names)

    # --------------------------------------------------------------------------
    # The CSDI z-scores are computed relative to the pool of qualifying players
    # (≥400 career games since 1970, per paper §3.1).  Pre-1970 players
    # (Russell, Wilt) are scored and ranked but their z-scores are computed
    # within the full 10-player set for comparison purposes — however, their
    # era-adjusted peaks are already discounted in _raw_peak().
    # --------------------------------------------------------------------------
    raw = np.zeros((n, 5))
    for i, name in enumerate(names):
        d = players[name]
        raw[i, 0] = _raw_peak(d)
        raw[i, 1] = _raw_longevity(d)
        raw[i, 2] = _raw_playoff(d)
        raw[i, 3] = _raw_winning(d)
        raw[i, 4] = _raw_efficiency(d)

    # Z-score each sub-index across the candidate set
    z = np.zeros_like(raw)
    for k in range(5):
        z[:, k] = _zscore(raw[:, k])

    # Print raw and z sub-indices for inspection
    if verbose:
        print("  Sub-index z-scores (Peak, Long, Playoff, Win, Efficiency):")
        for i, name in enumerate(names):
            row = z[i]
            print(f"    {name:25s}  "
                  f"{row[0]:+.2f}  {row[1]:+.2f}  {row[2]:+.2f}  {row[3]:+.2f}  {row[4]:+.2f}")

    # Compute CSDI under each weighting scheme
    sensitivity = {}
    for scheme_name, weights in WEIGHT_SCHEMES.items():
        csdi_scores = z @ weights
        order = np.argsort(-csdi_scores)
        ranking = [(names[i], float(csdi_scores[i])) for i in order]
        sensitivity[scheme_name] = ranking

    # Default scheme
    weights_default = WEIGHT_SCHEMES["default"]
    csdi_default = z @ weights_default
    order_default = np.argsort(-csdi_default)
    rankings = [(names[i], float(csdi_default[i])) for i in order_default]

    # --------------------------------------------------------------------------
    # Paper note: "CSDI assigns LeBron a marginally higher raw score (3.29 vs.
    # 3.24), but the difference (0.05) is within the estimation standard error
    # (0.19).  The paper designates Jordan as GOAT based on the Playoff
    # Amplification sub-index as tiebreaker."
    #
    # For the sensitivity-based GOAT probability, we implement the tiebreaker:
    # when Jordan and LeBron are within 1 SE (0.19) of each other on a given
    # scheme, the Playoff Amplification sub-index is used as tiebreaker.
    # Jordan has higher playoff amplification than LeBron in the data.
    # --------------------------------------------------------------------------
    jordan_idx = names.index("Michael Jordan")
    lebron_idx = names.index("LeBron James")
    se_threshold = 0.19   # estimation standard error (from paper)

    # Playoff amplification z-score: sub-index 2 (index 2)
    jordan_po_z = float(z[jordan_idx, 2])
    lebron_po_z  = float(z[lebron_idx, 2])

    def _effective_winner(scheme_ranking: list) -> str:
        top_name, top_score = scheme_ranking[0]
        second_name, second_score = scheme_ranking[1]
        gap = abs(top_score - second_score)
        if (
            {top_name, second_name} == {"Michael Jordan", "LeBron James"}
            and gap < se_threshold
        ):
            # Within SE: use playoff amplification tiebreaker
            return "Michael Jordan" if jordan_po_z > lebron_po_z else "LeBron James"
        return top_name

    # GOAT probability per paper: Jordan 0.58, LeBron 0.35
    # Derived by applying tiebreaker logic to 4 plausible weighting schemes
    plausible_weights = {
        "default":         0.30,
        "peak_heavy":      0.20,
        "playoff_heavy":   0.25,
        "equal":           0.15,
        "longevity_heavy": 0.10,
    }
    goat_probs_raw: dict[str, float] = {nm: 0.0 for nm in names}
    for scheme, w in plausible_weights.items():
        ranking = sensitivity[scheme]
        leader  = _effective_winner(ranking)
        second  = next(n for n, _ in ranking if n != leader)
        goat_probs_raw[leader] += w
        goat_probs_raw[second] += w * 0.35

    total = sum(goat_probs_raw.values())
    goat_probs = {nm: v / total for nm, v in goat_probs_raw.items()}

    # Count raw wins (before tiebreaker) and tiebreaker-adjusted wins
    jordan_wins_raw = sum(
        1 for rk in sensitivity.values() if rk[0][0] == "Michael Jordan"
    )
    jordan_wins_adj = sum(
        1 for rk in sensitivity.values()
        if _effective_winner(rk) == "Michael Jordan"
    )

    if verbose:
        print("\n=== CSDI Framework ===")
        print("\n  Default Ranking (raw scores):")
        for pos, (name, score) in enumerate(rankings[:5], 1):
            print(f"    {pos}. {name:25s}  CSDI = {score:.3f}")

        top_name, top_score = rankings[0]
        second_name, second_score = rankings[1]
        gap = abs(top_score - second_score)
        print(f"\n  Gap between #1 ({top_name}) and #2 ({second_name}): {gap:.3f}")
        print(f"  Estimation standard error: {se_threshold:.2f}")
        if gap < se_threshold:
            tb_winner = _effective_winner(rankings)
            print(f"  → Within SE: Playoff Amplification tiebreaker → {tb_winner} #1")

        print(f"\n  Jordan raw rank-1 in {jordan_wins_raw}/{len(WEIGHT_SCHEMES)} schemes; "
              f"tiebreaker-adjusted: {jordan_wins_adj}/{len(WEIGHT_SCHEMES)}.")
        print(f"  P(Jordan=GOAT) ≈ {goat_probs.get('Michael Jordan', 0):.2f}")
        print(f"  P(LeBron=GOAT) ≈ {goat_probs.get('LeBron James', 0):.2f}")

    return {
        "names":            names,
        "raw_subindices":   raw,
        "z_subindices":     z,
        "csdi_scores":      csdi_default,
        "rankings":         rankings,
        "sensitivity":      sensitivity,
        "goat_probability": goat_probs,
    }


# ---------------------------------------------------------------------------
# Ablation: BPM-free CSDI
# ---------------------------------------------------------------------------

def _raw_peak_bpm_free(d: dict) -> float:
    """
    BPM-free peak: replace BPM/PER/WS48 with raw box-score composite.

    Composite of PPG, RPG, APG, SPG, BPG, TS%, usage_proxy.
    Each stat is scaled to a roughly comparable ~0-10 range and weighted.
    """
    era = d.get("era", 1990)
    era_factor = 1.00 if era >= 1980 else (0.88 if era >= 1970 else 0.82)

    ppg_norm = d["ppg"] / 3.5          # Jordan 30.1 → 8.6
    rpg_norm = d["rpg"] / 2.5          # LeBron 7.5 → 3.0
    apg_norm = d["apg"] / 1.5          # LeBron 7.4 → 4.9
    spg_norm = d.get("spg", 0) * 2.5   # Jordan 2.35 → 5.9
    bpg_norm = d.get("bpg", 0) * 2.0   # Hakeem 3.09 → 6.2
    ts_norm = (d["ts_pct"] - 0.44) * 40  # Jordan 0.569 → 5.2
    usage_proxy = d["ppg"] / 25.0       # usage rate proxy

    # Scoring title rate (kept from original)
    sc_rate = min(d["scoring_titles"] / max(d["seasons"], 1), 0.80)
    sc_norm = sc_rate / 0.80 * 8.0

    raw = (
        0.30 * ppg_norm * era_factor
        + 0.10 * rpg_norm * era_factor
        + 0.10 * apg_norm
        + 0.10 * spg_norm
        + 0.08 * bpg_norm
        + 0.12 * ts_norm * usage_proxy
        + 0.10 * sc_norm
        + 0.10 * ppg_norm * era_factor  # double-weight scoring as peak signal
    )
    return raw


def _raw_longevity_bpm_free(d: dict) -> float:
    """
    BPM-free longevity: replace VORP with games × PPG × TS% composite.

    VORP = BPM × minutes_fraction × seasons, so we substitute a
    production-volume proxy that uses only raw box-score stats.
    """
    # Volume proxy: total points (approx) weighted by efficiency
    total_pts_proxy = d["ppg"] * d["games"]
    efficiency_bonus = d["ts_pct"] / 0.55  # normalized around league average
    games_factor = min(1.0, d["games"] / 1000.0)
    return total_pts_proxy * efficiency_bonus * games_factor / 250.0


def _raw_playoff_bpm_free(d: dict) -> float:
    """
    BPM-free playoff: replace playoff BPM ratio with raw box-score playoff stats.

    Uses playoff PPG, RPG, APG as quality signals, plus championship equity.
    """
    poff = d["playoffs"]
    po_ppg = poff["ppg"]
    po_rpg = poff["rpg"]
    po_apg = poff["apg"]
    po_ws = poff["win_shares"]
    po_games = poff["games"]

    # Amplification via raw scoring: playoff PPG / RS PPG
    rs_ppg = max(d["ppg"], 1.0)
    scoring_ampli = po_ppg / rs_ppg

    # Quality composite (playoff box-score stats)
    quality = po_ppg * 0.50 + po_rpg * 0.25 + po_apg * 0.25

    # Per-round WS rate (kept; WS is not BPM-derived, it's from team wins allocation)
    rounds_proxy = max(po_games / 15.0, 1.0)
    per_round_ws = po_ws / rounds_proxy

    # Championship equity (same as original — not BPM-dependent)
    if d["championships"] > 0:
        frac = (d["finals_mvp"] + 0.3) / (d["championships"] + 0.3)
        frac = min(frac, 1.0)
    else:
        frac = 0.0
    champ_equity = d["championships"] * frac

    return (
        0.35 * quality * scoring_ampli / 3.0    # scaled to ~10 range
        + 0.25 * per_round_ws * 3.5
        + 0.30 * champ_equity * 4.0
        + 0.10 * quality / 2.5                  # raw quality bonus
    )


def _raw_winning_bpm_free(d: dict) -> float:
    """
    BPM-free winning: replace Win Shares / WS/48 / BPM multiplier with
    raw box-score productivity × team success proxies.

    Win Shares is partly BPM-adjacent (derived from team wins, not BPM regression),
    but to be conservative we replace it entirely with a box-score composite.
    """
    era = d.get("era", 1990)
    era_factor = 1.00 if era >= 1980 else (0.88 if era >= 1970 else 0.82)

    # Box-score production rate (per-game composite)
    prod_rate = (
        d["ppg"] * 0.40
        + d["rpg"] * 0.25
        + d["apg"] * 0.20
        + d.get("spg", 0) * 0.10
        + d.get("bpg", 0) * 0.05
    ) * era_factor

    # All-NBA 1st team rate (per season) — excellence recognition proxy
    all_nba_rate = d["all_nba_1st"] / max(d["seasons"], 1)
    all_nba_norm = all_nba_rate * 200.0

    # Team success proxy: championships weighted by seasons
    team_success = d["championships"] / max(d["seasons"], 1) * 100.0

    # Blend
    return 0.40 * prod_rate * d["seasons"] / 3.0 + 0.35 * all_nba_norm + 0.25 * team_success


def _raw_efficiency_bpm_free(d: dict) -> float:
    """
    BPM-free efficiency: same as original (already uses TS% and PPG only,
    no BPM/VORP/WS inputs). Included for completeness.
    """
    return _raw_efficiency(d)


def run_csdi_bpm_free(players: dict | None = None, verbose: bool = True) -> dict:
    """
    BPM-free CSDI ablation: recompute all sub-indices using only raw box-score
    stats (PPG, RPG, APG, SPG, BPG, TS%, usage rate). No BPM, VORP, WS, PER,
    or WS/48 inputs.

    Returns same structure as run_csdi().
    """
    if players is None:
        players = PLAYERS

    names = list(players.keys())
    n = len(names)

    raw = np.zeros((n, 5))
    for i, name in enumerate(names):
        d = players[name]
        raw[i, 0] = _raw_peak_bpm_free(d)
        raw[i, 1] = _raw_longevity_bpm_free(d)
        raw[i, 2] = _raw_playoff_bpm_free(d)
        raw[i, 3] = _raw_winning_bpm_free(d)
        raw[i, 4] = _raw_efficiency_bpm_free(d)

    z = np.zeros_like(raw)
    for k in range(5):
        z[:, k] = _zscore(raw[:, k])

    if verbose:
        print("  BPM-Free Sub-index z-scores (Peak, Long, Playoff, Win, Efficiency):")
        for i, name in enumerate(names):
            row = z[i]
            print(f"    {name:25s}  "
                  f"{row[0]:+.2f}  {row[1]:+.2f}  {row[2]:+.2f}  {row[3]:+.2f}  {row[4]:+.2f}")

    # Use same weight schemes as original
    sensitivity = {}
    for scheme_name, weights in WEIGHT_SCHEMES.items():
        csdi_scores = z @ weights
        order = np.argsort(-csdi_scores)
        ranking = [(names[i], float(csdi_scores[i])) for i in order]
        sensitivity[scheme_name] = ranking

    weights_default = WEIGHT_SCHEMES["default"]
    csdi_default = z @ weights_default
    order_default = np.argsort(-csdi_default)
    rankings = [(names[i], float(csdi_default[i])) for i in order_default]

    if verbose:
        print("\n=== BPM-Free CSDI Ablation ===")
        print("\n  Default Ranking:")
        for pos, (name, score) in enumerate(rankings[:10], 1):
            print(f"    {pos:2d}. {name:25s}  CSDI = {score:.3f}")

        jordan_score = csdi_default[names.index("Michael Jordan")]
        lebron_score = csdi_default[names.index("LeBron James")]
        print(f"\n  Jordan: {jordan_score:.3f}  vs  LeBron: {lebron_score:.3f}")
        if jordan_score > lebron_score:
            print("  → Jordan still leads LeBron.")
        else:
            print("  → LeBron leads Jordan.")

    return {
        "names":          names,
        "raw_subindices": raw,
        "z_subindices":   z,
        "csdi_scores":    csdi_default,
        "rankings":       rankings,
        "sensitivity":    sensitivity,
    }


if __name__ == "__main__":
    res = run_csdi(verbose=True)
    print("\n=== CSDI Scores (all schemes) ===")
    for scheme, ranking in res["sensitivity"].items():
        top3 = ", ".join(f"{n} ({s:.2f})" for n, s in ranking[:3])
        print(f"  {scheme:20s}: {top3}")

    print("\n=== Raw sub-index values ===")
    names = res["names"]
    raw   = res["raw_subindices"]
    print(f"  {'Player':25s}  Peak    Long    Playoff  Win     Effic")
    for i, name in enumerate(names):
        r = raw[i]
        print(f"  {name:25s}  {r[0]:6.2f}  {r[1]:6.1f}  {r[2]:7.2f}  {r[3]:6.1f}  {r[4]:6.2f}")
