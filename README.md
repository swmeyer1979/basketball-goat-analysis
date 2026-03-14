# Basketball GOAT: A Multi-Method Ensemble Analysis

**Convergent Evidence for the Greatest Basketball Player of All Time**

*Samuel Meyer, March 2026*

## Overview

This repository contains the complete paper, supplementary materials, and generation code for a multi-method ensemble analysis of the basketball GOAT question. Five independent, methodologically orthogonal analytical frameworks are applied to determine the greatest basketball player of all time:

1. **Composite Statistical Dominance Index (CSDI)** -- Weighted composite of z-scored advanced metrics
2. **Era-Adjusted Relative Dominance (EARD)** -- Within-season z-scores with talent pool depth adjustment
3. **Causal Win Impact Model (CWIM)** -- Rubin causal model counterfactual win estimation
4. **Bayesian Peak-Longevity Synthesis (BPLS)** -- Hierarchical Bayesian career arc model with revealed-preference weight learning
5. **AHP with Stochastic Dominance (AHP-SD)** -- Multi-criteria decision analysis with Monte Carlo weight sampling

## Key Result

All five frameworks independently identify **Michael Jordan** as the most probable GOAT:

| Framework | GOAT | Confidence |
|-----------|------|------------|
| CSDI | Michael Jordan | Score: 3.24 (95% CI: 3.05--3.43) |
| EARD | Michael Jordan | Score: 9.72; rank 1 in 94.2% of bootstrap specs |
| CWIM | Michael Jordan | 243.7 career WAR; P(GOAT) = 0.68 |
| BPLS | Michael Jordan | P(Jordan = GOAT) = 0.48 |
| AHP-SD | Michael Jordan | Ranked #1 under 100% of 500K weight vectors |

**Ensemble probability: P(Jordan = GOAT) = 0.70**

LeBron James is the only candidate within the margin of statistical uncertainty (ensemble P = 0.21).

## Files

| File | Description |
|------|-------------|
| `Basketball_GOAT_Multi-Method_Ensemble_Analysis.pdf` | Full paper with supplementary materials (PDF) |
| `Basketball_GOAT_Multi-Method_Ensemble_Analysis.docx` | Full paper with supplementary materials (Word) |
| `basketball-goat-paper-draft.md` | Main paper body (Markdown) |
| `generate_goat_paper.py` | Python script to generate the Word document with all tables and supplementary materials |

## Supplementary Materials (included in the paper)

- **Table S1**: Full 25-player rankings across all five frameworks
- **Table S2**: Complete CSDI sub-index decomposition (5 sub-tables, top 10 players)
- **Table S3**: AHP-SD scoring rubric with statistical justification (6 sub-tables, all criteria)
- **Table S4**: CWIM natural experiment catalog (arrivals, departures, teammate effects)
- **Table S5**: BPLS posterior trajectory parameters for all 25 candidates
- **Figure S1**: Career arc data for plotting (Jordan and LeBron posterior trajectories)
- **Figure S2**: AHP-SD pairwise stochastic dominance matrix
- **Figure S3**: EARD sensitivity grid (TPD form x playoff weight)
- **Figure S4**: CWIM sensitivity grid (10 parameter specifications)
- **Figure S5**: Ensemble GOAT probability vs. peak-longevity ratio
- **Appendix A-C**: BPLS utility weights, sensitivity tables, AHP-SD archetype vectors

## Requirements

To regenerate the Word document:

```bash
pip install python-docx
python generate_goat_paper.py
```

## Data Sources

All statistical data sourced from [Basketball Reference](https://www.basketball-reference.com/), with supplementary data from NBA.com/stats and Cleaning the Glass.

## License

This work is released under the MIT License. The analysis is for research and entertainment purposes.

## Citation

```
Meyer, S. (2026). Convergent Evidence for the Greatest Basketball Player of All Time:
A Multi-Method Ensemble Analysis. Submitted to PNAS.
```
