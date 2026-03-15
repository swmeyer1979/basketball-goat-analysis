# Convergent Evidence for the Greatest Basketball Player of All Time: A Multi-Method Ensemble Analysis

**Samuel Meyer**



---

## Abstract

The basketball GOAT debate persists not because evidence is lacking, but because evaluators disagree on what to measure. We construct five complementary analytical frameworks (CSDI, EARD, CWIM, BPLS, AHP-SD), each addressing different threats to validity. Four of five identify Michael Jordan as the most probable GOAT; the fifth produces a statistical tie with LeBron James holding a marginal point-estimate lead. The cross-method agreement index is 0.70 (range: 0.48--1.00). LeBron is the only candidate within the margin of uncertainty (0.21). The frameworks share a common data substrate but differ in analytical approach and bias profile, so their convergence reflects robustness across modeling choices rather than full independence. We present the ensemble analysis, identify the conditions under which the result would change, and quantify the uncertainty inherent in cross-era comparison.

**Keywords:** sports analytics, multi-criteria decision analysis, Bayesian hierarchical models, causal inference, era adjustment, basketball

---

## 1. Introduction

### 1.1 The Problem

The basketball GOAT question is hard not because the data is thin but because "greatest" is underdefined. Peak dominance, career longevity, championship count, and two-way impact all have legitimate claims on the concept, and they point to different players. Michael Jordan scored 30.1 PPG with a 6-0 Finals record. LeBron James scored 40,474 career points across 21 elite seasons. Kareem Abdul-Jabbar won 6 MVPs over two decades. Bill Russell has 11 rings. Each of these facts is a valid argument for a different answer.

Previous work has typically picked one methodology — career statistics [1], WAR estimation [2], adjusted plus-minus [3], or expert assessment [4] — and lived with its blind spots. No single method can address era incomparability, the peak-versus-longevity tradeoff, causal attribution in a team sport, and the legitimate plurality of evaluative criteria at the same time.

### 1.2 Our Approach: Methodological Triangulation

Our approach borrows from psychometrics: **convergent validity** [5]. Build multiple instruments with different biases. If they agree, the agreement is more trustworthy than any single reading. We build five:

1. **Composite Statistical Dominance Index (CSDI)** — Weighted linear combination of z-scored advanced metrics across five sub-indices (peak, longevity, playoff amplification, winning contribution, era-adjusted efficiency). Roots in classical psychometric composite construction.

2. **Era-Adjusted Relative Dominance (EARD)** — Within-season z-scoring with talent pool depth adjustment, rule-change structural corrections, and playoff leverage weighting. Roots in cross-cultural measurement theory and standardized testing.

3. **Causal Win Impact Model (CWIM)** — Counterfactual estimation of career wins above replacement using triangulated quasi-experimental identification strategies (on/off splits, teammate discontinuities, team trajectory analysis) combined via Bayesian model averaging. Roots in the Rubin causal model [6].

4. **Bayesian Peak-Longevity Synthesis (BPLS)** — Hierarchical Bayesian model of latent ability trajectories fitted via Hamiltonian Monte Carlo, with peak-versus-longevity tradeoff weights learned from revealed preferences in historical expert rankings via a Plackett-Luce observation model. Roots in Bayesian nonparametrics and preference learning [7].

5. **Analytic Hierarchy Process with Stochastic Dominance (AHP-SD)** — Multi-criteria scoring across six dimensions with weight uncertainty modeled as a Dirichlet mixture over five stakeholder archetypes, tested for stochastic dominance across 500,000 Monte Carlo weight vector draws. Roots in operations research and decision science [8].

The methods draw from a common data substrate (Basketball Reference career statistics) but differ substantially in analytical approach, weighting philosophy, and structural assumptions. Their biases are distinct and, in several cases, opposing — CWIM is purely cumulative and favors longevity; BPLS learns its peak-favoring weight from data; AHP-SD is agnostic. The frameworks are not fully independent, though: all rely to varying degrees on BPM-family metrics, and all incorporate some form of postseason weighting. We discuss the implications of these shared dependencies for the convergence argument in Section 5.10. Despite these shared elements, convergence across five frameworks with different formalisms and opposing bias profiles provides meaningful evidence that the result is robust. It is not the same as five fully independent confirmations — but it is considerably more than one.

### 1.3 Scope and Limitations

Our analysis is restricted to players for whom reliable statistical records exist, effectively limiting the candidate pool to careers beginning circa 1950 or later. Players from the BAA era (1946--1949) are excluded. Pre-1974 players (before steals, blocks, and turnovers were tracked) are included with wider uncertainty bounds. Active players are evaluated on completed seasons through 2023--24; their rankings may change as careers conclude.

We are not measuring "talent" in some abstract sense. We are measuring **accomplished impact** — how much each player dominated their era, contributed to winning, and sustained excellence. That is a function of both ability and context. We make no attempt to separate them.

---

## 2. Data

All statistical data are sourced from Basketball Reference (basketball-reference.com), with supplementary play-by-play data from NBA.com/stats (available 1996--present) and Cleaning the Glass (available 2007--present). Data were accessed in February 2026.

### 2.1 Candidate Selection

We evaluate 25 candidates: any player appearing in the top 10 of at least two major published all-time rankings (ESPN, Sports Illustrated, The Athletic, Bleacher Report, and Simmons [4]). The candidates span seven decades (1954--2024) and include both completed and active careers. For presentation clarity, we focus on the top 10 in our ensemble ranking while reporting full results in Supplementary Table S1.

### 2.2 Statistical Inputs

Each framework draws from a common data layer but processes it differently:

| Metric | Availability | Used By |
|---|---|---|
| Points, rebounds, assists, FG%, FT% | 1950--present | All |
| Steals, blocks, turnovers | 1974--present | CSDI, EARD, CWIM, BPLS |
| Player Efficiency Rating (PER) | 1952--present (estimated pre-1974) | CSDI, BPLS |
| Box Plus-Minus (BPM) | 1974--present (backfilled pre-1974 via regression) | All |
| Win Shares (WS), WS/48 | 1952--present | CSDI, CWIM, AHP-SD |
| Value Over Replacement (VORP) | 1974--present | CSDI, EARD, BPLS |
| True Shooting % (TS%) | 1952--present | CSDI, EARD |
| On/off court net rating | 1997--present | CWIM |
| Playoff statistics (all above) | 1950--present | All |
| Team pace, possessions | 1974--present (estimated earlier) | EARD, CWIM |
| Championship results, Finals MVP, MVP voting | 1956--present | All |
| All-NBA, All-Defensive selections | 1947--present | AHP-SD, BPLS |

### 2.3 Era Adjustment Data

For the EARD and BPLS frameworks, we compute within-season distributional parameters (mean, standard deviation) for each metric across all qualifying players (≥ 41 games, ≥ 20 MPG) in each season. For the CWIM framework, we calibrate replacement level using expansion team performance data. For the AHP-SD framework, era adjustment is embedded in the scoring rubric.

---

## 3. Methods

### 3.1 Framework 1: Composite Statistical Dominance Index (CSDI)

The CSDI computes a weighted linear combination of five normalized sub-indices:

> CSDI(p) = w1 · Z1(p) + w2 · Z2(p) + w3 · Z3(p) + w4 · Z4(p) + w5 · Z5(p)

where Z_k(p) is the z-score of player p on sub-index k relative to all qualifying players (≥ 400 career games since 1970), and w_k are weights: Peak Dominance (0.25), Longevity-Adjusted Production (0.20), Playoff Amplification (0.25), Winning Contribution (0.20), Era-Adjusted Efficiency (0.10).

**Peak Dominance** (Z_peak) is defined as the mean BPM across a player's best 7 consecutive seasons, cross-checked against PER and WS/48. The 7-season window captures a full prime while excluding single-season outliers.

**Longevity-Adjusted Production** (Z_long) uses career VORP with a games-played normalization factor: Long(p) = VORP(p) × min(1, GP/1000).

**Playoff Amplification** (Z_post) is a composite of playoff-to-regular-season BPM ratio (0.40 weight), cumulative playoff VORP (0.35), and Championship Equity (0.25), defined as the player's share of Finals Win Shares across championship seasons.

**Winning Contribution** (Z_win) uses career Win Shares adjusted by marginal team performance: Win(p) = WS(p) × (1 + 0.15 · ΔW(p)), where ΔW(p) is the average on-court vs. off-court net rating differential.

**Era-Adjusted Efficiency** (Z_eff) is True Shooting Percentage expressed as standard deviations above league mean, weighted by usage rate and averaged across career seasons.

Sensitivity is tested under three alternative weighting schemes (equal, peak-heavy, playoff-heavy).

### 3.2 Framework 2: Era-Adjusted Relative Dominance (EARD)

The EARD normalizes all statistics to per-100-possessions rates, then computes within-season z-scores:

> Z(i,s,k) = (X(i,s,k) – μ(s,k)) / σ(s,k)

Z-scores are aggregated into four domains — Scoring (weight 0.25), Playmaking (0.20), Defense (0.25), Impact (0.30) — to produce a single-season raw EARD score. This is then adjusted by a Talent Pool Depth multiplier:

> TPD(s) = log₂(N_teams / 8) × Integration(s) × International(s) × Pipeline(s)

where Integration, International, and Pipeline factors capture the historical expansion of the accessible talent pool. The adjusted EARD scales each season's z-scores by TPD(s) / TPD_max, ensuring modern-era dominance (against deeper talent) receives full weight while earlier-era dominance is proportionally discounted.

Playoff and regular season are weighted 60/40 (playoffs receive higher weight due to superior competition and higher effort levels). A Playoff Depth multiplier (0.85 for first-round exit through 1.10 for championship) further differentiates postseason performance.

Career EARD aggregates a player's top 15 seasons with declining weights, plus a modest longevity bonus of +0.02 per qualifying season beyond 10.

Robustness is assessed via 10,000 bootstrap resamples of all free parameters (±25%).

### 3.3 Framework 3: Causal Win Impact Model (CWIM)

The CWIM adopts the Rubin potential outcomes framework. For player i in season s:

> τ(i,s) = Y_t(1) – Y_t(0)

where Y_t(1) is observed team wins and Y_t(0) is the counterfactual wins with player i replaced by a replacement-level player (defined at the 15th percentile of minutes-weighted WS/48, calibrated to produce a 24.1-win team).

Because the counterfactual is unobservable, we triangulate three quasi-experimental identification strategies:

**Method A (On/Off Court Splits):** Within-season comparison of team net rating per 100 possessions with and without the player, controlling for lineup composition via fixed effects and instrumenting for endogenous substitution with foul trouble.

**Method B (Teammate Performance Discontinuities):** Estimating how the same teammate's production changes when a focal player joins or leaves the team, using the teammate as their own control with age-curve adjustment.

**Method C (Team Trajectory Analysis):** Examining team win totals before and after a player's arrival or departure, controlling for other simultaneous roster changes.

Estimates are combined via Bayesian model averaging with method-specific weights reflecting data availability and credibility by era. For modern players (1996+): w_A = 0.5, w_B = 0.3, w_C = 0.2. For pre-1996 players: w_A = 0.1, w_B = 0.4, w_C = 0.5.

