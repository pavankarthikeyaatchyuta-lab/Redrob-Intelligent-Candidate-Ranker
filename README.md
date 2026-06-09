# Redrob Senior AI Engineer Ranker

This repo contains a CPU-only ranking pipeline for the Redrob Intelligent Candidate Discovery & Ranking Challenge. The system is optimized for leaderboard performance under the challenge constraints: `100,000` candidates, `<=5 minutes`, `<=16GB RAM`, and no network calls during ranking.

## What This Ranker Optimizes For

The JD is not asking for generic AI keyword matching. It is implicitly looking for candidates who:

- have shipped retrieval, ranking, recommendation, or matching systems in production
- can operate as product-minded AI engineers rather than pure researchers
- still write code and own delivery end-to-end
- are realistic to hire: active, responsive, reachable, and reasonably available
- are likely to succeed in a fast-moving India-based startup context

The pipeline therefore weights `career evidence` more heavily than raw skill keywords, and uses behavioral signals as a multiplicative availability modifier rather than letting popularity dominate fit.

## Project Structure

```text
.
|-- analysis/
|   `-- dataset_profile.md
|-- scripts/
|   `-- profile_dataset.py
|-- src/
|   `-- redrob_ranker/
|       |-- __init__.py
|       |-- config.py
|       `-- pipeline.py
|-- candidate_schema.json
|-- candidates.jsonl
|-- job_description.docx
|-- rank.py
|-- ranked_candidates.csv
|-- README.md
|-- requirements.txt
|-- submission_spec.docx
`-- validate_submission.py
```

## Ranking Pipeline

### Stage 1. Hard Filters And Sanity Checks

- weaken candidates with very low direct relevance
- penalize consulting-only backgrounds
- penalize pure research profiles without production signals
- penalize outside-India profiles that are not willing to relocate
- down-weight candidates far outside the preferred experience band

### Stage 2. Candidate Feature Extraction

The ranker extracts structured features from:

- `career_history`
- `skills`
- `education`
- `profile headline + summary`
- `Redrob behavioral signals`

### Stage 3. Semantic Relevance Scoring

Explicit scores are computed for:

- retrieval/search relevance
- ranking-system relevance
- recommendation-system relevance
- ranking-evaluation relevance
- Python stack strength
- LLM stack relevance

Career-history evidence is weighted above skill-list evidence to avoid keyword-stuffer traps.

### Stage 4. Behavioral Scoring

Behavioral scoring combines:

- candidate responsiveness
- recruiter attractiveness
- activity recency
- logistics fit

Signals include response rate, response time, notice period, recent activity, recruiter saves, search appearances, views, GitHub activity, verification, and relocation/work-mode preference.

### Stage 5. Career Evidence Scoring

Explicit scores are computed for:

- production ML experience
- startup/product fit
- ownership/impact evidence
- recent hands-on engineering
- title fit
- experience-band fit
- relevant-role depth
- tenure stability

### Stage 6. Honeypot Detection And Penalties

The ranker applies penalties for:

- impossible timelines
- unrealistic advanced/expert skill durations
- title-to-skill mismatches
- suspiciously perfect junior profiles
- seniority contradictions
- CV/speech-heavy profiles without retrieval/ranking evidence
- inactive low-response candidates

### Stage 7. Final Weighted Ranking

The final score is:

`stage1_gate * (semantic + career weighted core) * behavioral_multiplier * (1 - honeypot_penalty)`

Weighting choice:

- semantic fit is highest because the hidden ground truth is likely dominated by real retrieval/ranking relevance
- career evidence is close behind because the JD explicitly warns against skill-list-only matching
- behavior is multiplicative because availability should down-rank but not rescue weak technical fit
- honeypot penalties are strong to protect against Stage 3 disqualification

## Runtime Characteristics

- single-pass scoring over `candidates.jsonl`
- bounded heap to keep only the top-scoring candidates in memory
- standard-library only runtime

On this machine, the full ranking run completed in about `78 seconds`.

## How To Run

```bash
python rank.py --candidates candidates.jsonl --out ranked_candidates.csv
python validate_submission.py ranked_candidates.csv
```

To regenerate the profiling report:

```bash
python scripts/profile_dataset.py
```

## Notes On Weight Inference

Weights were inferred from:

- the JD’s repeated emphasis on `retrieval + ranking + matching + eval`
- the explicit warning against `keyword matching`
- the warning against `recent LangChain/OpenAI-only experience`
- the preference for `product-minded shippers`
- the behavioral-signal document’s claim that availability can be more predictive than static profile quality

## Submission Readiness

- `ranked_candidates.csv` is produced end-to-end by code
- output format is validator-compatible
- no external APIs or GPU dependencies are used
