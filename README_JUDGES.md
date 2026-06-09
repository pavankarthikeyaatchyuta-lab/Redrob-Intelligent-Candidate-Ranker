# Redrob Candidate Ranking System

This repository contains an explainable candidate ranking system built for the Redrob Intelligent Candidate Discovery challenge.

## What It Does

The system ranks 100,000 candidates for a senior AI engineering role by combining:

- semantic understanding of the JD
- career evidence from job history
- behavioral signals from the Redrob platform
- honeypot detection and penalties
- recruiter-readable explanations for every top candidate

## Why This Is Better Than Keyword Matching

Keyword matching can tell you that a candidate mentioned `Pinecone` or `RAG`. It cannot tell you whether they built a real ranking system, shipped it, evaluated it, or used it in production. Our system uses the full profile context, not just skill keywords.

## How To Run

```bash
python rank.py --candidates candidates.jsonl --out ranked_candidates.csv --explainability-report explainability_report.md
python validate_submission.py ranked_candidates.csv
```

## Output Files

- `ranked_candidates.csv`
- `explainability_report.md`
- `analysis/evaluation/evaluation_report.md`
- `analysis/evaluation/figures/*.svg`
- `analysis/evaluation/tables/*.csv`
- `analysis/evaluation/cases/*.md`

## Design Highlights

- CPU only
- No network calls during ranking
- Single-pass scoring over the full pool
- Bounded memory with top-K retention
- Traceable score breakdowns
- Recruiter-style explanations

## Why The System Should Score Well

- It prioritizes the actual JD intent: retrieval, ranking, recommendation, and production ML
- It down-ranks keyword-stuffed non-fits
- It integrates behavioral signals as hireability modifiers
- It avoids honeypot traps through timeline and consistency checks
- It is explainable enough for manual review and interview defense

## Evidence Pack

The repository now includes an evaluation pack that compares the hybrid system against:

- keyword matching
- BM25
- skills-only scoring
- semantic-only scoring

It also includes ablation evidence for:

- removing behavioral signals
- removing career evidence
- removing honeypot detection
- removing semantic scoring

And five recruiter-style case studies that compare a high-ranked candidate against a lower-ranked nearby candidate.
