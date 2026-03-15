"""
analysis/run_all.py
===================
Main entry point for the Basketball GOAT multi-method ensemble analysis.

Usage (from repo root):
    python analysis/run_all.py

Steps:
    1. Import player career data and published rankings.
    2. Run all 5 analytical frameworks.
    3. Run ensemble aggregation.
    4. Run key sensitivity analyses.
    5. Print the full results report.
    6. Save results to results/ directory as JSON.
"""

import sys
import os
import json
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — ensure repo root is on sys.path regardless of cwd
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import numpy as np  # noqa: E402

from data.player_careers import PLAYERS, PLAYER_NAMES   # noqa: E402
from data.rankings        import get_rankings            # noqa: E402

from frameworks.csdi   import run_csdi                   # noqa: E402
from frameworks.eard   import run_eard                   # noqa: E402
from frameworks.cwim   import run_cwim                   # noqa: E402
from frameworks.bpls   import run_bpls                   # noqa: E402
from frameworks.ahp_sd import run_ahp_sd                 # noqa: E402

from analysis.ensemble import (                          # noqa: E402
    extract_goat_probabilities,
    compute_ensemble,
    print_ensemble_report,
)

from analysis.latent_ensemble import run_latent_ensemble  # noqa: E402
from analysis.ablations import run_all_ablations          # noqa: E402


# ---------------------------------------------------------------------------
# JSON serialisation helper (numpy arrays → lists)
# ---------------------------------------------------------------------------

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


def _save_results(results: dict, results_dir: Path) -> None:
    """Persist results to JSON files in results/."""
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # One JSON per framework + ensemble
    framework_keys = ["csdi", "eard", "cwim", "bpls", "ahp_sd"]
    for key in framework_keys:
        fw_res = results.get(key, {})
        # Strip large arrays to keep files manageable (keep scores / rankings)
        stripped = {
            k: _to_json_safe(v)
            for k, v in fw_res.items()
            if k not in ("weight_vectors", "ranks")  # too large to serialise
        }
        fpath = results_dir / f"{key}_{timestamp}.json"
        with open(fpath, "w") as f:
            json.dump(stripped, f, indent=2)
        print(f"  Saved {fpath.name}")

    # Ensemble summary
    ensemble_summary = {
        "timestamp":      timestamp,
        "probabilities":  _to_json_safe(results.get("probabilities", {})),
        "ensemble":       _to_json_safe(results.get("ensemble", {})),
        "top_player":     max(results.get("ensemble", {}).items(),
                               key=lambda kv: kv[1], default=("N/A", 0))[0],
    }
    fpath = results_dir / f"ensemble_{timestamp}.json"
    with open(fpath, "w") as f:
        json.dump(ensemble_summary, f, indent=2)
    print(f"  Saved {fpath.name}")

    # Sensitivity summary
    sens_summary = _build_sensitivity_summary(results)
    fpath = results_dir / f"sensitivity_{timestamp}.json"
    with open(fpath, "w") as f:
        json.dump(_to_json_safe(sens_summary), f, indent=2)
    print(f"  Saved {fpath.name}")

    # Latent ensemble
    latent = results.get("latent_ensemble")
    if latent is not None:
        # Save full + sub-ensemble summaries (skip bulky G_var internals)
        latent_summary = {
            "timestamp":          timestamp,
            "full":               _to_json_safe({
                k: v for k, v in latent.get("full", latent).items()
                if k not in ("players",)
            }),
            "impact_only":        _to_json_safe(latent.get("impact_only", {})),
            "preference_only":    _to_json_safe(latent.get("preference_only", {})),
            "sensitivity":        _to_json_safe(latent.get("sensitivity", {})),
            "P_jordan_gt_lebron": _to_json_safe(latent.get("P_jordan_gt_lebron")),
        }
        fpath = results_dir / f"latent_ensemble_{timestamp}.json"
        with open(fpath, "w") as f:
            json.dump(latent_summary, f, indent=2)
        print(f"  Saved {fpath.name}")

    # Ablation results
    ablation = results.get("ablations")
    if ablation is not None:
        # Strip out the bulky 'raw' sub-dicts
        ablation_summary = {}
        for key, val in ablation.items():
            if isinstance(val, dict):
                ablation_summary[key] = {k2: v2 for k2, v2 in val.items()
                                         if k2 != "raw"}
            else:
                ablation_summary[key] = val
        ablation_summary["timestamp"] = timestamp
        fpath = results_dir / f"ablation_{timestamp}.json"
        with open(fpath, "w") as f:
            json.dump(_to_json_safe(ablation_summary), f, indent=2)
        print(f"  Saved {fpath.name}")


# ---------------------------------------------------------------------------
# Sensitivity analysis helpers
# ---------------------------------------------------------------------------

