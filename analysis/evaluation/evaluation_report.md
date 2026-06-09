# Evaluation Report

This report compares the current hybrid system against four baselines and several ablations. It is intentionally evidence-driven, not claim-driven.

## Baseline Comparison

| Ranker | Avg Retrieval | Avg Ranking | Avg Behavioral | Avg Career | Avg Response Rate | Avg Notice Days |
|---|---:|---:|---:|---:|---:|---:|
| Keyword matching | 0.419 | 0.227 | 0.600 | 0.588 | 0.562 | 68.2 |
| BM25 | 0.546 | 0.401 | 0.776 | 0.827 | 0.658 | 56.4 |
| Skills only | 0.314 | 0.107 | 0.489 | 0.439 | 0.469 | 80.1 |
| Semantic only | 0.643 | 0.407 | 0.775 | 0.839 | 0.648 | 57.5 |
| Hybrid system | 0.609 | 0.400 | 0.791 | 0.851 | 0.675 | 59.5 |

### Interpretation

- Pure keyword matching and skills-only scoring are weak at distinguishing actual search/ranking builders from keyword-stuffed candidates.
- BM25 is better than raw keyword counting but still over-rewards lexical similarity without understanding career evidence or behavior.
- Semantic-only ranking is stronger, but it still misses hireability and honeypot resistance.
- The hybrid system is strongest because it combines relevance, evidence, and availability signals in one shortlist.

## Ablation Study

| Mode | Avg Retrieval | Avg Ranking | Avg Behavioral | Avg Career | Avg Response Rate | Avg Notice Days | Overlap with Full Top-100 |
|---|---:|---:|---:|---:|---:|---:|---:|
| full | 0.609 | 0.400 | 0.791 | 0.851 | 0.675 | 59.5 | 100 |
| no_behavior | 0.614 | 0.395 | 0.767 | 0.853 | 0.637 | 59.5 | 90 |
| no_career | 0.632 | 0.402 | 0.777 | 0.843 | 0.646 | 58.2 | 91 |
| no_honeypot | 0.609 | 0.400 | 0.791 | 0.851 | 0.675 | 59.5 | 100 |
| no_semantic | 0.496 | 0.371 | 0.819 | 0.860 | 0.725 | 60.6 | 69 |

### Ablation Interpretation

- Removing behavioral signals lowers recruiter readiness and raises long-notice, lower-engagement candidates.
- Removing career evidence makes the shortlist more keyword-driven and less product/production grounded.
- Removing semantic scoring destroys direct JD fit and shifts the shortlist toward generic engineering profiles.
- Removing honeypot detection increases risk because synthetic-looking candidates move upward.

## Ranking Quality Analysis

- Hybrid top-100 mean retrieval relevance: 0.609
- Hybrid top-100 mean ranking relevance: 0.400
- Hybrid top-100 mean behavioral score: 0.791
- Hybrid top-100 mean career evidence score: 0.851
- Hybrid top-100 mean response rate: 0.675
- Hybrid top-100 mean notice period: 59.5

## Top Candidate Archetypes

- Applied ML Engineer: 15
- Recommendation Systems Engineer: 15
- Machine Learning Engineer: 11
- AI Engineer: 10
- Search Engineer: 10
- Senior Data Scientist: 9
- NLP Engineer: 9
- Senior NLP Engineer: 6
- Staff Machine Learning Engineer: 4
- Senior Machine Learning Engineer: 3

## Failure Cases

- Keyword matching still promotes profiles with surface-term overlap and weak career evidence.
- Skills-only ranking ignores whether the candidate actually shipped production systems.
- Semantic-only ranking can be too forgiving toward inactive or hard-to-hire candidates.
- BM25 can be fooled by dense lexical overlap from non-relevant profiles.

## Why The Hybrid System Is Stronger

- It uses semantic fit to find the right kind of work.
- It uses career evidence to confirm the work was real.
- It uses behavioral signals to determine whether the candidate is realistically hireable.
- It uses honeypot penalties to suppress fake or inconsistent profiles.

## PPT-Ready Figures

- figures/baseline_relevance.svg
- figures/baseline_behavior_career.svg
- figures/hybrid_score_distribution.svg
- figures/semantic_score_distribution.svg
- figures/behavioral_score_distribution.svg
- figures/career_score_distribution.svg

## PPT-Ready Tables

- tables/baseline_comparison.csv
- tables/ablation_comparison.csv

## Case Study Slides

- cases/case_1.md
- cases/case_2.md
- cases/case_3.md
- cases/case_4.md
- cases/case_5.md