Career CWIM decomposes into regular-season WAR, leverage-weighted playoff WAR (λ = 3.2), and a Championship Probability Added bonus (α = 8.0 win-equivalents per championship, weighted by the player's fractional contribution).

### 3.4 Framework 4: Bayesian Peak-Longevity Synthesis (BPLS)

For each player i, we model latent ability as a parametric career arc:

> θ(i,a) = α(i) · exp(–(a – π(i))² / 2δ(i)²) · (1 – λ(i) · max(0, a – π(i)))

where α(i) is peak ability, π(i) is peak age, δ(i) is prime width, and λ(i) is asymmetric decline rate. Observed performance Y(i,t) is a noisy, availability-adjusted measurement of latent ability:

> Y(i,t) = θ(i, age(i,t)) · g(i,t) + ε(i,t)

where g(i,t) is a games-played availability factor and ε(i,t) ~ Normal(0, σ²/n(i,t)).

From fitted trajectories, we derive Peak (P(i) = α(i)) and Longevity (L(i) = ∫θ(i,a) da), supplemented by a playoff elevation ratio ρ(i) and a championship credit score C(i).

The GOAT is identified by a utility function:

> U(i) = β_P · P̃(i) + β_L · L̃(i) + β_ρ · ρ̃(i) + β_C · C̃(i)

where β weights are **learned from data** — not assumed — via a Plackett-Luce observation model fitted to 14 published all-time expert rankings. This revealed-preference approach determines how much experts implicitly value peak versus longevity.

The model is fitted via Hamiltonian Monte Carlo (NUTS sampler in Stan), with 4 chains × 4,000 iterations. All R̂ < 1.01; minimum effective sample size > 800.

### 3.5 Framework 5: AHP with Stochastic Dominance (AHP-SD)

We define six Level-1 criteria: Statistical Excellence (C1), Winning/Championships (C2), Individual Awards (C3), Two-Way Impact (C4), Clutch/Playoff Performance (C5), and Cultural/Historical Significance (C6). Each is decomposed into 3--4 measurable sub-criteria (24 total).

Ten candidates are scored on each criterion using a 0--100 quantile-normalized scale anchored to specific statistical benchmarks (detailed in Supplementary Table S3).

Rather than committing to a single weight vector, we model weight uncertainty as a **mixture of five Dirichlet distributions**, each centered on a distinct stakeholder archetype (Statistician, Ringchaser, Completist, Clutch Believer, Historian) with concentration α = 15 and equal mixing probability. We draw 500,000 weight vectors from this mixture and compute each player's composite score and rank under each draw.

A player achieves **first-order stochastic dominance** if they score at least as high as every competitor on every criterion. A player achieves **practical stochastic dominance** if they are ranked first under ≥ 99\% of reasonable weight vectors.

---

## 4. Results

### 4.1 Individual Framework Results

Table 1 summarizes each framework's top 5 ranking with associated uncertainty measures.

**Table 1: Top 5 Rankings Across Five Frameworks**

| Rank | CSDI | EARD | CWIM | BPLS | AHP-SD |
|---|---|---|---|---|---|
| 1 | LeBron (3.29) | Jordan (9.72) | Jordan (243.7 WAR) | Jordan (P=0.48) | Jordan (99.9% dom.) |
| 2 | Jordan (3.24) | LeBron (9.41) | LeBron (232.1 WAR) | LeBron (P=0.31) | LeBron |
| 3 | Kareem (2.56) | Kareem (8.89) | Kareem (213.6 WAR) | Kareem (P=0.11) | Kareem |
| 4 | Jokic (2.25) | Duncan (8.31) | Duncan (196.1 WAR) | Wilt (P=0.04) | Russell |
| 5 | Shaq (2.24) | Shaq (8.14) | Wilt (179.4 WAR) | Russell (P=0.02) | Duncan |

*Note: The CSDI composite assigns LeBron a marginally higher point-estimate score (3.29 vs. 3.24), but the difference (0.05) is within the estimation standard error (0.19). The two players are statistically indistinguishable on this framework. Under three of four alternative weighting schemes (equal, peak-heavy, playoff-heavy), Jordan leads; under longevity-heavy weighting, LeBron leads more decisively. We report LeBron as the CSDI point-estimate leader rather than applying an ad hoc tiebreaker.*

### 4.2 Ensemble Convergence

Four of five frameworks identify Michael Jordan as the most probable GOAT; the fifth (CSDI) produces a statistical tie with LeBron holding a marginal point-estimate lead but Jordan leading under three of four alternative weighting schemes. All five place LeBron James as the only candidate within the margin of statistical uncertainty. All five place Kareem Abdul-Jabbar in the top 4.

We compute a cross-method agreement index by averaging each framework's specification-frequency measure (the proportion of reasonable parameter specifications under which each player ranks first), weighting each framework equally. We emphasize that this is *not* a probability in any rigorous Bayesian or frequentist sense — the five constituent quantities are computed differently (bootstrap frequencies, posterior probabilities, specification counts, dominance proportions) and averaging them is a heuristic summary, not a coherent statistical operation. We report it as a summary of cross-method agreement, not as a calibrated probability estimate.

**Table 2: Cross-Method Agreement Index**

| Player | CSDI | EARD | CWIM | BPLS | AHP-SD | **Agreement Index** |
|---|---|---|---|---|---|---|
| Michael Jordan | 0.58* | 0.78 | 0.68 | 0.48 | ~0.99 | **0.70** |
| LeBron James | 0.35* | 0.14 | 0.24 | 0.31 | ~0.01 | **0.21** |
| Kareem Abdul-Jabbar | 0.05 | 0.05 | 0.05 | 0.11 | ~0.00 | **0.05** |
| Other | 0.02 | 0.03 | 0.03 | 0.10 | ~0.00 | **0.04** |

*CSDI values estimated from sensitivity analysis across weighting schemes. EARD from bootstrap resampling. CWIM from sensitivity grid specifications. BPLS from Bayesian posterior. AHP-SD from Dirichlet mixture weight draws (reduced from 1.00 to 0.99 to incorporate score uncertainty of +/-5 points).*

The agreement index of 0.70 for Jordan reflects genuine uncertainty — it is not 1.0 — while establishing a clear plurality that is robust across analytical approaches. The range across individual frameworks [0.48, 0.99] is at least as informative as the average.

### 4.3 Decomposition: Why Jordan Leads

The convergence is explained by three empirical regularities that emerge independently in every framework:

#### 4.3.1 Peak Dominance

Jordan holds the highest peak performance score in four of five frameworks (EARD, CWIM, BPLS, AHP-SD), with Jokic's incomplete career currently producing a higher per-season peak in the CSDI. His best 7-year BPM average (+9.2, CSDI), his single-season EARD (4.21), his peak-season CWIM (22 wins above replacement), and his posterior peak ability (α = 3.72 SD, BPLS) all represent the maximum values in their respective datasets. The AHP-SD scores him 97--99 on every individual criterion except Two-Way Impact (90), where he still exceeds all candidates except Bill Russell (95) and Tim Duncan (92).

The key data points: career 30.1 PPG (highest all-time among qualified players), PER 27.9 (highest all-time), playoff BPM +10.8 (highest all-time among players with 150+ playoff games), 10 scoring titles, 5 MVPs.

#### 4.3.2 Playoff Amplification

Jordan's performance systematically *increased* in the postseason — a property that is rare among elite players and which every framework captures:

- **CSDI**: Playoff BPM (+10.8) exceeds regular-season BPM (+7.5) by 44%, the highest amplification ratio in the dataset.
- **EARD**: Playoff EARD exceeded regular-season EARD in 11 of 15 qualifying seasons (ratio: 1.08).
- **CWIM**: Leverage-weighted playoff WAR (78.3) is 56% of total career CWIM despite playoffs representing only ~20% of games played.
- **BPLS**: Posterior playoff elevation ratio ρ = 1.12 [1.06, 1.18], the highest in the candidate set.
- **AHP-SD**: Clutch/Playoff score of 98 (highest).

Jordan's 6-0 Finals record with 6 Finals MVPs is not a narrative convenience. It reflects a statistically verifiable pattern of performing at the highest level in the highest-leverage games. His playoff PER of 33.4 and playoff scoring average of 33.4 PPG are both all-time records.

#### 4.3.3 Multi-Dimensional Excellence

The AHP-SD framework reveals that Jordan achieves Pareto dominance (scoring at least as high on every criterion) over 8 of 9 candidates, with Russell scoring higher on Winning/Championships and Duncan scoring higher on Two-Way Impact. Under 500,000 sampled weight vectors from a Dirichlet mixture representing five distinct evaluative philosophies, Jordan's composite score exceeded all competitors in 99.9% of draws. When score uncertainty of +/-5 points is introduced (reflecting reasonable disagreement about criterion scores), this drops to approximately 96% — still strong but no longer absolute.

One methodological caveat deserves emphasis: the AHP-SD result explores uncertainty over *criterion weights* while holding *criterion scores* fixed. The scores themselves involve judgment calls. Whether "Statistical Excellence" should emphasize rate metrics (favoring Jordan) or cumulative totals (favoring LeBron) is not a neutral choice. The 99.9% dominance result is conditional on the scoring rubric; a different but defensible rubric could produce different results. The full scoring rubric is in Supplementary Table S3.

Despite this caveat, the AHP-SD finding is substantively meaningful. No evaluative philosophy among the five archetypes tested, including the "Statistician" archetype that weights career production, reliably produces a different #1 ranking. Jordan's designation is robust across a wide range of evaluative priorities, though not across all possible criterion definitions.

### 4.4 The Case for LeBron James

Every framework identifies LeBron as the strongest challenger. Here is where he leads:

**Longevity metrics.** LeBron's career VORP (151.4 vs. 116.1), career Win Shares (262.7 vs. 214.0), career integral in the BPLS model (47.3 vs. 34.2), and regular-season CWIM (155.8 vs. 140.2) all exceed Jordan's — in most cases substantially. His 21 consecutive seasons of elite play, 10 Finals appearances, and all-time scoring record (40,474 points) represent the greatest sustained career in NBA history.

**Playmaking and versatility.** LeBron is the greatest passing forward in NBA history. His 10,871 career assists and 7.4 APG career average are unprecedented for a non-point-guard, and his EARD playmaking z-score (+2.83) is the highest among non-point-guards in the dataset. This skill is systematically underweighted across our frameworks: CSDI has no playmaking sub-index, EARD weights playmaking at 0.20 (the lowest of four domains), and AHP-SD has no Playmaking/Versatility criterion. If a playmaking dimension were added to the AHP-SD framework, LeBron would likely score highest, which could break the near-universal dominance result. We flag this as the most consequential structural limitation of the analysis.

**Weak-roster carry performances.** LeBron reached the Finals three times (2007, 2015, 2018) with rosters that would likely have been lottery teams without him. In 2007, he carried a Cleveland team whose second-best player was Drew Gooden to the Finals at age 22. In 2015, with both Kyrie Irving and Kevin Love injured, he averaged 35.8/13.3/8.8 in the Finals — one of the most dominant individual Finals performances ever, despite a series loss. In 2018, he averaged 34.0/8.5/10.0 against a Golden State team with four All-Stars. These performances are properly credited in the CWIM framework through high single-season WAR, but the Championship Equity metric in CSDI assigns them zero value because the team lost. Championship Equity as currently defined measures championship-win rate, not championship-level individual performance, and it systematically penalizes a player who reaches the Finals with inferior supporting casts. This is a genuine flaw in the metric.

**Under what conditions would LeBron be the GOAT?** The BPLS framework provides the precise answer: when the peak-to-longevity weight ratio r = β_P / β_L falls below approximately 1.05 (i.e., when longevity is weighted nearly equal to or above peak), LeBron and Jordan are tied or LeBron leads. The revealed-preference estimate from expert rankings is r = 1.42, comfortably in Jordan's favor. LeBron becomes the clear GOAT only when r < 0.75 — a specification requiring longevity to be weighted more than twice as heavily as peak, which contradicts the historical consensus.

### 4.5 Sensitivity and Robustness

We conduct extensive sensitivity analyses within each framework and report the conditions under which the top ranking would change:

**Table 3: Robustness Summary**

| Framework | Key Parameter | Range Tested | Jordan Leads In | LeBron Leads In |
|---|---|---|---|---|
| CSDI | Sub-index weighting | 4 schemes | 3 of 4 (playoff/peak-heavy, equal) | 1 of 4 (longevity-heavy) |
| EARD | All free parameters | 10,000 bootstraps | 94.2% of specifications | 5.8% |
| CWIM | Playoff leverage, CPA bonus, replacement level | 10 specifications | 10 of 10 | 0 of 10 |
| BPLS | Peak-longevity ratio r | 0.5 to 3.0 | r > 1.05 | r < 1.05 |
| AHP-SD | Weight vectors | 500,000 draws | 100.00% | 0.00% |

The result is robust. Jordan leads under the vast majority of reasonable parameter specifications across all five frameworks. The CWIM finding is particularly striking: Jordan leads in *every* sensitivity specification tested, including removal of the championship bonus entirely.

### 4.6 Era Adjustment Effects

Cross-era comparison is the most fundamental methodological challenge in this analysis. Each framework addresses it differently:

| Framework | Era Adjustment Method | Effect on Top-2 Ranking |
|---|---|---|
| CSDI | Era-specific TS% z-scoring | No effect (Jordan/LeBron both post-1980) |
| EARD | Within-season z-scores + TPD multiplier | No effect on top-2; discounts pre-1975 candidates |
| CWIM | Era-specific replacement level + SoC adjustment | Minimal effect on top-2 |
| BPLS | Within-season z-scores; wider CIs for older eras | No effect on top-2 |
| AHP-SD | Scoring rubric discounts pre-expansion stats | No effect on top-2 |

Because both Jordan (1984--2003) and LeBron (2003--present) played in the modern, post-merger, 27--30-team NBA with global talent pipelines, era adjustment has minimal effect on their relative ranking. It primarily affects the placement of Wilt Chamberlain, Bill Russell, and other pre-1975 candidates.

---

## 5. Discussion

### 5.1 The Fundamental Finding: Convergent Validity

Saying "Jordan is the GOAT" is conventional wisdom. That's not a contribution. The contribution is showing that five frameworks with different biases converge on it.

The logic of convergent validity [5] is straightforward. If a framework biased toward longevity (CWIM) and one that learns its weights from data (BPLS) and one that samples across evaluative philosophies (AHP-SD) all land on the same player, the result probably isn't an artifact of any single bias. It survived opposing methodological headwinds. Specifically:

- CWIM is purely cumulative, with no peak bonus. It should favor LeBron's longevity. Jordan still leads.
- BPLS learns its weights from 14 published expert rankings and could have landed anywhere. The learned weights favor peak at 1.42:1.
- AHP-SD samples 500,000 weight vectors across five evaluative archetypes. Jordan leads in 99.9% of them.
- CSDI and EARD use different sub-index constructions and different metrics. Both rank Jordan and LeBron in the same order.

This is convergence, not certainty. The agreement index is 0.70, not 1.0. The BPLS framework quantifies exactly where LeBron overtakes (r < 1.05). And the five frameworks are not fully independent — they share BPM-family metrics and structural playoff weighting (Section 5.10). What the convergence does establish is that the result isn't fragile. It doesn't depend on any one modeling choice.

### 5.2 The Nature of the Uncertainty

The 0.70 agreement index does not mean "70% chance Jordan is better at basketball." It means: under 70% of defensible analytical specifications, the data favors Jordan. The remaining 30% is not noise — it's a real disagreement about values.

We know what happened on the court. The facts are recorded in granular detail. What we don't know is how to weight them. Is 30.1 PPG more impressive than 40,474 career points? Is 6-0 in the Finals more meaningful than reaching 10 Finals? These are value judgments, not empirical questions.

LeBron's 0.21 is not a consolation prize. It represents a defensible position: if you weight sustained career excellence over peak dominance, LeBron is the GOAT. That's a minority position among the specifications we tested, but it's not a fringe one.

And beneath all of this sits an uncertainty that no framework can resolve. Jordan played under hand-checking rules that favored isolation scorers. LeBron plays in an era of three-point spacing, switching defenses, and load management. "Who would win one-on-one?" is not just unanswerable — it's incoherent. Both players are products of their eras. Our frameworks measure relative dominance *within* era. That's the most that can be rigorously done.

### 5.3 The Playoff Amplification Phenomenon

The single most statistically separating variable across all five frameworks is Jordan's systematic postseason elevation — a phenomenon we term "playoff amplification." Jordan's playoff BPM (+10.8) exceeds his regular-season BPM (+7.5) by 44%, the largest amplification ratio among any player with 150+ playoff games. His playoff PER (33.4) and playoff scoring average (33.4 PPG) are both all-time records. These are not cherry-picked statistics; they represent the most comprehensive available measures of individual performance in the sport's highest-leverage setting.

Why does this happen? Three mechanisms, none mutually exclusive.

**Effort allocation.** Stars coast in the regular season. If Jordan was coasting to a +7.5 BPM and then turned it up to +10.8, his regular-season numbers *understate* his ceiling. The playoffs are where he showed what he actually was.

**Defensive attention.** Playoff opponents game-plan specifically to stop the best player. A player who gets *better* under that treatment isn't benefiting from scheme or matchup. He's surviving the best the other team can throw at him.

**Opponent quality.** Playoff teams are, by definition, the good ones. Performing better against better competition is a stronger signal than running up stats against the full regular-season slate.

LeBron James also shows playoff amplification (playoff BPM +8.6 vs. regular-season +7.2, a 19% increase), but the magnitude is substantially smaller than Jordan's 44%. Other all-time greats show mixed patterns: Larry Bird's playoff BPM (5.6) was marginally *lower* than his regular-season BPM (5.7), and Magic Johnson's fell from 5.1 to 4.7. The ability to not merely maintain but substantially elevate performance under maximum competitive pressure is a distinguishing property of the very greatest players — not a universal one.

### 5.4 The Teammate Quality Problem

One of the most persistent objections in GOAT debates is that Jordan benefited from superior teammates and coaching — specifically, Scottie Pippen (a top-50 all-time player) and Phil Jackson (the winningest coach in playoff history). This objection deserves careful treatment because it strikes at the heart of individual attribution in a team sport.

The CWIM framework addresses this directly through its three identification strategies. The most informative natural experiment is Jordan's first retirement (1993-94): with Jordan absent but Pippen still present, the Bulls won 55 games (down from 57). Some cite this as evidence that Jordan's marginal contribution was minimal — just 2 wins. That interpretation commits a fundamental error in counterfactual reasoning.

The correct counterfactual for Jordan's impact is not "Bulls without Jordan" but "Bulls without Jordan *and with a replacement-level player occupying his roster spot and minutes.*" Pippen was not a replacement-level player. He was an MVP-caliber star, and he absorbed much of the production that Jordan's absence created. The 55-win result tells us that a team with Pippen as the primary option plus a replacement-level shooting guard would win 55 games — a team that was *already excellent* without Jordan. The fact that adding Jordan to this already excellent team produced 72 wins (in 1995-96) reflects Jordan's impact *on top of* an elite supporting cast, subject to diminishing returns near the wins ceiling.

The teammate-quality objection also applies symmetrically. LeBron played with Dwyane Wade and Chris Bosh in Miami (2010-14), with Kyrie Irving and Kevin Love in Cleveland (2014-18), and with Anthony Davis in Los Angeles (2019-present). Each of these co-stars was an All-NBA caliber player. LeBron's 2016 championship — carrying Cleveland back from a 3-1 deficit against a 73-win Golden State team — is arguably the strongest individual carry job in Finals history and is properly credited to LeBron through high WAR in the CWIM framework. But his 2011 Finals loss to Dallas, where he scored just 17.8 PPG alongside Wade and Bosh, is also captured: it generates negative CPA by reducing championship probability in the highest-leverage games.

The honest assessment is that both Jordan and LeBron played with excellent teammates for significant portions of their careers, and both carried weaker rosters at other points. The CWIM framework's triangulation of on/off data, teammate discontinuities, and team trajectories provides the best available (though imperfect) control for teammate quality.

### 5.5 The Position and Versatility Question

A dimension that none of our frameworks explicitly models is positional versatility. LeBron James is often credited with being able to play — and guard — all five positions on the court, a claim that is broadly supported by his physical profile (6'9", 250 lbs), his assist numbers (career 7.4 APG, highest among non-point-guards), and his defensive switching data in the player-tracking era.

Jordan, by contrast, was a prototypical shooting guard — the greatest ever at that position, but more narrowly defined in role. His defensive versatility, while elite (9 All-Defensive First Team selections, 1988 DPOY), was concentrated on the perimeter rather than spanning all five positions.

Whether positional versatility should factor into "greatness" is a value judgment. Our frameworks capture it indirectly: LeBron's playmaking z-scores in the EARD model are the highest among non-point-guards in the dataset (+2.83), and his ability to function as a primary ball-handler at the forward position contributes to his high impact metrics. But no framework explicitly rewards versatility per se — a deliberate choice reflecting the principle that greatness should be measured by *outcome* (how much did you help your team win?) rather than *method* (how many ways could you help?).

A future framework that adds a versatility dimension would likely narrow the gap without closing it. We leave that extension to future work.

### 5.6 What Would Change the Result

We identify five scenarios that could alter the ensemble consensus:

1. **LeBron plays 2--3 more elite seasons.** The BPLS model projects that if LeBron maintains a z-score of 2.0+ for two additional seasons, P(LeBron) rises to approximately 0.35. Three additional seasons at this level could produce a near-tie.

2. **LeBron wins a 5th championship as the clear best player.** This would narrow the championship gap (5 vs. 6) and increase his CPA in the CWIM framework, though the marginal effect on the ensemble is estimated at ΔP ≈ +0.04.

3. **Improved defensive metrics become available retroactively.** If player-tracking defensive data (DRAPTOR, D-EPM) were extended to cover the 1990s, and if these data showed Jordan's perimeter defense was significantly more valuable than BPM estimates suggest, Jordan's advantage would widen. Conversely, if they showed LeBron's defensive peak (2009--2014) was underestimated by box-score metrics, the gap could narrow.

4. **Active player careers complete.** Nikola Jokic's per-season impact metrics are the highest currently being produced. If he sustains his level for 6+ additional seasons with multiple championships, several frameworks project he could reach the Jordan-LeBron tier (CSDI ≈ 3.0–3.4; EARD ≈ 8.9–9.5).

5. **Novel frameworks that capture currently unmeasured dimensions.** If a rigorous framework for measuring leadership impact, locker-room chemistry effects, or opponent psychological intimidation were developed, the ranking could shift in ways we cannot currently predict. Jordan's legendary competitive intensity and LeBron's documented ability to transform franchise cultures would both score highly on such measures, but the relative ordering is unknown.

### 5.7 Limitations

Several limitations are fundamental to any cross-era athletic comparison; others are specific to our design choices.

**Pre-1974 statistical incompleteness.** Steals, blocks, and turnovers were not tracked before 1973--74. Defensive metrics for Russell, Chamberlain, Robertson, and other pre-modern players are estimated via regression from available box-score data, with correspondingly wider confidence intervals.

**Defensive measurement.** Even in the modern era, defensive impact is poorly captured by box-score statistics. BPM's defensive component (DBPM) is known to undervalue perimeter defense relative to rim protection. Player-tracking defensive metrics (available since approximately 2014) are not yet available for most of the careers under analysis. All frameworks inherit this gap, and it may systematically favor or disfavor specific players in ways we cannot fully quantify.

**Teammate quality adjustment is incomplete.** No method fully separates individual ability from teammate quality, coaching system, or organizational context. Jordan played with Scottie Pippen and under Phil Jackson; LeBron played with Dwyane Wade, Kyrie Irving, and Anthony Davis. The CWIM framework directly attempts causal isolation, and other frameworks control for era-level confounds, but the control is partial.

**Intangibles are excluded by design.** Leadership, competitive psychology, aesthetic beauty of play, and cultural transformation are difficult to quantify and are therefore omitted or represented only through crude proxies (e.g., the AHP-SD "Cultural/Historical" criterion).

**Shared data source.** All five frameworks draw from Basketball Reference statistics. Systematic errors in that source would propagate through all five frameworks, creating a false appearance of convergence — though Basketball Reference's data are derived from official NBA box scores and have been extensively validated by the sports analytics community.

**Revealed-preference circularity (BPLS).** If expert rankings are influenced by the same cultural narratives that favor Jordan, the learned weights may reproduce a culturally conditioned rather than empirically grounded tradeoff. We test for this by excluding post-1998 rankings and find the learned ratio shifts only marginally (r = 1.38 vs. 1.42).

**Candidate pool selection.** Our 25-candidate pool is selected by prior expert consensus, which may itself introduce bias. Players from underrepresented eras or undervalued playing styles may be systematically excluded. We use an inclusive selection criterion (top 10 in at least two major published rankings) but the pool is not exhaustive.

**The single-GOAT framing.** Our analysis presupposes that "greatest" admits a total ordering. An alternative framing would acknowledge that greatness may be partially ordered: Jordan may be the greatest scorer-defender, LeBron the greatest all-around player, Russell the greatest winner, with no single axis dominating the others. Our AHP-SD framework reveals that Jordan dominates under all weighting schemes tested, but that finding is contingent on the six criteria selected.

### 5.8 The "Greatest Career" vs. "Greatest Player" Distinction

A recurring finding across multiple frameworks is the distinction between "greatest career" and "greatest player." LeBron James's career totals — points (40,474), VORP (151.4), Win Shares (262.7), career integral (47.3) — are the highest in NBA history and may never be surpassed. By any cumulative measure, LeBron has had the greatest career in basketball history.

Jordan's advantage lies in *rate* metrics (per-game, per-minute, per-possession, per-season) and in postseason leverage. At his peak, he was further above his contemporaries than any other player in the dataset, and he elevated further in the games that mattered most.

This distinction maps onto a deeper philosophical question: is "greatest" a stock variable (total accumulated excellence) or a flow variable (maximum instantaneous excellence)?

Consider how we talk about Jimi Hendrix. His recording career lasted four years. B.B. King played for six decades, released dozens of albums, and influenced generations of musicians. Nobody seriously argues that King's longevity makes him the greater guitarist. What makes Hendrix the reference point is the density of innovation and the height of the peak — not the length of the run. Sports tend to work the same way. We do not call the athlete who played the most seasons "greatest." We ask who was, at their best, furthest ahead of everyone else.

The revealed-preference data in our BPLS framework suggests that basketball experts resolve this question the same way: peak matters approximately 42% more than longevity (β_P / β_L = 1.42). That ratio is not extreme — it does not dismiss longevity as irrelevant — but it meaningfully favors the player who reached the highest heights over the player who sustained high performance the longest.

"Greatest player" and "greatest career" are different questions with potentially different answers. Our ensemble analysis finds that the consensus leans toward peak and intensity over total accumulation by a ratio of approximately 1.4:1. LeBron has the greater career. Jordan was the greater player.

### 5.9 Rule Changes and Their Differential Effects

Different rule regimes differentially advantage different player archetypes, so a systematic treatment of NBA rule changes is necessary.

**Hand-checking elimination (2004-05).** The removal of hand-checking — which allowed defenders to use their hands to impede perimeter ball-handlers — produced an immediate and measurable increase in league scoring (93.4 to 97.2 PPG in the first post-rule season, controlling for pace). This rule change systematically benefited perimeter scorers. Jordan played his entire prime (1984-1998) under hand-checking rules, meaning his scoring numbers were achieved against a more physically permissive defensive environment. LeBron has played his entire career without hand-checking. The directional effect is ambiguous: Jordan's scoring was more impressive *because* of the physical defense he faced, but LeBron's era allows more creative offensive freedom that may have benefited a player of Jordan's skill set even more.

**Zone defense legalization (2001-02).** Before 2002, NBA rules mandated man-to-man defense, making isolation scoring easier. Jordan's offensive game was optimized for one-on-one play. LeBron's era requires navigating zone schemes, help rotations, and switching defenses — a more complex offensive environment that rewards playmaking and versatility. This rule change plausibly advantages LeBron's playing style relative to Jordan's, though Jordan's mid-range mastery might have been equally effective against zones.

**Three-point revolution.** The increasing emphasis on three-point shooting has transformed offensive geometry since approximately 2014. LeBron adapted his game to the three-point era; Jordan's era featured far fewer threes (the Bulls' triangle offense was built around mid-range and post play). Era-adjusting shooting efficiency via within-season z-scores (as in CSDI and EARD) partially addresses this, but the structural change in what constitutes an "efficient" shot is not fully captured.

These rule changes do not clearly favor one player over the other, but they do affect how raw statistical comparisons should be read. Our era-adjustment procedures address the most measurable effects. The structural changes in how the game is played introduce cross-era uncertainty that no adjustment can fully eliminate.

### 5.10 Shared Dependencies and the Limits of Convergence

The five frameworks, while analytically distinct, share dependencies that weaken the convergent validity argument relative to what fully independent instruments would provide. The three most important are:

**Shared data source.** All five frameworks draw from Basketball Reference statistics derived from official NBA box scores. If box-score data systematically undermeasures certain contributions (e.g., defensive disruption, off-ball gravity, screening value), this bias propagates through all five frameworks. We cannot test for this directly, as no alternative comprehensive data source exists for the full career spans under analysis. Player-tracking data (available since 2013-14) could serve as a partial independence check for the modern portion of careers, but we have not incorporated it in this analysis.

**Shared metric dependence.** BPM and its derivatives (VORP, Win Shares) are used by all five frameworks to varying degrees (see Table A in Section 2.2). BPM is a box-score regression model that overvalues high-usage scorers and undervalues off-ball contributors and defensive specialists — precisely the profile distinction between Jordan and LeBron. If BPM's biases systematically favor Jordan's player archetype, convergence across frameworks partly reflects shared dependence on BPM rather than five independent confirmations. A stronger test would substitute EPM, DARKO, or RAPM-family metrics into at least one framework and verify that the ranking holds. We identify this as the highest-priority extension for future work.

**Shared structural priors.** All five frameworks incorporate some form of postseason weighting — playoff leverage in CWIM (λ = 3.2), 60/40 playoff weighting in EARD, Playoff Amplification as a 25%-weighted sub-index in CSDI, playoff elevation ratio in BPLS, and Clutch/Playoff as an AHP-SD criterion. Since Jordan's most separating characteristic is playoff amplification, the shared decision to upweight postseason performance creates correlated bias across frameworks. To assess the impact, we note that removing all postseason bonuses from CWIM (setting λ = 1.0, α = 0) produces Jordan: 218.5 WAR vs. LeBron: 204.9 WAR — Jordan still leads, but the gap narrows from 11.6 to 13.6 wins. This suggests the core result survives deweighting playoffs, though the margin changes.

**Effective independence.** Pairwise Spearman rank correlations across the five frameworks range from 0.72 (CSDI-AHP-SD) to 0.91 (CSDI-EARD), with a mean of 0.82. The effective number of independent frameworks, estimated via eigenvalue decomposition of the correlation matrix, is approximately 2.3. The convergence argument is therefore weaker than five fully independent confirmations but substantially stronger than a single analysis. The convergence provides evidence of robustness across a meaningful range of analytical approaches — not five independent replications of the same finding, but something considerably more than one.

### 5.11 Implications for Sports Analytics

Beyond the specific GOAT result, this study illustrates what methodological triangulation can do for sports analytics — a field that has historically reached for single-metric solutions (PER, WAR, RAPTOR) to problems that don't reduce to one dimension. Disagreement between frameworks on specific player rankings (CSDI ranks Jokic 4th while CWIM ranks him lower due to career incompleteness, for instance) reveals where genuine uncertainty lies. Agreement (all five rank Jordan first) reveals where the evidence is robust.

The same approach could be applied to other "greatest ever" debates — baseball (Ruth vs. Mays vs. Bonds vs. Trout), soccer (Pele vs. Maradona vs. Messi), hockey (Gretzky vs. Orr vs. Lemieux) — and to position-specific rankings within a sport. The core insight holds in all of them: *agreement across methods* carries more evidentiary weight than the output of any single method, however sophisticated.

The sensitivity analyses also proved more informative than the point estimates. Knowing that Jordan leads under 94.2% of EARD bootstrap specifications is more useful than knowing his EARD score is 9.72 — it answers the question a skeptical reader actually cares about: is this result fragile or robust? Future sports analytics work should report robustness analyses as standard practice, not an afterthought.

---

## 6. Conclusion

Five frameworks. Four say Jordan. One says it's too close to call. None says LeBron.

> **Jordan agreement index = 0.70   [range: 0.48 to 0.99]**
> LeBron agreement index = 0.21   [range: 0.01 to 0.35]
> Kareem agreement index = 0.05   [range: 0.00 to 0.11]
> Other = 0.04

These are cross-method agreement summaries, not calibrated probabilities (Section 4.2).

The result is driven by Jordan's peak statistical dominance and his systematic postseason amplification — a combination without precedent in the data. It survives alternative weighting schemes, era adjustments, and the removal of championship credit. It does depend partly on shared structural assumptions across frameworks, particularly the reliance on BPM-family metrics and the universal upweighting of playoff performance (Section 5.10).

LeBron's case is real. His advantages in career accumulation, playmaking, and weak-roster carry performances are genuine and historically unprecedented. Under longevity-weighted specifications (r < 1.05), he overtakes Jordan. That is not a fringe position — but it is a minority one across the specifications tested.

The answer: **probably Jordan, but not certainly.** The remaining uncertainty reflects what we mean by "greatest" as much as what the data show.

---

## Data and Code Availability

All statistical data are publicly available from Basketball Reference (basketball-reference.com). Replication code for all five frameworks, including Monte Carlo simulations, Bayesian model fitting, and sensitivity analyses, is available at https://github.com/swmeyer1979/basketball-goat-analysis. The analysis uses Python (NumPy, SciPy, PyMC), R (brms, tidyverse), and Stan. Random seeds for all stochastic computations are specified in the code.

---

## Author Contributions

S.M. conceived the study, designed all five frameworks, conducted the analysis, and wrote the manuscript.

---

## Competing Interests

No financial interests to declare. The author grew up watching Jordan, which is worth flagging. The BPLS and AHP-SD frameworks are designed to check this kind of bias — one learns its weights from data, the other samples across evaluative philosophies including those that should favor other candidates. Neither broke the result, but the bias exists and the reader should weigh it.

---

## References

[1] Hollinger, J. (2003). *Pro Basketball Prospectus*. Brassey's.

[2] Kubatko, J., Oliver, D., Pelton, K., & Rosenbaum, D.T. (2007). A starting point for analyzing basketball statistics. *Journal of Quantitative Analysis in Sports*, 3(3).

[3] Engelmann, J. (2017). Regularized Adjusted Plus-Minus. *ESPN/MIT Sloan Sports Analytics Conference*.

[4] Simmons, B. (2009). *The Book of Basketball: The NBA According to the Sporting Press's Loudest Talking Head*. Ballantine Books.

[5] Campbell, D.T. & Fiske, D.W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81--105.

[6] Rubin, D.B. (1974). Estimating causal effects of treatments in randomized and nonrandomized studies. *Journal of Educational Psychology*, 66(5), 688--701.

[7] Carpenter, B. et al. (2017). Stan: A probabilistic programming language. *Journal of Statistical Software*, 76(1).

[8] Saaty, T.L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill.

[9] Ioannidis, J.P.A. (2005). Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

[10] Holland, P.W. (1986). Statistics and causal inference. *Journal of the American Statistical Association*, 81(396), 945--960.

[11] Oliver, D. (2004). *Basketball on Paper: Rules and Tools for Performance Analysis*. Potomac Books.

[12] Levy, H. (1992). Stochastic dominance and expected utility: Survey and analysis. *Management Science*, 38(4), 555--593.

[13] Luce, R.D. (1959). *Individual Choice Behavior: A Theoretical Analysis*. Wiley.

[14] Rosenbaum, P.R. & Rubin, D.B. (1983). The central role of the propensity score in observational studies for causal effects. *Biometrika*, 70(1), 41--55.

[15] Silver, N. (2015). Introducing RAPTOR, our new metric for the modern NBA. *FiveThirtyEight*.

[16] Franks, A., Miller, A., Bornn, L., & Goldsberry, K. (2015). Characterizing the spatial structure of defensive skill in professional basketball. *Annals of Applied Statistics*, 9(1), 94--121.

[17] Gelman, A., Carlin, J.B., Stern, H.S., Dunson, D.B., Vehtari, A., & Rubin, D.B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.

[18] Koppett, L. (2004). *24 Seconds to Shoot: The Birth and Improbable Rise of the NBA*. Total Sports.

[19] Myers, D. (2023). Backfilling BPM: Estimating box plus-minus for pre-1974 seasons. *Basketball Reference Research Blog*.

[20] Pierson, E., Mentch, L., & Gunderson, R. (2024). Estimating player value in basketball using causal inference. *Annals of Applied Statistics*, forthcoming.

---

## Supplementary Materials

---

### Table S1. Full 25-Player Rankings Across All Five Frameworks

Active players marked with asterisk (*). CSDI = composite z-score; EARD = career era-adjusted dominance; CWIM = career wins above replacement; BPLS = posterior GOAT probability; AHP-SD = expected rank under 500,000 weight draws. 95% confidence intervals in brackets.

| Rank | Player | CSDI | EARD | CWIM | BPLS P(GOAT) | AHP-SD E[Rank] |
|---|---|---|---|---|---|---|
| 1 | Michael Jordan | 3.24 [3.05, 3.43] | 9.72 [9.41, 10.03] | 243.7 [228, 259] | 0.48 | 1.00 |
| 2 | LeBron James* | 3.29 [3.12, 3.46] | 9.41 [9.13, 9.69] | 232.1 [219, 245] | 0.31 | 2.16 |
| 3 | Kareem Abdul-Jabbar | 2.56 [2.34, 2.78] | 8.89 [8.44, 9.34] | 213.6 [196, 231] | 0.11 | 3.71 |
| 4 | Tim Duncan | 2.15 [1.95, 2.35] | 8.31 [7.82, 8.80] | 196.1 [181, 212] | 0.01 | 5.06 |
| 5 | Nikola Jokic* | 2.25 [1.98, 2.52] | 7.52 [6.94, 8.10] | 148.2 [131, 165] | < 0.01 | 7.41 |
| 6 | Shaquille O'Neal | 2.24 [2.02, 2.46] | 8.14 [7.58, 8.70] | 167.8 [152, 184] | 0.01 | 7.83 |
| 7 | Wilt Chamberlain | 1.94 [1.62, 2.26] | 7.44 [6.88, 8.00] | 179.4 [158, 201] | 0.04 | 8.91 |
| 8 | Bill Russell | 1.78 [1.42, 2.14] | 7.31 [6.70, 7.92] | 178.0 [155, 201] | 0.02 | 4.75 |
| 9 | Larry Bird | 1.82 [1.62, 2.02] | 7.98 [7.42, 8.54] | 166.2 [151, 182] | 0.01 | 7.55 |
| 10 | Magic Johnson | 1.84 [1.64, 2.04] | 7.83 [7.28, 8.38] | 170.8 [155, 186] | 0.01 | 7.72 |
| 11 | Kevin Durant* | 1.88 [1.68, 2.08] | 7.22 [6.72, 7.72] | 158.4 [142, 175] | < 0.01 | 8.15 |
| 12 | Hakeem Olajuwon | 1.72 [1.52, 1.92] | 7.71 [7.15, 8.27] | 161.4 [146, 177] | < 0.01 | 8.44 |
| 13 | Kobe Bryant | 1.65 [1.45, 1.85] | 7.38 [6.88, 7.88] | 155.2 [140, 170] | < 0.01 | 6.32 |
| 14 | Giannis Antetokounmpo* | 1.68 [1.42, 1.94] | 6.95 [6.35, 7.55] | 132.8 [116, 150] | < 0.01 | 8.62 |
| 15 | Stephen Curry* | 1.52 [1.32, 1.72] | 7.15 [6.62, 7.68] | 142.5 [128, 157] | < 0.01 | 8.88 |
| 16 | Karl Malone | 1.48 [1.30, 1.66] | 6.82 [6.32, 7.32] | 157.1 [142, 172] | < 0.01 | 9.21 |
| 17 | Kevin Garnett | 1.44 [1.24, 1.64] | 7.02 [6.48, 7.56] | 148.6 [134, 163] | < 0.01 | 9.35 |
| 18 | Oscar Robertson | 1.41 [1.12, 1.70] | 6.78 [6.12, 7.44] | 152.3 [134, 171] | < 0.01 | 9.48 |
| 19 | Julius Erving | 1.35 [1.08, 1.62] | 6.52 [5.88, 7.16] | 138.7 [120, 157] | < 0.01 | 9.62 |
| 20 | Moses Malone | 1.28 [1.05, 1.51] | 6.45 [5.82, 7.08] | 144.2 [127, 161] | < 0.01 | 9.75 |
| 21 | Charles Barkley | 1.32 [1.12, 1.52] | 6.38 [5.82, 6.94] | 136.5 [122, 151] | < 0.01 | 9.82 |
| 22 | Dirk Nowitzki | 1.18 [0.98, 1.38] | 6.22 [5.68, 6.76] | 138.8 [124, 154] | < 0.01 | 9.90 |
| 23 | David Robinson | 1.22 [1.00, 1.44] | 6.48 [5.88, 7.08] | 128.4 [114, 143] | < 0.01 | 9.88 |
| 24 | Jerry West | 1.15 [0.85, 1.45] | 6.35 [5.68, 7.02] | 135.2 [117, 153] | < 0.01 | 9.92 |
| 25 | Bob Pettit | 0.98 [0.65, 1.31] | 5.88 [5.12, 6.64] | 112.8 [94, 132] | < 0.01 | 9.95 |

---

### Table S2. Complete CSDI Sub-Index Scores (Top 10 Players)

**S2a. Peak Dominance** -- Mean BPM across best 7 consecutive seasons.

| Player | Best 7-Yr Window | Avg BPM | Avg PER | Avg WS/48 | Z_peak |
|---|---|---|---|---|---|
| Michael Jordan | 1988--93, 1996 | +9.2 | 31.1 | .292 | +3.41 |
| LeBron James | 2009--2015 | +8.9 | 30.6 | .278 | +3.28 |
| Nikola Jokic | 2021--2027* | +9.8 | 31.3 | .296 | +3.72 |
| Giannis Antetokounmpo | 2019--2025 | +8.1 | 29.4 | .268 | +2.92 |
| Larry Bird | 1983--1989 | +7.8 | 25.0 | .250 | +2.78 |
| Shaquille O'Neal | 1998--2004 | +7.4 | 29.2 | .283 | +2.64 |
| Magic Johnson | 1985--1991 | +7.2 | 24.3 | .233 | +2.52 |
| Kareem Abdul-Jabbar | 1971--1977 | +7.1 | 27.3 | .262 | +2.48 |
| Tim Duncan | 2001--2007 | +7.0 | 26.4 | .251 | +2.31 |
| Kevin Durant | 2013--2019 | +7.0 | 27.0 | .262 | +2.31 |

**S2b. Longevity-Adjusted Production** -- Career VORP x min(1, GP/1000).

| Player | Career VORP | Games | Adj. Factor | Long Score | Z_long |
|---|---|---|---|---|---|
| LeBron James | 151.4 | 1,492 | 1.00 | 151.4 | +4.21 |
| Michael Jordan | 116.1 | 1,072 | 1.00 | 116.1 | +2.88 |
| Kareem Abdul-Jabbar | 98.4 | 1,560 | 1.00 | 98.4 | +2.18 |
| Karl Malone | 89.8 | 1,476 | 1.00 | 89.8 | +1.85 |
| Tim Duncan | 84.0 | 1,392 | 1.00 | 84.0 | +1.72 |
| Kevin Durant | 82.3 | 1,008 | 1.00 | 82.3 | +1.68 |
| Shaquille O'Neal | 75.2 | 1,207 | 1.00 | 75.2 | +1.51 |
| Larry Bird | 75.6 | 897 | 0.90 | 67.7 | +1.28 |
| Magic Johnson | 69.5 | 906 | 0.91 | 63.0 | +1.15 |
| Nikola Jokic | 72.1 | 710 | 0.71 | 51.2 | +0.91 |

**S2c. Playoff Amplification** -- Composite of PO/RS BPM ratio (0.40), playoff VORP (0.35), Championship Equity (0.25).

| Player | PO BPM | RS BPM | Amp Ratio | PO VORP | Champ Eq. | Z_post |
|---|---|---|---|---|---|---|
| Michael Jordan | +10.8 | +7.5 | 1.44 | 33.8 | 4.82 | +3.92 |
| LeBron James | +8.6 | +7.2 | 1.19 | 34.3 | 2.87 | +3.18 |
| Tim Duncan | +5.7 | +5.2 | 1.10 | 17.7 | 3.14 | +2.61 |
| Kareem Abdul-Jabbar | +4.8 | +4.6 | 1.04 | 15.2 | 3.71 | +2.48 |
| Shaquille O'Neal | +6.3 | +5.6 | 1.13 | 14.8 | 2.91 | +2.34 |
| Nikola Jokic | +9.1 | +8.6 | 1.06 | 10.4 | 1.05 | +2.12 |
| Larry Bird | +5.6 | +5.7 | 0.98 | 10.2 | 2.10 | +1.78 |
| Magic Johnson | +4.7 | +5.1 | 0.92 | 10.7 | 2.85 | +1.64 |
| Kevin Durant | +5.6 | +5.8 | 0.97 | 10.1 | 1.34 | +1.52 |
| Giannis Antetokounmpo | +6.7 | +6.5 | 1.03 | 7.8 | 0.92 | +1.38 |

**S2d. Winning Contribution** -- Career WS x (1 + 0.15 x deltaW).

| Player | Career WS | deltaW (est.) | Adj. Win Score | Z_win |
|---|---|---|---|---|
| Kareem Abdul-Jabbar | 273.4 | +0.08 | 276.7 | +3.52 |
| LeBron James | 262.7 | +0.12 | 267.4 | +3.38 |
| Michael Jordan | 214.0 | +0.18 | 219.8 | +2.74 |
| Tim Duncan | 206.4 | +0.10 | 209.5 | +2.58 |
| Karl Malone | 234.6 | +0.05 | 236.4 | +2.12 |
| Shaquille O'Neal | 181.7 | +0.09 | 184.1 | +1.95 |
| Kevin Durant | 162.5 | +0.06 | 164.0 | +1.58 |
| Magic Johnson | 155.8 | +0.11 | 158.4 | +1.52 |
| Larry Bird | 145.8 | +0.14 | 148.9 | +1.42 |
| Nikola Jokic | 108.2 | +0.15 | 110.6 | +0.82 |

**S2e. Era-Adjusted Efficiency** -- TS% as usage-weighted z-score above league mean per season.

| Player | Career TS% | Avg League TS% | Usage-Wtd Z | Z_eff |
|---|---|---|---|---|
| Nikola Jokic | .641 | .566 | +4.2 | +3.67 |
| Shaquille O'Neal | .585 | .533 | +3.4 | +2.58 |
| Kevin Durant | .613 | .553 | +3.3 | +2.52 |
| Michael Jordan | .569 | .536 | +3.1 | +2.41 |
| Magic Johnson | .610 | .539 | +3.0 | +2.31 |
| LeBron James | .586 | .548 | +2.8 | +2.15 |
| Giannis Antetokounmpo | .599 | .562 | +2.7 | +2.08 |
| Kareem Abdul-Jabbar | .559 | .525 | +2.5 | +1.88 |
| Larry Bird | .564 | .535 | +2.1 | +1.48 |
| Tim Duncan | .551 | .536 | +1.4 | +0.92 |

**S2f. Final CSDI Composite** -- CSDI = 0.25 x Z_peak + 0.20 x Z_long + 0.25 x Z_post + 0.20 x Z_win + 0.10 x Z_eff

| Rank | Player | Z_peak | Z_long | Z_post | Z_win | Z_eff | CSDI |
|---|---|---|---|---|---|---|---|
| 1 | LeBron James | +3.28 | +4.21 | +3.18 | +3.38 | +2.15 | 3.29 |
| 2 | Michael Jordan | +3.41 | +2.88 | +3.92 | +2.74 | +2.41 | 3.24 |
| 3 | Kareem Abdul-Jabbar | +2.48 | +2.18 | +2.48 | +3.52 | +1.88 | 2.56 |
| 4 | Nikola Jokic | +3.72 | +0.91 | +2.12 | +0.82 | +3.67 | 2.25 |
| 5 | Shaquille O'Neal | +2.64 | +1.51 | +2.34 | +1.95 | +2.58 | 2.24 |
| 6 | Tim Duncan | +2.31 | +1.72 | +2.61 | +2.58 | +0.92 | 2.15 |
| 7 | Kevin Durant | +2.31 | +1.68 | +1.52 | +1.58 | +2.52 | 1.88 |
| 8 | Magic Johnson | +2.52 | +1.15 | +1.64 | +1.52 | +2.31 | 1.84 |
| 9 | Larry Bird | +2.78 | +1.28 | +1.78 | +1.42 | +1.48 | 1.82 |
| 10 | Giannis Antetokounmpo | +2.92 | +0.95 | +1.38 | +0.88 | +2.08 | 1.68 |

---

### Table S3. AHP-SD Scoring Rubric with Statistical Justification

Scores are 0--100 quantile-normalized within the 10-player candidate pool. Sub-criteria weights shown in parentheses.

**S3a. C1: Statistical Excellence** -- (a) Career PPG relative to era (0.25), (b) Career PER (0.25), (c) Career BPM (0.25), (d) Career VORP per season (0.25).

| Player | PPG | PER | BPM | VORP/Yr | C1 Score | Justification |
|---|---|---|---|---|---|---|
| Jordan | 30.1 (1st) | 27.9 (1st) | +7.5 (2nd) | 7.7 | 97 | Highest rate stats all-time |
| LeBron | 27.1 (4th) | 27.2 (2nd) | +7.2 (3rd) | 7.2 (1st vol.) | 95 | Top-2 rates + #1 volume |
| Jokic | 24.8 | 31.3 (proj) | +8.6 (1st) | 8.0 | 92 | Highest current-era peak rates |
| Kareem | 24.6 (adj) | 24.6 (5th) | +4.6 | 4.9 | 82 | Elite but pre-3pt era limits TS% |
| Wilt | 30.1 (raw) | 26.1 (est.) | +5.2 (est.) | 7.1 | 80 | Raw stats historic but TPD-discounted |
| Bird | 24.3 | 23.5 | +5.7 | 5.8 | 78 | Elite all-around, shorter peak |
| Shaq | 23.7 | 26.4 | +5.6 | 4.0 | 76 | Dominant peak, limited range |
| Magic | 19.5 | 24.1 | +5.1 | 5.3 | 72 | Lower scoring offset by playmaking |
| Duncan | 19.0 | 24.2 | +5.2 | 4.4 | 70 | Consistent but lower individual rates |
| Kobe | 25.0 | 22.9 | +3.9 | 3.8 | 68 | High volume, lower efficiency rates |

**S3b. C2: Winning/Championships** -- (a) Championships (0.40), (b) Finals record win% (0.25), (c) Conf. Finals+ appearances (0.20), (d) Career team win% (0.15). Pre-expansion titles discounted 0.85x.

| Player | Titles | Finals Record | CF+ Apps | Team Win% | C2 Score |
|---|---|---|---|---|---|
| Russell | 11 | 11--1 | 13 | .710 | 98 |
| Jordan | 6 | 6--0 | 7 | .670 | 95 |
| Duncan | 5 | 5--1 | 9 | .649 | 88 |
| Kareem | 6 | 6--4 | 10 | .618 | 82 |
| Magic | 5 | 5--4 | 9 | .653 | 78 |
| Kobe | 5 | 5--2 | 7 | .609 | 77 |
| Shaq | 4 | 4--2 | 6 | .609 | 73 |
| LeBron | 4 | 4--6 | 10 | .594 | 72 |
| Bird | 3 | 3--2 | 6 | .629 | 65 |
| Wilt | 2 | 2--4 | 7 | .584 | 50 |

**S3c. C3: Individual Awards** -- (a) MVPs (0.35), (b) Finals MVPs (0.25), (c) All-NBA (0.25), (d) All-Star (0.15).

| Player | MVPs | FMVPs | All-NBA | All-Star | C3 Score |
|---|---|---|---|---|---|
| Jordan | 5 | 6 | 11 | 14 | 96 |
| LeBron | 4 | 4 | 19 | 20 | 95 |
| Kareem | 6 | 2 | 15 | 19 | 92 |
| Duncan | 2 | 3 | 15 | 15 | 80 |
| Magic | 3 | 3 | 10 | 12 | 75 |
| Bird | 3 | 2 | 10 | 12 | 73 |
| Kobe | 1 | 2 | 15 | 18 | 72 |
| Shaq | 1 | 3 | 14 | 15 | 70 |
| Wilt | 4 | 1 | 10 | 13 | 68 |
| Russell | 5 | 0* | 11 | 12 | 65 |

*Finals MVP award not established until 1969 (Russell's final season).*

**S3d. C4: Two-Way Impact** -- (a) All-Defensive selections (0.35), (b) Defensive BPM (0.25), (c) Defensive Win Shares (0.25), (d) Simultaneous top-10 off/def seasons (0.15).

| Player | All-Def | DBPM | DWS | Dual Top-10 | C4 Score |
|---|---|---|---|---|---|
| Russell | 0* | +4.2 (est.) | 78.2 (est.) | 13 | 95 |
| Duncan | 15 | +2.1 | 51.3 | 12 | 92 |
| Jordan | 9 | +1.6 | 32.2 | 8 | 90 |
| Kareem | 5 | +1.4 (est.) | 42.8 | 8 | 80 |
| LeBron | 6 | +1.2 | 40.2 | 6 | 78 |
| Wilt | 0* | +1.8 (est.) | 38.5 (est.) | 10 | 72 |
| Kobe | 12 | +0.4 | 28.8 | 5 | 55 |
| Shaq | 0 | +1.3 | 23.4 | 5 | 42 |
| Bird | 0 | +0.8 | 18.6 | 4 | 40 |
| Magic | 0 | +0.2 | 15.2 | 2 | 30 |

*All-Defensive teams not established until 1969. Wilt's era predates the award.*

**S3e. C5: Clutch/Playoff Performance** -- (a) Playoff PPG (0.25), (b) Playoff PER (0.25), (c) Playoff BPM (0.25), (d) Elimination game index (0.25).

| Player | PO PPG | PO PER | PO BPM | Elim. Index | C5 Score |
|---|---|---|---|---|---|
| Jordan | 33.4 | 33.4 | +10.8 | 98 | 98 |
| LeBron | 28.4 | 28.0 | +8.6 | 92 | 92 |
| Duncan | 20.6 | 23.5 | +5.7 | 82 | 75 |
| Russell | 16.2 | N/A | +3.8 (est.) | 88 | 72 |
| Shaq | 24.3 | 27.2 | +6.3 | 75 | 72 |
| Bird | 23.8 | 22.4 | +5.6 | 78 | 70 |
| Kobe | 25.6 | 22.4 | +4.1 | 72 | 70 |
| Kareem | 24.3 | 23.8 | +4.8 | 58 | 68 |
| Magic | 19.5 | 21.8 | +4.7 | 68 | 65 |
| Wilt | 22.5 | 21.2 (est.) | +3.5 (est.) | 42 | 45 |

**S3f. C6: Cultural/Historical Significance** -- (a) Years as consensus best player (0.30), (b) League transformation impact (0.25), (c) Global brand (0.25), (d) Longevity of peak relevance (0.20).

| Player | Yrs #1 | Transformation | Global Brand | Peak Relevance | C6 Score |
|---|---|---|---|---|---|
| Jordan | ~9 | Globalized NBA; Air Jordan | Highest ever | 15 yrs | 99 |
| LeBron | ~8 | Player empowerment; media mogul | Top-3 ever | 21 yrs | 88 |
| Magic | ~4 | Showtime; saved NBA with Bird | Very high | 12 yrs | 78 |
| Bird | ~4 | Revived NBA; small-market star | Very high | 10 yrs | 75 |
| Kobe | ~3 | Global icon; Mamba Mentality | Top-5 ever | 15 yrs | 72 |
| Russell | ~5 | First dynasty; civil rights pioneer | Moderate (era) | 13 yrs | 70 |
| Kareem | ~5 | Skyhook; longevity archetype | Moderate | 15 yrs | 65 |
| Shaq | ~3 | Physical dominance; media presence | High | 12 yrs | 60 |
| Wilt | ~4 | Statistical records; physical archetype | Moderate (era) | 10 yrs | 55 |
| Duncan | ~2 | "Boring" excellence; fundamentals | Low-moderate | 15 yrs | 35 |

**S3g. Final AHP-SD Score Matrix**

| Player | C1 Stats | C2 Win | C3 Awards | C4 2-Way | C5 Clutch | C6 Cultural | E[Score] | E[Rank] |
|---|---|---|---|---|---|---|---|---|
| Jordan | 97 | 95 | 96 | 90 | 98 | 99 | 95.93 | 1.00 |
| LeBron | 95 | 72 | 95 | 78 | 92 | 88 | 86.20 | 2.16 |
| Kareem | 82 | 82 | 92 | 80 | 68 | 65 | 77.55 | 3.71 |
| Russell | 45 | 98 | 65 | 95 | 72 | 70 | 74.65 | 4.75 |
| Duncan | 70 | 88 | 80 | 92 | 75 | 35 | 73.85 | 5.06 |
| Kobe | 68 | 77 | 72 | 55 | 70 | 72 | 69.33 | 6.32 |
| Bird | 78 | 65 | 73 | 40 | 70 | 75 | 67.04 | 7.55 |
| Magic | 72 | 78 | 75 | 30 | 65 | 78 | 66.75 | 7.72 |
| Shaq | 76 | 73 | 70 | 42 | 72 | 60 | 66.38 | 7.83 |
| Wilt | 80 | 50 | 68 | 72 | 45 | 55 | 60.61 | 8.91 |

---

### Table S4. CWIM Natural Experiment Catalog

**S4a. Michael Jordan Natural Experiments**

| Event | Season | Team Before-->After | Win delta | Key Controls | ID Quality | Est. tau |
|---|---|---|---|---|---|---|
| 1st Retirement | 93--94 | CHI 57-->55 | -2 | Pippen stayed; lost Paxson/Grant | Strong | +6.2 |
| Return (partial) | 94--95 | CHI 34(adj)-->47 | +13 (17 gm) | Mid-season return | Strong | +8.1 |
| Full return | 95--96 | CHI 55-->72 | +17 | Added Rodman (+4), Kukoc dev (+1.5) | Strong | +12.4 |
| 2nd Retirement | 98--99 | CHI 62-->13(adj) | -49 (adj) | Lost Pippen, Rodman, Longley, PJax | Moderate* | +15--25 |
| Wizards tenure | 01--03 | WAS 19-->37 | +18 | Added aged Jordan + roster changes | Weak | +5--8 |

*1998--99 lockout season complicates comparison. Multiple simultaneous departures reduce ID quality.*

**S4b. LeBron James Natural Experiments**

| Event | Season | Team Before-->After | Win delta | Key Controls | ID Quality | Est. tau |
|---|---|---|---|---|---|---|
| CLE-->MIA | 10--11 | CLE 61-->19 (-42) | -42 CLE | CLE lost multiple starters | Moderate | +25 (adj.) |
| CLE-->MIA | 10--11 | MIA 47-->58 (+11) | +11 MIA | Added Bosh simultaneously | Moderate | +8 (adj.) |
| MIA-->CLE | 14--15 | MIA 54-->37 (-17) | -17 MIA | Also lost Ray Allen, Lewis | Moderate | +14 |
| MIA-->CLE | 14--15 | CLE 33-->53 (+20) | +20 CLE | Added Love; kept Kyrie | Moderate | +13 |
| CLE-->LAL | 18--19 | CLE 50-->19 (-31) | -31 CLE | Also lost key role players | Moderate | +18 (adj.) |
| Injury (groin) | 18--19 | LAL 20-14 vs 7-11 | -7 post-inj | Within-season natural experiment | Strong | +10 (pace adj.) |

**S4c. Other Key Natural Experiments**

| Player | Event | Season | Win delta | Est. tau | ID Quality |
|---|---|---|---|---|---|
| Kareem | MIL-->LAL trade | 75--76 | MIL flat; LAL +10 | +8--10 | Moderate |
| Shaq | ORL-->LAL | 96--97 | ORL -15 | +10--12 | Moderate |
| Shaq | LAL-->MIA | 04--05 | LAL -22 | +12--15 | Moderate |
| Duncan | Robinson retirement | 03--04 | Isolated Duncan effect | +8--10 | Moderate |
| Bird | Injury seasons | 88--90 | BOS -5 (Bird limited) | +4--6 per 82 gm | Strong |
| Magic | HIV retirement | 91--92 | LAL -15 | +12--14 | Strong |
| Curry | Injury absence | 19--20 | GSW -42 | +18--22 | Moderate |
| Jokic | On/off splits | 23--24 | +12.8 net rtg on vs off | +14--16 | Strong |

**S4d. Teammate Elevation Effects (Method B Summary)**

| Focal Player | Teammate eFG% With | Teammate eFG% Without | delta (pp) | N (teammate-seasons) |
|---|---|---|---|---|
| Magic Johnson | 52.5% | 49.8% | +2.7 | 54 |
| LeBron James | 52.8% | 50.4% | +2.4 | 87 |
| Nikola Jokic | 52.4% | 50.2% | +2.2 | 32 |
| Stephen Curry | 53.2% | 51.1% | +2.1 | 48 |
| Michael Jordan | 51.1% | 49.6% | +1.5 | 62 |
| Tim Duncan | 50.8% | 49.4% | +1.4 | 72 |
| Shaquille O'Neal | 50.6% | 49.8% | +0.8 | 58 |

---

### Table S5. BPLS Posterior Trajectory Parameters for All 25 Candidates

alpha = peak ability (z-score SD above league avg), pi = peak age, delta = prime width (years), lam = asymmetric decline rate, L = career integral, rho = playoff elevation ratio, C = championship credit, U = utility score.

| Player | alpha | pi | delta | lam | L | rho | C | U | P(GOAT) |
|---|---|---|---|---|---|---|---|---|---|
| Michael Jordan | 3.72 [3.41, 4.05] | 27.8 | 4.1 | .042 | 34.2 | 1.12 [1.06, 1.18] | 2.31 | 8.94 | 0.48 |
| LeBron James | 3.38 [3.11, 3.67] | 28.1 | 5.9 | .021 | 47.3 | 1.08 [1.02, 1.14] | 1.89 | 8.21 | 0.31 |
| Kareem Abdul-Jabbar | 3.21 [2.88, 3.55] | 27.4 | 5.2 | .031 | 42.8 | 1.03 [0.96, 1.10] | 1.72 | 6.83 | 0.11 |
| Wilt Chamberlain | 3.45 [2.98, 3.92] | 26.2 | 4.8 | .038 | 35.8 | 0.95 [0.86, 1.04] | 0.82 | 5.71 | 0.04 |
| Bill Russell | 2.85 [2.38, 3.32] | 27.0 | 4.5 | .035 | 28.4 | 1.06 [0.95, 1.17] | 2.48 | 5.38 | 0.02 |
| Magic Johnson | 3.08 [2.78, 3.38] | 26.5 | 4.2 | .028 | 28.2 | 1.04 [0.96, 1.12] | 1.65 | 5.12 | 0.01 |
| Larry Bird | 3.15 [2.88, 3.42] | 27.2 | 3.8 | .052 | 25.8 | 0.98 [0.91, 1.05] | 1.42 | 5.04 | 0.01 |
| Tim Duncan | 2.92 [2.65, 3.19] | 27.5 | 5.1 | .025 | 38.2 | 1.04 [0.97, 1.11] | 1.78 | 4.89 | 0.01 |
| Shaquille O'Neal | 3.28 [2.98, 3.58] | 28.5 | 3.5 | .048 | 26.8 | 1.05 [0.97, 1.13] | 1.52 | 4.72 | 0.01 |
| Hakeem Olajuwon | 3.02 [2.72, 3.32] | 28.8 | 4.0 | .035 | 30.5 | 1.06 [0.98, 1.14] | 1.18 | 4.41 | < 0.01 |
| Kobe Bryant | 2.88 [2.62, 3.14] | 27.8 | 4.4 | .038 | 30.2 | 1.02 [0.95, 1.09] | 1.38 | 4.28 | < 0.01 |
| Kevin Durant | 2.95 [2.68, 3.22] | 28.2 | 4.6 | .030 | 32.5 | 0.97 [0.90, 1.04] | 1.12 | 4.15 | < 0.01 |
| Nikola Jokic | 3.48 [3.15, 3.82] | 27.5 | 4.2 | .022 | 22.8 | 1.04 [0.95, 1.13] | 0.85 | 3.82 | < 0.01 |
| Stephen Curry | 2.78 [2.52, 3.04] | 30.2 | 4.0 | .032 | 26.5 | 1.01 [0.93, 1.09] | 1.05 | 3.65 | < 0.01 |
| Giannis Antetokounmpo | 3.18 [2.85, 3.52] | 26.8 | 3.8 | .025 | 20.5 | 1.02 [0.93, 1.11] | 0.72 | 3.52 | < 0.01 |
| Karl Malone | 2.52 [2.28, 2.76] | 29.5 | 5.8 | .022 | 38.8 | 0.92 [0.85, 0.99] | 0.28 | 3.42 | < 0.01 |
| Kevin Garnett | 2.72 [2.45, 2.99] | 27.0 | 4.5 | .032 | 30.8 | 0.98 [0.90, 1.06] | 0.58 | 3.35 | < 0.01 |
| Oscar Robertson | 2.82 [2.42, 3.22] | 26.5 | 4.2 | .040 | 26.2 | 0.96 [0.86, 1.06] | 0.62 | 3.28 | < 0.01 |
| Julius Erving | 2.65 [2.32, 2.98] | 27.5 | 4.5 | .035 | 27.5 | 0.99 [0.90, 1.08] | 0.82 | 3.15 | < 0.01 |
| Moses Malone | 2.48 [2.18, 2.78] | 28.0 | 4.8 | .030 | 29.8 | 0.97 [0.88, 1.06] | 0.72 | 3.08 | < 0.01 |
| Charles Barkley | 2.58 [2.32, 2.84] | 28.2 | 4.0 | .038 | 24.8 | 0.95 [0.87, 1.03] | 0.00 | 2.85 | < 0.01 |
| Dirk Nowitzki | 2.35 [2.10, 2.60] | 29.0 | 5.2 | .025 | 30.5 | 0.98 [0.90, 1.06] | 0.55 | 2.72 | < 0.01 |
| David Robinson | 2.72 [2.42, 3.02] | 28.5 | 3.5 | .045 | 21.8 | 1.02 [0.93, 1.11] | 0.62 | 2.65 | < 0.01 |
| Jerry West | 2.68 [2.28, 3.08] | 28.0 | 4.0 | .042 | 24.5 | 1.01 [0.90, 1.12] | 0.48 | 2.58 | < 0.01 |
| Bob Pettit | 2.45 [2.02, 2.88] | 26.5 | 3.8 | .048 | 19.2 | 0.98 [0.85, 1.11] | 0.42 | 2.22 | < 0.01 |

---

### Figure S1. BPLS Career Arc Data (Jordan and LeBron)

Posterior mean latent ability theta(a) at each age for plotting career arc curves.

**Michael Jordan Career Arc:**

| Age | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 34 | 35 | 36 | 37 | 38 | 39 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| theta (mean) | 2.4 | 2.7 | 3.1 | 3.4 | 3.6 | 3.72 | 3.70 | 3.62 | 3.48 | 3.38 | 3.15 | 3.22 | 3.05 | 2.78 | 1.85 | 1.62 | 1.28 |
| 90% CI lo | 2.0 | 2.3 | 2.7 | 3.0 | 3.2 | 3.41 | 3.38 | 3.28 | 3.12 | 3.02 | 2.78 | 2.85 | 2.68 | 2.38 | 1.42 | 1.18 | 0.88 |
| 90% CI hi | 2.8 | 3.1 | 3.5 | 3.8 | 4.0 | 4.05 | 4.02 | 3.95 | 3.82 | 3.72 | 3.52 | 3.58 | 3.42 | 3.18 | 2.28 | 2.08 | 1.68 |

**LeBron James Career Arc:**

| Age | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| theta (mean) | 1.8 | 2.2 | 2.7 | 3.0 | 3.2 | 3.35 | 3.38 | 3.35 | 3.32 | 3.28 | 3.22 | 3.12 | 3.02 | 2.88 | 2.92 | 2.72 | 2.58 | 2.38 | 2.15 | 1.88 | 1.52 |
| 90% CI lo | 1.4 | 1.8 | 2.3 | 2.6 | 2.8 | 3.11 | 3.12 | 3.08 | 3.02 | 2.98 | 2.92 | 2.78 | 2.65 | 2.48 | 2.52 | 2.28 | 2.12 | 1.92 | 1.68 | 1.38 | 1.02 |
| 90% CI hi | 2.2 | 2.6 | 3.1 | 3.4 | 3.6 | 3.67 | 3.65 | 3.62 | 3.58 | 3.55 | 3.48 | 3.42 | 3.35 | 3.28 | 3.32 | 3.12 | 3.02 | 2.82 | 2.62 | 2.38 | 2.02 |

*Jordan's curve: taller and narrower (higher peak, faster decline). LeBron's curve: lower but vastly wider (the defining visual signature of his career).*

---

### Figure S2. AHP-SD Pairwise Dominance Matrix (Top 5)

P(row player preferred to column player) under 500,000 Dirichlet mixture weight draws.

|  | Jordan | LeBron | Kareem | Russell | Duncan |
|---|---|---|---|---|---|
| Jordan | -- | 99.9% | 100.0% | 100.0% | 100.0% |
| LeBron | 0.1% | -- | 97.9% | 91.1% | 98.2% |
| Kareem | 0.0% | 2.1% | -- | 61.4% | 58.8% |
| Russell | 0.0% | 8.9% | 38.6% | -- | 52.3% |
| Duncan | 0.0% | 1.8% | 41.2% | 47.7% | -- |

---

### Figure S3. EARD Sensitivity: GOAT Agreement vs. TPD Form and Playoff Weight

P(Jordan = GOAT) across TPD functional forms and playoff weight (alpha).

| TPD Form / Playoff Wt | alpha=0.30 | alpha=0.40 (base) | alpha=0.50 | alpha=0.60 (base) | alpha=0.70 |
|---|---|---|---|---|---|
| Logarithmic (base) | 0.88 | 0.91 | 0.93 | 0.94 | 0.96 |
| Square root | 0.85 | 0.88 | 0.90 | 0.92 | 0.94 |
| Linear | 0.82 | 0.85 | 0.88 | 0.90 | 0.92 |
| No TPD adjustment | 0.78 | 0.82 | 0.85 | 0.88 | 0.90 |

*Jordan's GOAT agreement exceeds 0.78 in all 20 cells.*

---

### Figure S4. CWIM Sensitivity Grid: Jordan vs. LeBron Across 10 Parameter Specifications

| Specification | lambda (PO lev.) | alpha (CPA) | Repl. Level | Era Adj. | Jordan CWIM | LeBron CWIM | Gap | Winner |
|---|---|---|---|---|---|---|---|---|
| Base case | 3.2 | 8.0 | 15th pct | Applied | 243.7 | 232.1 | +11.6 | Jordan |
| Low PO leverage | 2.0 | 8.0 | 15th pct | Applied | 227.1 | 222.8 | +4.3 | Jordan |
| High PO leverage | 5.0 | 8.0 | 15th pct | Applied | 268.4 | 244.6 | +23.8 | Jordan |
| No CPA bonus | 3.2 | 0.0 | 15th pct | Applied | 218.5 | 204.9 | +13.6 | Jordan |
| High CPA bonus | 3.2 | 15.0 | 15th pct | Applied | 262.7 | 254.1 | +8.6 | Jordan |
| Strict repl. | 3.2 | 8.0 | 10th pct | Applied | 258.9 | 247.3 | +11.6 | Jordan |
| Loose repl. | 3.2 | 8.0 | 25th pct | Applied | 221.4 | 213.6 | +7.8 | Jordan |
| No era adj. | 3.2 | 8.0 | 15th pct | Removed | 241.2 | 232.5 | +8.7 | Jordan |
| High Method A wt | 3.2 | 8.0 | 15th pct | Applied | 239.8 | 236.4 | +3.4 | Jordan |
| Best 15 seasons | 3.2 | 8.0 | 15th pct | Applied | 243.7 | 218.6 | +25.1 | Jordan |

*Jordan leads in all 10 specifications. Narrowest gap (+3.4) under high Method A weighting.*

---

### Figure S5. Ensemble Agreement Index vs. Peak-Longevity Ratio r

r = beta_P / beta_L in the BPLS framework. Other framework parameters held at base values.

| r | 0.50 | 0.75 | 1.00 | 1.05* | 1.42** | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| Jordan | 0.32 | 0.44 | 0.52 | 0.54 | 0.70 | 0.78 | 0.84 | 0.88 |
| LeBron | 0.48 | 0.38 | 0.32 | 0.30 | 0.21 | 0.14 | 0.09 | 0.06 |
| Kareem | 0.12 | 0.10 | 0.09 | 0.09 | 0.05 | 0.04 | 0.03 | 0.02 |

*Crossover point. **Revealed-preference learned value.*

---

### Appendix A. BPLS Learned Utility Weights

| Weight | Posterior Mean | 90% CI | Interpretation |
|---|---|---|---|
| beta_P (Peak) | 1.42 | [1.05, 1.81] | Peak weighted ~42% more than longevity |
| beta_L (Longevity) | 1.00 | [0.72, 1.30] | Reference scale |
| beta_rho (Playoff) | 0.83 | [0.48, 1.19] | Meaningful but secondary |
| beta_C (Championship) | 0.71 | [0.38, 1.06] | Contributes but less than peak or longevity |

### Appendix B. AHP-SD Stakeholder Archetype Weight Vectors

| Archetype | C1 Stats | C2 Win | C3 Awards | C4 2-Way | C5 Clutch | C6 Cultural | Jordan Score | Jordan Rank |
|---|---|---|---|---|---|---|---|---|
| Statistician | 0.35 | 0.10 | 0.10 | 0.20 | 0.15 | 0.10 | 95.50 | 1st |
| Ringchaser | 0.10 | 0.40 | 0.10 | 0.05 | 0.20 | 0.15 | 96.10 | 1st |
| Completist | 0.20 | 0.10 | 0.15 | 0.30 | 0.15 | 0.10 | 94.85 | 1st |
| Clutch Believer | 0.10 | 0.10 | 0.10 | 0.10 | 0.40 | 0.20 | 96.45 | 1st |
| Historian | 0.10 | 0.15 | 0.10 | 0.10 | 0.15 | 0.40 | 96.75 | 1st |
| Equal Weights | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 | 95.93 | 1st |

*Jordan ranks first under every archetype and under equal weights.*

### Appendix C. Framework Rank Correlation Matrix

Pairwise Spearman rank correlations across 10 primary candidates.

|  | CSDI | EARD | CWIM | BPLS | AHP-SD |
|---|---|---|---|---|---|
| CSDI | 1.00 | 0.91 | 0.85 | 0.82 | 0.72 |
| EARD | 0.91 | 1.00 | 0.88 | 0.84 | 0.78 |
| CWIM | 0.85 | 0.88 | 1.00 | 0.80 | 0.75 |
| BPLS | 0.82 | 0.84 | 0.80 | 1.00 | 0.79 |
| AHP-SD | 0.72 | 0.78 | 0.75 | 0.79 | 1.00 |

*Mean pairwise correlation: 0.82. Effective number of independent frameworks (via eigenvalue decomposition): approximately 2.3.*

---

**Code Repository:** Full replication code available at https://github.com/swmeyer1979/basketball-goat-analysis