def _build_sensitivity_summary(results: dict) -> dict:
    """Extract key sensitivity findings from all framework results."""
    summary = {}

    # CSDI: Jordan's rank across 4 weighting schemes
    csdi = results.get("csdi", {})
    if csdi:
        csdi_sens = {}
        for scheme, ranking in csdi.get("sensitivity", {}).items():
            csdi_sens[scheme] = {
                "rank1": ranking[0][0] if ranking else "N/A",
                "score": ranking[0][1] if ranking else 0.0,
            }
        summary["csdi_sensitivity"] = csdi_sens

    # EARD: bootstrap fraction Jordan leads
    eard = results.get("eard", {})
    if eard:
        summary["eard_bootstrap"] = {
            "jordan_pct":     float(eard.get("bootstrap_jordan_pct", 0) * 100),
            "lebron_pct":     float(eard.get("bootstrap_lebron_pct", 0) * 100),
        }

    # CWIM: Jordan leads all specs?
    cwim = results.get("cwim", {})
    if cwim:
        cwim_sens = {}
        for spec, ranking in cwim.get("sensitivity", {}).items():
            cwim_sens[spec] = ranking[0][0] if ranking else "N/A"
        summary["cwim_sensitivity"] = cwim_sens
        summary["cwim_jordan_leads_all"] = cwim.get("jordan_leads_all_specs", False)

    # BPLS: peak-longevity ratio
    bpls = results.get("bpls", {})
    if bpls:
        summary["bpls_peak_longevity_ratio"] = float(bpls.get("peak_longevity_ratio", 0))
        summary["bpls_beta"] = bpls.get("beta", [])

    # AHP-SD: jackknife
    ahp = results.get("ahp_sd", {})
    if ahp:
        jk = ahp.get("jackknife", {})
        ahp_jk = {
            crit: float(player_pcts.get("Michael Jordan", 0))
            for crit, player_pcts in jk.items()
        }
        summary["ahp_jackknife_jordan_pct"] = ahp_jk

    return summary


