# Strategy Report

## Hidden Recruiter Intent

- Rank for a `founding-team Senior AI Engineer`, not a generic AI candidate.
- Prioritize people who have already shipped `retrieval`, `ranking`, `recommendation`, or `matching` systems to real users.
- Prefer `product-minded builders` over pure researchers or framework demo builders.
- Favor candidates who are `actually hireable now`: active, responsive, reachable, and not blocked by long notice periods or relocation friction.
- Avoid keyword-stuffed profiles even when the skills section looks perfect.

## Strongest Positive Signals

- Current or recent titles such as `Machine Learning Engineer`, `Search Engineer`, `Recommendation Systems Engineer`, `AI Engineer`, `Applied ML Engineer`, `NLP Engineer`, `Data Scientist`, and strong adjacent engineering titles with IR evidence.
- Career-history descriptions mentioning:
  - `BM25`, `dense retrieval`, `semantic search`, `FAISS`, `Pinecone`, `Qdrant`, `Weaviate`, `Milvus`, `OpenSearch`, `Elasticsearch`
  - `learning to rank`, `ranking`, `re-ranking`, `recommendation`, `matching`
  - `NDCG`, `MRR`, `MAP`, `A/B testing`, `offline evaluation`, `relevance metrics`
  - `production`, `deployed`, `shipped`, `latency`, `scale`, `real users`
- Experience near the JD sweet spot: roughly `5-9 years`, especially `6-8`.
- Product or marketplace context, especially `consumer`, `marketplace`, `fintech`, `SaaS`, `recruiting`, `HR tech`, `e-commerce`.
- Strong behavioral signals: `recent activity`, `good recruiter response rate`, `reasonable notice period`, `saved-by-recruiters`, `search appearances`, `GitHub activity`.
- India-based candidates in or near `Pune`, `Noida`, `Delhi NCR`, `Bangalore`, `Mumbai`, `Hyderabad`, or willing to relocate there.

## Strongest Negative Signals

- Non-technical current titles with AI-heavy skill lists but no corresponding career evidence.
- Consulting-only careers with little product-system ownership.
- Pure research signals without production deployment.
- Computer-vision or speech-only specialization without NLP/IR/search/ranking evidence.
- Architecture-only or management-heavy recent roles with weak hands-on coding evidence.
- Low response rate, stale activity, very long notice period, or non-relocatable overseas profiles.
- LLM/RAG profiles that look like wrappers or chatbots rather than retrieval/ranking systems.

## Likely Honeypot Characteristics

- Impossible timeline math between `start_date`, `end_date`, and `duration_months`.
- Many `advanced` or `expert` skills with almost no `duration_months`.
- Non-technical titles paired with suspiciously dense retrieval/ranking skill lists.
- Suspiciously perfect behavioral profiles for very junior candidates.
- Seniority labels that do not match years of experience.
- CV/speech-heavy profiles disguised as search/ranking candidates.

## Behavioral Signals That Should Heavily Influence Ranking

- `recruiter_response_rate`
- `avg_response_time_hours`
- `last_active_date`
- `open_to_work_flag`
- `notice_period_days`
- `interview_completion_rate`
- `saved_by_recruiters_30d`
- `search_appearance_30d`
- `profile_views_received_30d`
- `github_activity_score`

Behavior should be a multiplier, not the core ranking driver: weak fit cannot be rescued by popularity, but inactive candidates should drop.

## Statistical Profile Of The Dataset

- Full pass over `100,000` candidates.
- Experience distribution:
  - mean: `7.17`
  - p10: `2.2`
  - p50: `6.8`
  - p90: `13.0`
- Recruiter response rate:
  - mean: `0.437`
  - p50: `0.44`
  - p90: `0.73`
- Notice period:
  - p25: `60`
  - p50: `90`
  - p75: `120`
- Country mix:
  - `India`: `75,113`
  - `USA`: `9,978`
  - remaining countries are much smaller

## Skill Frequency Analysis

Most common raw skills are intentionally noisy and not predictive by themselves. Top-frequency skills include:

- `HTML`
- `Databricks`
- `Redux`
- `Terraform`
- `Angular`
- `Figma`
- `Salesforce CRM`
- `Vue.js`
- `Sales`
- `Accounting`
- `Kafka`
- `BigQuery`
- `Airflow`
- `AWS`
- `Flask`
- `Spark`

Interpretation:

- Global skill frequency is a weak ranking signal because the dataset is synthetic and deliberately broad.
- Career-history context matters much more than raw skill count.

## Common Candidate Archetypes

- Non-AI professionals with AI keyword lists: HR, marketing, accounting, project, sales, design, support.
- Adjacent engineers transitioning toward ML: software, backend, data, analytics engineers with retrieval or LLM tooling.
- Applied AI/ML engineers with direct search, ranking, recommendation, or matching experience.
- Consulting-heavy AI candidates with modern tool exposure but weaker product ownership.

## Likely Top-Performer Archetypes

- `Search / relevance / ranking engineers` with production deployment and evaluation-framework evidence.
- `Applied ML / recommendation engineers` at product or marketplace companies.
- `Backend/data engineers` who demonstrably built retrieval or ranking systems, not just data pipelines.
- `NLP / AI engineers` whose work includes retrieval, reranking, candidate-role matching, and offline/online evaluation.

## Likely Honeypot Archetypes

- `Marketing Manager` / `HR Manager` / `Content Writer` with Pinecone, FAISS, Weaviate, RAG, and LTR in skills but no technical career history.
- Junior candidates with near-perfect behavioral metrics and deep expert-level skill lists.
- Profiles where duration math or seniority labels do not add up.
- CV/speech specialists made to look like retrieval engineers through skill stuffing.

## Ranking Design Summary

- Stage 1 gates obvious low-fit profiles.
- Stage 2 extracts evidence from titles, summaries, skills, career history, and platform signals.
- Stage 3 scores semantic fit for retrieval, ranking, recommendation, evaluation, Python, and LLM tooling.
- Stage 4 scores behavior and hireability.
- Stage 5 scores career evidence, product/startup fit, ownership, and recent hands-on depth.
- Stage 6 penalizes honeypots and inconsistent profiles.
- Stage 7 combines all signals with semantic and career evidence as the main drivers, behavior as a multiplier, and honeypot penalties as a hard brake.
