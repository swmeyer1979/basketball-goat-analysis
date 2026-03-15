"""
analysis/run_ablations.py
=========================
Run all three ablation studies requested by reviewers:

1. BPM-free CSDI — replace all BPM/VORP/WS inputs with raw box-score stats
2. Playoff-free CWIM — pure RS WAR + parity variant (no leverage, no CPA)
3. Championship-free AHP-SD — remove C2 entirely, run Monte Carlo on 5 criteria

Saves results to results/ablation_*.json.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from data.player_careers import PLAYERS  # noqa: E402
from frameworks.csdi import run_csdi_bpm_free  # noqa: E402
from frameworks.cwim import run_cwim_playoff_free  # noqa: E402
from frameworks.ahp_sd import run_ahp_sd_no_championships  # noqa: E402


def _to_json_safe(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    return obj


def run_all_ablations(verbose: bool = True, save: bool = True) -> dict:
    """Run all three ablation studies and return consolidated results."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results = {}

    print("\n" + "=" * 72)
    print("  ABLATION STUDIES — Reviewer-Requested Independence Tests")
    print("=" * 72)

    # ── Ablation 1: BPM-free CSDI ──────────────────────────────────────────
    print("\n" + "-" * 72)
    print("  ABLATION 1: BPM-Free CSDI")
    print("  (Replace all BPM/VORP/WS/PER/WS48 with raw box-score stats)")
    print("-" * 72)

    csdi_res = run_csdi_bpm_free(players=PLAYERS, verbose=verbose)
    rankings_csdi = csdi_res["rankings"]
    jordan_csdi = next(s for n, s in rankings_csdi if n == "Michael Jordan")
    lebron_csdi = next(s for n, s in rankings_csdi if n == "LeBron James")
    results["bpm_free_csdi"] = {
        "top_10":       [(n, round(s, 3)) for n, s in rankings_csdi[:10]],
        "jordan_score":  round(jordan_csdi, 3),
        "lebron_score":  round(lebron_csdi, 3),
        "jordan_leads":  jordan_csdi > lebron_csdi,
        "gap":           round(jordan_csdi - lebron_csdi, 3),
        "sensitivity":   {k: [(n, round(s, 3)) for n, s in v[:5]]
                          for k, v in csdi_res["sensitivity"].items()},
    }

    # ── Ablation 2: Playoff-free CWIM ──────────────────────────────────────
    print("\n" + "-" * 72)
    print("  ABLATION 2: Playoff-Free CWIM")
    print("  (A) RS-only: no playoff data at all")
    print("  (B) Parity: playoffs at 1x, no championship bonus")
    print("-" * 72)

    cwim_res = run_cwim_playoff_free(players=PLAYERS, verbose=verbose)
    rs = cwim_res["rs_only"]
    par = cwim_res["parity"]
    results["playoff_free_cwim"] = {
        "rs_only": {
            "top_10":      rs["rankings"][:10],
            "jordan_war":  rs["jordan_war"],
            "lebron_war":  rs["lebron_war"],
            "jordan_leads": rs["jordan_leads"],
            "gap":         rs["gap"],
        },
        "parity": {
            "top_10":      par["rankings"][:10],
            "jordan_war":  par["jordan_war"],
            "lebron_war":  par["lebron_war"],
            "jordan_leads": par["jordan_leads"],
            "gap":         par["gap"],
        },
    }

    # ── Ablation 3: Championship-free AHP-SD ───────────────────────────────
    print("\n" + "-" * 72)
    print("  ABLATION 3: Championship-Free AHP-SD")
    print("  (Remove C2 Winning/Championships entirely)")
    print("-" * 72)

    ahp_res = run_ahp_sd_no_championships(
        players=PLAYERS, n_samples=500_000, verbose=verbose,
    )
    results["championship_free_ahp"] = {
        "jordan_dominance_pct":    ahp_res["jordan_dominance_pct"],
        "lebron_pct":              ahp_res["lebron_pct"],
        "pct_rank1":               ahp_res["pct_rank1"],
        "archetype_breakdown":     ahp_res["archetype_breakdown"],
        "lebron_leads_archetypes": ahp_res["lebron_leads_archetypes"],
        "criteria_used":           ahp_res["criteria"],
    }

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("  ABLATION SUMMARY")
    print("=" * 72)

    ab1 = results["bpm_free_csdi"]
    ab2_rs = results["playoff_free_cwim"]["rs_only"]
    ab2_par = results["playoff_free_cwim"]["parity"]
    ab3 = results["championship_free_ahp"]

    # For the summary count, use RS-only (strongest ablation)
    jordan_wins = sum([
        ab1["jordan_leads"],
        ab2_rs["jordan_leads"],
        ab3["jordan_dominance_pct"] > ab3["lebron_pct"],
    ])

    print(f"\n  1. BPM-Free CSDI:              Jordan {'LEADS' if ab1['jordan_leads'] else 'TRAILS'} "
          f"({ab1['jordan_score']:.3f} vs {ab1['lebron_score']:.3f})")
    print(f"  2a. RS-Only CWIM:              Jordan {'LEADS' if ab2_rs['jordan_leads'] else 'TRAILS'} "
          f"({ab2_rs['jordan_war']:.1f} vs {ab2_rs['lebron_war']:.1f} WAR)")
    print(f"  2b. Parity CWIM (1x playoff):  Jordan {'LEADS' if ab2_par['jordan_leads'] else 'TRAILS'} "
          f"({ab2_par['jordan_war']:.1f} vs {ab2_par['lebron_war']:.1f} WAR)")
    print(f"  3. Championship-Free AHP:      Jordan {'LEADS' if ab3['jordan_dominance_pct'] > ab3['lebron_pct'] else 'TRAILS'} "
          f"({ab3['jordan_dominance_pct']:.1f}% vs {ab3['lebron_pct']:.1f}%)")
    print(f"\n  Jordan leads {jordan_wins}/3 ablations (using RS-only for #2).")

    if jordan_wins == 3:
        print("  Result is ROBUST: Jordan leads all three ablations.")
        print("    The five-framework convergence is not an artifact of shared BPM inputs,")
        print("    shared playoff weighting, or shared championship valuation.")
    elif jordan_wins >= 2:
        print(f"  Result is PARTIALLY ROBUST: Jordan leads {jordan_wins}/3 ablations.")
        if not ab2_rs["jordan_leads"]:
            print("    The CWIM ablation reveals that removing all postseason signal causes")
            print("    LeBron's longevity advantage to dominate. This is the expected result")
            print("    and confirms that playoff amplification is load-bearing for Jordan's")
            print("    CWIM advantage — but the result survives in BPM-free and championship-free")
            print("    tests, meaning the convergence is not an artifact of a single shared bias.")
    else:
        print(f"  Result is FRAGILE: Jordan leads only {jordan_wins}/3 ablations.")

    results["summary"] = {
        "jordan_leads_count": jordan_wins,
        "total_ablations": 3,
        "robust": jordan_wins == 3,
        "partially_robust": jordan_wins >= 2,
        "timestamp": timestamp,
    }

    # ── Save ───────────────────────────────────────────────────────────────
    if save:
        results_dir = REPO_ROOT / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        fpath = results_dir / f"ablation_{timestamp}.json"
        with open(fpath, "w") as f:
            json.dump(_to_json_safe(results), f, indent=2)
        print(f"\n  Results saved to {fpath.name}")

    print("=" * 72 + "\n")
    return results


if __name__ == "__main__":
    run_all_ablations(verbose=True, save=True)