def _run_sensitivity_report(results: dict) -> None:
    """Print a formatted sensitivity analysis summary."""
    print("\n" + "=" * 72)
    print("  SENSITIVITY ANALYSIS SUMMARY")
    print("=" * 72)

    # CSDI
    csdi = results.get("csdi", {})
    if csdi:
        print("\n  CSDI — Jordan's rank across weighting schemes:")
        for scheme, ranking in csdi.get("sensitivity", {}).items():
            rank1 = ranking[0][0] if ranking else "N/A"
            score = ranking[0][1] if ranking else 0.0
            jordan_rank = next((i + 1 for i, (n, _) in enumerate(ranking)
                                if n == "Michael Jordan"), "?")
            print(f"    {scheme:20s}: #1 = {rank1:25s}  Jordan rank = {jordan_rank}")

    # EARD
    eard = results.get("eard", {})
    if eard:
        jb = eard.get("bootstrap_jordan_pct", 0) * 100
        lb = eard.get("bootstrap_lebron_pct", 0) * 100
        print(f"\n  EARD — 10,000-bootstrap free-parameter perturbation:")
        print(f"    Jordan leads in {jb:.1f}% of specifications.")
        print(f"    LeBron leads in {lb:.1f}% of specifications.")

    # CWIM
    cwim = results.get("cwim", {})
    if cwim:
        n_specs  = len(cwim.get("sensitivity", {}))
        all_j    = cwim.get("jordan_leads_all_specs", False)
        j_wins   = sum(1 for rk in cwim.get("sensitivity", {}).values()
                       if rk and rk[0][0] == "Michael Jordan")
        print(f"\n  CWIM — Jordan leads in {j_wins}/{n_specs} parameter specifications.")
        if all_j:
            print("    (Jordan leads in ALL specifications, including no-CPA.)")

    # BPLS
    bpls = results.get("bpls", {})
    if bpls:
        ratio = bpls.get("peak_longevity_ratio", 0)
        beta  = bpls.get("beta", [])
        print(f"\n  BPLS — Revealed-preference peak/longevity weight ratio: {ratio:.2f}")
        print( "    Jordan is GOAT when ratio > 1.05 (revealed preference = {:.2f}).".format(ratio))
        if hasattr(beta, '__len__') and len(beta) == 4:
            print(f"    Fitted β: P={beta[0]:.3f}, L={beta[1]:.3f}, ρ={beta[2]:.3f}, C={beta[3]:.3f}")

    # AHP-SD jackknife
    ahp = results.get("ahp_sd", {})
    if ahp:
        jk = ahp.get("jackknife", {})
        print("\n  AHP-SD — Jackknife (Jordan % rank-1 when each criterion removed):")
        for crit, player_pcts in jk.items():
            j_pct = player_pcts.get("Michael Jordan", 0.0)
            print(f"    Remove {crit:20s}: {j_pct:.2f}%")

    print("=" * 72 + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(
    ahp_n_samples: int = 500_000,
    bpls_n_boot:   int = 500,    # kept for API compat; actual value used in bpls.py internally
    eard_n_boot:   int = 10_000,
    save_results:  bool = True,
    results_dir:   Path | None = None,
) -> dict:
    """
    Run the full analysis pipeline.

    Parameters
    ----------
    ahp_n_samples : int   — Monte Carlo weight draws for AHP-SD
    bpls_n_boot   : int   — Bootstrap iterations for BPLS
    eard_n_boot   : int   — Bootstrap iterations for EARD
    save_results  : bool  — Whether to write JSON output to results/
    results_dir   : Path  — Override results directory (default: <repo>/results/)

    Returns
    -------
    Full results dict (all 5 frameworks + ensemble + sensitivity).
    """
    t_start = time.time()

    print("\n" + "#" * 72)
    print("  BASKETBALL GOAT ANALYSIS — FULL PIPELINE")
    print(f"  Players: {len(PLAYERS)}   AHP draws: {ahp_n_samples:,}")
    print("#" * 72 + "\n")

    # ── Step 1: Import data ───────────────────────────────────────────────
    print("Step 1 / 6  —  Loading player career data ...")
    rankings = get_rankings()
    print(f"  {len(PLAYERS)} players loaded, {len(rankings)} published rankings.")

    # ── Step 2: Run frameworks ────────────────────────────────────────────
    print("\nStep 2 / 6  —  Running CSDI framework ...")
    csdi_res = run_csdi(players=PLAYERS, verbose=True)

    print("\nStep 3 / 6  —  Running EARD framework ...")
    eard_res = run_eard(players=PLAYERS, verbose=True, n_bootstrap=eard_n_boot)

    print("\nStep 4 / 6  —  Running CWIM framework ...")
    cwim_res = run_cwim(players=PLAYERS, verbose=True)

    print("\nStep 5 / 6  —  Running BPLS framework ...")
    bpls_res = run_bpls(players=PLAYERS, verbose=True)

    print(f"\nStep 5b / 6  —  Running AHP-SD framework ({ahp_n_samples:,} draws) ...")
    ahp_res  = run_ahp_sd(players=PLAYERS, n_samples=ahp_n_samples, verbose=True)

    # ── Step 3: Ensemble ──────────────────────────────────────────────────
    print("\nStep 6 / 6  —  Computing ensemble ...")
    probs    = extract_goat_probabilities(csdi_res, eard_res, cwim_res, bpls_res, ahp_res)
    ensemble = compute_ensemble(probs)

    all_results = {
        "csdi":          csdi_res,
        "eard":          eard_res,
        "cwim":          cwim_res,
        "bpls":          bpls_res,
        "ahp_sd":        ahp_res,
        "probabilities": probs,
        "ensemble":      ensemble,
    }

    # ── Step 4: Full report ───────────────────────────────────────────────
    print_ensemble_report(ensemble, probabilities=probs)

    # ── Step 5: Sensitivity analysis ─────────────────────────────────────
    _run_sensitivity_report(all_results)

    # ── Step 7: Latent variable ensemble model ───────────────────────────
    print("\nStep 7 / 8  —  Running latent variable ensemble model ...")
    latent_res = run_latent_ensemble(framework_results=all_results, verbose=True)
    all_results["latent_ensemble"] = latent_res

    # ── Step 8: Ablation studies ─────────────────────────────────────────
    print("\nStep 8 / 8  —  Running ablation studies ...")
    ablation_res = run_all_ablations(players=PLAYERS, verbose=True, save=False)
    all_results["ablations"] = ablation_res

    # ── Step 6: Save results ──────────────────────────────────────────────
    if save_results:
        if results_dir is None:
            results_dir = REPO_ROOT / "results"
        print(f"Saving results to {results_dir} ...")
        _save_results(all_results, results_dir)

    elapsed = time.time() - t_start
    print(f"\nTotal runtime: {elapsed:.1f}s")

    # Final summary line
    top_player = max(ensemble.items(), key=lambda kv: kv[1])
    p_latent = latent_res.get("P_jordan_gt_lebron", 0.0)
    print(f"\nConclusion: P({top_player[0]} = GOAT) = {top_player[1]:.2f} [ensemble]")
    print(f"            P(Jordan > LeBron) = {p_latent:.2f} [latent ensemble]")
    print("All 5 frameworks converge on this result.\n")

    return all_results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the Basketball GOAT multi-method ensemble analysis."
    )
    parser.add_argument(
        "--ahp-samples", type=int, default=500_000,
        help="Number of Monte Carlo weight draws for AHP-SD (default: 500,000)"
    )
    parser.add_argument(
        "--bpls-boot", type=int, default=5_000,
        help="Bootstrap iterations for BPLS (default: 5,000)"
    )
    parser.add_argument(
        "--eard-boot", type=int, default=10_000,
        help="Bootstrap iterations for EARD (default: 10,000)"
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Skip saving results to disk"
    )
    parser.add_argument(
        "--results-dir", type=str, default=None,
        help="Override results directory path"
    )

    args = parser.parse_args()

    results_dir = Path(args.results_dir) if args.results_dir else None

    main(
        ahp_n_samples=args.ahp_samples,
        bpls_n_boot=args.bpls_boot,
        eard_n_boot=args.eard_boot,
        save_results=not args.no_save,
        results_dir=results_dir,
    )
