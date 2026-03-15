"""
analysis/ablations.py
=====================
Ablation runner for the Basketball GOAT multi-method ensemble analysis.

Wraps the three reviewer-requested ablation studies:

    1. BPM-free CSDI        — run_bpm_free_csdi(players)
    2. Playoff-free CWIM    — run_playoff_free_cwim(players)
    3. Championship-free AHP-SD — run_championship_free_ahpsd(players)

Each function can be called independently or via run_all_ablations().

All imports work from repo root via `python analysis/run_all.py`.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from data.player_careers import PLAYERS                      # noqa: E402
from frameworks.csdi import run_csdi_bpm_free                # noqa: E402
from frameworks.cwim import run_cwim_playoff_free            # noqa: E402
from frameworks.ahp_sd import run_ahp_sd_no_championships   # noqa: E402


# ---------------------------------------------------------------------------
# JSON serialisation helper
# ---------------------------------------------------------------------------

def _to_json_safe(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    return obj


# ---------------------------------------------------------------------------
# Individual ablation runners
# ---------------------------------------------------------------------------

def run_bpm_free_csdi(players: dict | None = None) -> dict:
    """
    Ablation 1: BPM-free CSDI.

    Calls csdi.run_csdi_bpm_free() to replace all BPM/VORP/WS/PER/WS48
    inputs with raw box-score stats (PPG, RPG, APG, SPG, BPG, TS%).

    Parameters
    ----------
    players : dict or None
        Player career data mapping {name: career_dict}.
        Defaults to the full PLAYERS dict from data.player_careers.

    Returns
    -------
    dict with keys:
        'top_10'        : list of (name, score) tuples — top 10 under default weights
        'jordan_score'  : float
        'lebron_score'  : float
        'jordan_leads'  : bool
        'gap'           : float  (Jordan - LeBron)
        'sensitivity'   : dict {scheme: [(name, score), ...]} for top 5 per scheme
        'raw'           : full run_csdi_bpm_free() result dict
    """
    if players is None:
        players = PLAYERS

    res = run_csdi_bpm_free(players=players, verbose=False)
    rankings = res["rankings"]

    jordan_score = next(s for n, s in rankings if n == "Michael Jordan")
    lebron_score = next(s for n, s in rankings if n == "LeBron James")

    return {
        "top_10":       [(n, round(s, 3)) for n, s in rankings[:10]],
        "jordan_score": round(float(jordan_score), 3),
        "lebron_score": round(float(lebron_score), 3),
        "jordan_leads": bool(jordan_score > lebron_score),
        "gap":          round(float(jordan_score - lebron_score), 3),
        "sensitivity":  {k: [(n, round(s, 3)) for n, s in v[:5]]
                         for k, v in res["sensitivity"].items()},
        "raw":          res,
    }


def run_playoff_free_cwim(players: dict | None = None) -> dict:
    """
    Ablation 2: Playoff-free CWIM.

    Calls cwim.run_cwim_playoff_free() with two variants:
      (A) RS-only:  lambda=1.0, alpha=0, no playoff data at all.
      (B) Parity:   playoffs at 1x weight, no championship bonus (alpha=0).

    Parameters
    ----------
    players : dict or None
        Player career data.  Defaults to PLAYERS.

    Returns
    -------
    dict with keys:
        'rs_only'  : sub-dict {rankings, jordan_war, lebron_war, jordan_leads, gap}
        'parity'   : sub-dict {rankings, jordan_war, lebron_war, jordan_leads, gap}
        'raw'      : full run_cwim_playoff_free() result dict
    """
    if players is None:
        players = PLAYERS

    res = run_cwim_playoff_free(players=players, verbose=False)
    rs = res["rs_only"]
    par = res["parity"]

    return {
        "rs_only": {
            "top_10":       rs["rankings"][:10],
            "jordan_war":   rs["jordan_war"],
            "lebron_war":   rs["lebron_war"],
            "jordan_leads": rs["jordan_leads"],
            "gap":          rs["gap"],
        },
        "parity": {
            "top_10":       par["rankings"][:10],
            "jordan_war":   par["jordan_war"],
            "lebron_war":   par["lebron_war"],
            "jordan_leads": par["jordan_leads"],
            "gap":          par["gap"],
        },
        "raw": res,
    }


def run_championship_free_ahpsd(players: dict | None = None) -> dict:
    """
    Ablation 3: Championship-free AHP-SD.

    Calls ahp_sd.run_ahp_sd_no_championships() to remove C2
    (Winning/Championships) entirely and run Monte Carlo on 5 criteria.

    Parameters
    ----------
    players : dict or None
        Player career data.  Defaults to PLAYERS.

    Returns
    -------
    dict with keys:
        'jordan_dominance_pct'   : float  — Jordan % rank-1 across all draws
        'lebron_pct'             : float
        'pct_rank1'              : dict {player: float}
        'archetype_breakdown'    : dict {archetype: {player: float}}
        'lebron_leads_archetypes': list[str] — archetypes where LeBron leads
        'criteria_used'          : list[str]
        'raw'                    : full run_ahp_sd_no_championships() result dict
    """
    if players is None:
        players = PLAYERS

    res = run_ahp_sd_no_championships(
        players=players,
        n_samples=500_000,
        verbose=False,
    )

    return {
        "jordan_dominance_pct":    res["jordan_dominance_pct"],
        "lebron_pct":              res["lebron_pct"],
        "pct_rank1":               res["pct_rank1"],
        "archetype_breakdown":     res["archetype_breakdown"],
        "lebron_leads_archetypes": res["lebron_leads_archetypes"],
        "criteria_used":           res["criteria"],
        "raw":                     res,
    }


# ---------------------------------------------------------------------------
# Consolidated runner
# ---------------------------------------------------------------------------

def run_all_ablations(
    players: dict | None = None,
    verbose: bool = True,
    save: bool = False,
    results_dir: Path | None = None,
) -> dict:
    """
    Run all three ablation studies and return a consolidated summary dict.

    Parameters
    ----------
    players : dict or None
        Player career data.  Defaults to PLAYERS.
    verbose : bool
        Print progress and results to stdout.
    save : bool
        If True, write results to results_dir / ablation_<timestamp>.json.
    results_dir : Path or None
        Directory to save JSON output.  Defaults to <repo_root>/results/.

    Returns
    -------
    dict with keys:
        'bpm_free_csdi'        : run_bpm_free_csdi() result
        'playoff_free_cwim'    : run_playoff_free_cwim() result
        'championship_free_ahp': run_championship_free_ahpsd() result
        'summary': {
            'jordan_leads_count' : int   (out of 3)
            'total_ablations'    : 3
            'robust'             : bool  (jordan_leads_count == 3)
            'partially_robust'   : bool  (jordan_leads_count >= 2)
            'timestamp'          : str
        }
    """
    if players is None:
        players = PLAYERS

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    if verbose:
        print("\n" + "=" * 72)
        print("  ABLATION STUDIES — Reviewer-Requested Independence Tests")
        print("=" * 72)

    # ── Ablation 1: BPM-free CSDI ──────────────────────────────────────────
    if verbose:
        print("\n" + "-" * 72)
        print("  ABLATION 1: BPM-Free CSDI")
        print("  (Replace all BPM/VORP/WS/PER/WS48 with raw box-score stats)")
        print("-" * 72)

    ab1 = run_bpm_free_csdi(players=players)

    if verbose:
        print(f"\n  Default Ranking (top 10):")
        for pos, (name, score) in enumerate(ab1["top_10"], 1):
            print(f"    {pos:2d}. {name:25s}  CSDI = {score:.3f}")
        direction = "LEADS" if ab1["jordan_leads"] else "TRAILS"
        print(f"\n  Jordan {direction} LeBron  "
              f"({ab1['jordan_score']:.3f} vs {ab1['lebron_score']:.3f}, "
              f"gap = {ab1['gap']:+.3f})")

    # ── Ablation 2: Playoff-free CWIM ──────────────────────────────────────
    if verbose:
        print("\n" + "-" * 72)
        print("  ABLATION 2: Playoff-Free CWIM")
        print("  (A) RS-only: no playoff data at all")
        print("  (B) Parity: playoffs at 1x, no championship bonus")
        print("-" * 72)

    ab2 = run_playoff_free_cwim(players=players)
    rs = ab2["rs_only"]
    par = ab2["parity"]

    if verbose:
        print("\n  Variant A — RS-Only (top 10):")
        for pos, (name, war) in enumerate(rs["top_10"], 1):
            print(f"    {pos:2d}. {name:25s}  {war:.1f} WAR")
        direction_rs = "LEADS" if rs["jordan_leads"] else "TRAILS"
        print(f"\n  Jordan {direction_rs} LeBron  "
              f"({rs['jordan_war']:.1f} vs {rs['lebron_war']:.1f}, "
              f"gap = {rs['gap']:+.1f})")

        print("\n  Variant B — Parity (top 10):")
        for pos, (name, war) in enumerate(par["top_10"], 1):
            print(f"    {pos:2d}. {name:25s}  {war:.1f} WAR")
        direction_par = "LEADS" if par["jordan_leads"] else "TRAILS"
        print(f"\n  Jordan {direction_par} LeBron  "
              f"({par['jordan_war']:.1f} vs {par['lebron_war']:.1f}, "
              f"gap = {par['gap']:+.1f})")

    # ── Ablation 3: Championship-free AHP-SD ───────────────────────────────
    if verbose:
        print("\n" + "-" * 72)
        print("  ABLATION 3: Championship-Free AHP-SD")
        print("  (Remove C2 Winning/Championships entirely)")
        print("-" * 72)

    ab3 = run_championship_free_ahpsd(players=players)

    if verbose:
        print(f"\n  Jordan dominance: {ab3['jordan_dominance_pct']:.2f}%")
        print(f"  LeBron:           {ab3['lebron_pct']:.2f}%")
        print("\n  Per-archetype breakdown (Jordan % | LeBron %):")
        for arch_name, arch_pct in ab3["archetype_breakdown"].items():
            j_pct = arch_pct.get("Michael Jordan", 0.0)
            l_pct = arch_pct.get("LeBron James", 0.0)
            leader = "Jordan" if j_pct >= l_pct else "LEBRON"
            print(f"    {arch_name:20s}:  Jordan {j_pct:6.2f}%  LeBron {l_pct:6.2f}%  [{leader}]")
        if ab3["lebron_leads_archetypes"]:
            print(f"  → LeBron leads under: {', '.join(ab3['lebron_leads_archetypes'])}")
        else:
            print("  → Jordan leads under ALL archetypes even without championships.")

    # ── Summary ────────────────────────────────────────────────────────────
    jordan_leads_rs = rs["jordan_leads"]
    jordan_leads_ahp = ab3["jordan_dominance_pct"] > ab3["lebron_pct"]
    jordan_wins = sum([
        ab1["jordan_leads"],
        jordan_leads_rs,
        jordan_leads_ahp,
    ])

    if verbose:
        print("\n" + "=" * 72)
        print("  ABLATION SUMMARY")
        print("=" * 72)
        print(f"\n  1. BPM-Free CSDI:              Jordan {'LEADS' if ab1['jordan_leads'] else 'TRAILS'} "
              f"({ab1['jordan_score']:.3f} vs {ab1['lebron_score']:.3f})")
        print(f"  2a. RS-Only CWIM:              Jordan {'LEADS' if rs['jordan_leads'] else 'TRAILS'} "
              f"({rs['jordan_war']:.1f} vs {rs['lebron_war']:.1f} WAR)")
        print(f"  2b. Parity CWIM (1x playoff):  Jordan {'LEADS' if par['jordan_leads'] else 'TRAILS'} "
              f"({par['jordan_war']:.1f} vs {par['lebron_war']:.1f} WAR)")
        print(f"  3. Championship-Free AHP:      Jordan {'LEADS' if jordan_leads_ahp else 'TRAILS'} "
              f"({ab3['jordan_dominance_pct']:.1f}% vs {ab3['lebron_pct']:.1f}%)")
        print(f"\n  Jordan leads {jordan_wins}/3 ablations (using RS-only for #2).")

        if jordan_wins == 3:
            print("  Result is ROBUST: Jordan leads all three ablations.")
        elif jordan_wins >= 2:
            print(f"  Result is PARTIALLY ROBUST: Jordan leads {jordan_wins}/3 ablations.")
        else:
            print(f"  Result is FRAGILE: Jordan leads only {jordan_wins}/3 ablations.")

        print("=" * 72 + "\n")

    results = {
        "bpm_free_csdi":         ab1,
        "playoff_free_cwim":     ab2,
        "championship_free_ahp": ab3,
        "summary": {
            "jordan_leads_count": jordan_wins,
            "total_ablations":    3,
            "robust":             jordan_wins == 3,
            "partially_robust":   jordan_wins >= 2,
            "timestamp":          timestamp,
        },
    }

    if save:
        if results_dir is None:
            results_dir = REPO_ROOT / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        # Strip raw sub-dicts to keep file size manageable
        saveable = {k: v for k, v in results.items()}
        for key in ("bpm_free_csdi", "playoff_free_cwim", "championship_free_ahp"):
            if key in saveable and isinstance(saveable[key], dict):
                saveable[key] = {k2: v2 for k2, v2 in saveable[key].items()
                                 if k2 != "raw"}
        fpath = results_dir / f"ablation_{timestamp}.json"
        with open(fpath, "w") as f:
            json.dump(_to_json_safe(saveable), f, indent=2)
        if verbose:
            print(f"  Results saved to {fpath.name}")

    return results


# ---------------------------------------------------------------------------
# Standalone execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_all_ablations(verbose=True, save=True)
