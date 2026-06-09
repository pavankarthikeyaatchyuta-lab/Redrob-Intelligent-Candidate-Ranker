# Explainability Report

## Audit Of The Previous Explainability Layer

### How reasoning was generated before the redesign

- A short threshold-based template selected a few generic strengths from high-level scores such as title, matched skills, product fit, and one concern.
- The template used aggregated scores like `semantic_score`, `career_evidence_score`, and `behavioral_score`, but did not expose their component values.
- Gate penalties and honeypot penalties influenced rank but were not clearly surfaced to the recruiter-facing explanation.

### Where it fell short

- Candidate-specific: partially yes, but often too templated.
- Recruiter-readable: mostly yes, but too abstract for decision support.
- Traceable to actual features: only partially, because many statements hid the underlying metrics.
- Useful for human decision making: limited, because it did not consistently show concrete positives, negatives, or behavioral evidence.

## Redesign Summary

- Explanations are now grounded in explicit feature groups: semantic fit, behavioral signals, career evidence, and penalties.
- Every ranked candidate now has:
  - overall score
  - recruiter-style summary
  - top positive factors
  - top negative factors
  - behavioral signal highlights
  - career evidence highlights
  - skill alignment highlights
- Non-explainable parts of the old pipeline were redesigned by exposing score components and penalty sources in `score_breakdown`, `semantic_components`, `behavioral_components`, and `career_components`.

## Scoring Methodology

Final score formula:

```text
final_score = stage1_gate
              * (0.58 * semantic_score + 0.42 * career_evidence_score + synergy_terms)
              * (0.72 + 0.38 * behavioral_score)
              * (1 - honeypot_penalty)
```

### Feature importance by design

- `semantic_score` is the largest single driver because the JD strongly emphasizes retrieval, ranking, recommendation, and evaluation evidence.
- `career_evidence_score` is nearly as important because the challenge explicitly warns against skill-list-only ranking.
- `behavioral_score` is multiplicative so that availability and recruiter engagement can down-rank weakly available candidates without rescuing weak technical fits.
- `stage1_gate` and `honeypot_penalty` act as safety controls for obvious non-fits and suspicious profiles.

### Weight rationale

- Retrieval and ranking evidence got the heaviest semantic weights because they map most directly to the JD.
- Product/startup fit, recent hands-on work, and production ML evidence are emphasized because the JD prefers shippers over pure researchers.
- Response rate, recency, recruiter saves, and notice period are emphasized because the behavioral-signal doc says availability can be more predictive than static profile quality.

## Sample Explanations For Top Candidates

### Rank 1: CAND_0018499

- Summary: Strong semantic alignment with retrieval and ranking requirements; 7.2 years of experience in Senior Machine Learning Engineer; currently at Zomato. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.61 recruiter response rate, 15-day notice, 16 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.860595`
- Positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (16 saves, 1291 search appearances), good India hybrid logistics fit (Noida, Uttar Pradesh, India), and strong responsiveness (0.61 response rate, 59.6h avg response time)
- Negative factors: no major red flags after timeline and behavioral sanity checks

### Rank 2: CAND_0081846

- Summary: Strong semantic alignment with retrieval and ranking requirements; 6.7 years of experience in Lead AI Engineer; currently at Razorpay. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.73 recruiter response rate, 30-day notice, and 62 recruiter saves in 30d.
- Overall score: `0.838547`
- Positive factors: strong responsiveness (0.73 response rate, 40.2h avg response time), recent hands-on engineering evidence (0.94), healthy recruiter demand (62 saves, 347 search appearances), and production ML evidence (0.74)
- Negative factors: no major red flags after timeline and behavioral sanity checks

### Rank 3: CAND_0077337

- Summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.0 years of experience in Staff Machine Learning Engineer; currently at Paytm. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.95 recruiter response rate, 60-day notice, 32 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.815400`
- Positive factors: healthy recruiter demand (32 saves, 240 search appearances), strong responsiveness (0.95 response rate, 26.0h avg response time), recent hands-on engineering evidence (0.89), and product/startup fit (0.77)
- Negative factors: no major red flags after timeline and behavioral sanity checks

### Rank 4: CAND_0046064

- Summary: Strong semantic alignment with retrieval and ranking requirements; 8.9 years of experience in Senior NLP Engineer; currently at Salesforce. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.78 recruiter response rate, 30-day notice, and 25 recruiter saves in 30d.
- Overall score: `0.781323`
- Positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (25 saves, 802 search appearances), strong responsiveness (0.78 response rate, 40.8h avg response time), and short notice period (30 days)
- Negative factors: no major red flags after timeline and behavioral sanity checks

### Rank 5: CAND_0079387

- Summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.9 years of experience in AI Engineer; currently at Microsoft. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.81 recruiter response rate, 30-day notice, and 22 recruiter saves in 30d.
- Overall score: `0.768999`
- Positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (22 saves, 189 search appearances), strong responsiveness (0.81 response rate, 29.1h avg response time), and product/startup fit (0.73)
- Negative factors: no major red flags after timeline and behavioral sanity checks

## Justification For Ranking Decisions

- Candidates rise when they show combined retrieval/ranking evidence, product-context delivery, recent hands-on engineering, and realistic hireability signals.
- Candidates fall when they rely on skill keywords without matching role history, have slow recruiter responsiveness, long notice periods, relocation friction, or profile inconsistency flags.
- This keeps the final ranking aligned with both hidden relevance judgments and recruiter usability.

## Ranked Candidate Explainability

### Rank 1: CAND_0018499

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.2 years of experience in Senior Machine Learning Engineer; currently at Zomato. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.61 recruiter response rate, 15-day notice, 16 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.860595`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (16 saves, 1291 search appearances), good India hybrid logistics fit (Noida, Uttar Pradesh, India), and strong responsiveness (0.61 response rate, 59.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 22 days, marked open to work, 0.61 recruiter response rate, 15-day notice period, and 16 recruiter saves in 30 days
- Career evidence highlights: Senior Machine Learning Engineer with 7.2 years of experience, product-company background at Zomato, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zomato, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Weaviate, Pinecone, Information Retrieval, Milvus, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.78, ranking=0.79, recommendation=0.07, evaluation=0.54, python=0.10, llm=0.78`
- Behavioral component scores: `activity=0.91, responsiveness=0.82, recruiter_attractiveness=0.97, logistics=0.88`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.76, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.6212, career_evidence_score=0.9175, semantic_plus_career=0.8143, behavior_multiplier=1.0568, behavioral_score=0.8863, honeypot_penalty=0.0000, final_score=0.8606`

### Rank 2: CAND_0081846

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.7 years of experience in Lead AI Engineer; currently at Razorpay. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.73 recruiter response rate, 30-day notice, and 62 recruiter saves in 30d.
- Overall score: `0.838547`
- Top positive factors: strong responsiveness (0.73 response rate, 40.2h avg response time), recent hands-on engineering evidence (0.94), healthy recruiter demand (62 saves, 347 search appearances), and production ML evidence (0.74)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 32 days, though not very recent, marked open to work, 0.73 recruiter response rate, 30-day notice period, and 62 recruiter saves in 30 days
- Career evidence highlights: Lead AI Engineer with 6.7 years of experience, product-company background at Razorpay, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Razorpay, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Information Retrieval, Elasticsearch, Vector Search, Embeddings, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.83, ranking=0.65, recommendation=0.07, evaluation=0.54, python=0.13, llm=0.64`
- Behavioral component scores: `activity=0.86, responsiveness=0.98, recruiter_attractiveness=0.93, logistics=0.74`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.74, product_fit=0.73, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5852, career_evidence_score=0.9076, semantic_plus_career=0.7841, behavior_multiplier=1.0694, behavioral_score=0.9194, honeypot_penalty=0.0000, final_score=0.8385`

### Rank 3: CAND_0077337

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.0 years of experience in Staff Machine Learning Engineer; currently at Paytm. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.95 recruiter response rate, 60-day notice, 32 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.815400`
- Top positive factors: healthy recruiter demand (32 saves, 240 search appearances), strong responsiveness (0.95 response rate, 26.0h avg response time), recent hands-on engineering evidence (0.89), and product/startup fit (0.77)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 9 days, marked open to work, 0.95 recruiter response rate, 60-day notice period, and 32 recruiter saves in 30 days
- Career evidence highlights: Staff Machine Learning Engineer with 7.0 years of experience, product-company background at Paytm, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Paytm, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Semantic Search, Pinecone, BM25, Information Retrieval, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.72, ranking=0.62, recommendation=0.38, evaluation=0.54, python=0.07, llm=0.45`
- Behavioral component scores: `activity=0.87, responsiveness=0.89, recruiter_attractiveness=0.95, logistics=0.74`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.73, product_fit=0.77, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5680, career_evidence_score=0.9002, semantic_plus_career=0.7704, behavior_multiplier=1.0584, behavioral_score=0.8906, honeypot_penalty=0.0000, final_score=0.8154`

### Rank 4: CAND_0046064

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.9 years of experience in Senior NLP Engineer; currently at Salesforce. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.78 recruiter response rate, 30-day notice, and 25 recruiter saves in 30d.
- Overall score: `0.781323`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (25 saves, 802 search appearances), strong responsiveness (0.78 response rate, 40.8h avg response time), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 39 days, though not very recent, marked open to work, 0.78 recruiter response rate, 30-day notice period, and 25 recruiter saves in 30 days
- Career evidence highlights: Senior NLP Engineer with 8.9 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Salesforce, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Pinecone, BM25, OpenSearch, Elasticsearch, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.71, ranking=0.52, recommendation=0.10, evaluation=0.42, python=0.22, llm=0.81`
- Behavioral component scores: `activity=0.67, responsiveness=0.93, recruiter_attractiveness=1.00, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.68, product_fit=0.63, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5306, career_evidence_score=0.8877, semantic_plus_career=0.7361, behavior_multiplier=1.0615, behavioral_score=0.8986, honeypot_penalty=0.0000, final_score=0.7813`

### Rank 5: CAND_0079387

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.9 years of experience in AI Engineer; currently at Microsoft. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.81 recruiter response rate, 30-day notice, and 22 recruiter saves in 30d.
- Overall score: `0.768999`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (22 saves, 189 search appearances), strong responsiveness (0.81 response rate, 29.1h avg response time), and product/startup fit (0.73)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 40 days, though not very recent, marked open to work, 0.81 recruiter response rate, 30-day notice period, and 22 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 6.9 years of experience, product-company background at Microsoft, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Microsoft, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Sentence Transformers, Vector Search, OpenSearch, BM25, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.68, ranking=0.41, recommendation=0.50, evaluation=0.44, python=0.23, llm=0.23`
- Behavioral component scores: `activity=0.72, responsiveness=0.96, recruiter_attractiveness=0.96, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.70, product_fit=0.73, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4961, career_evidence_score=0.9051, semantic_plus_career=0.7221, behavior_multiplier=1.0650, behavioral_score=0.9079, honeypot_penalty=0.0000, final_score=0.7690`

### Rank 6: CAND_0086022

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 5.3 years of experience in Senior Applied Scientist; currently at Sarvam AI. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.55 recruiter response rate, 0-day notice, and 53 recruiter saves in 30d.
- Overall score: `0.767938`
- Top positive factors: recent hands-on engineering evidence (0.94), good India hybrid logistics fit (Kolkata, West Bengal, India), healthy recruiter demand (53 saves, 723 search appearances), and product/startup fit (0.76)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 50 days, though not very recent, marked open to work, 0.55 recruiter response rate, 0-day notice period, and 53 recruiter saves in 30 days
- Career evidence highlights: Senior Applied Scientist with 5.3 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Sarvam AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Vector Search, Elasticsearch, Pinecone, Embeddings, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.83, ranking=0.54, recommendation=0.07, evaluation=0.50, python=0.13, llm=0.69`
- Behavioral component scores: `activity=0.73, responsiveness=0.69, recruiter_attractiveness=0.82, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.72, product_fit=0.76, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5540, career_evidence_score=0.9080, semantic_plus_career=0.7627, behavior_multiplier=1.0069, behavioral_score=0.7550, honeypot_penalty=0.0000, final_score=0.7679`

### Rank 7: CAND_0005649

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.4 years of experience in Senior Data Scientist; currently at Sarvam AI. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.57 recruiter response rate, 90-day notice, and 26 recruiter saves in 30d.
- Overall score: `0.761375`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Delhi, Delhi, India), healthy recruiter demand (26 saves, 595 search appearances), and product/startup fit (0.76)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 51 days, though not very recent, marked open to work, 0.57 recruiter response rate, 90-day notice period, and 26 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 7.4 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Sarvam AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Semantic Search, Weaviate, Information Retrieval, Recommendation Systems, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.91, ranking=0.43, recommendation=0.47, evaluation=0.42, python=0.10, llm=0.30`
- Behavioral component scores: `activity=0.59, responsiveness=0.69, recruiter_attractiveness=0.79, logistics=0.88`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.75, product_fit=0.76, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5514, career_evidence_score=0.9194, semantic_plus_career=0.7643, behavior_multiplier=0.9961, behavioral_score=0.7267, honeypot_penalty=0.0000, final_score=0.7614`

### Rank 8: CAND_0005260

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 5.2 years of experience in Senior NLP Engineer; currently at Netflix. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.86 recruiter response rate, 60-day notice, 11 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.746122`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Chennai, Tamil Nadu, India), healthy recruiter demand (11 saves, 1154 search appearances), and strong responsiveness (0.86 response rate, 46.8h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 25 days, 0.86 recruiter response rate, 60-day notice period, 11 recruiter saves in 30 days, and 1154 recruiter search appearances in 30 days
- Career evidence highlights: Senior NLP Engineer with 5.2 years of experience, product-company background at Netflix, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Netflix, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Information Retrieval, Semantic Search, Embeddings, Python, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.71, ranking=0.52, recommendation=0.00, evaluation=0.42, python=0.29, llm=0.92`
- Behavioral component scores: `activity=0.56, responsiveness=0.84, recruiter_attractiveness=0.85, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.56, ownership=0.89, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5350, career_evidence_score=0.8622, semantic_plus_career=0.7262, behavior_multiplier=1.0275, behavioral_score=0.8091, honeypot_penalty=0.0000, final_score=0.7461`

### Rank 9: CAND_0044883

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.3 years of experience in AI Engineer; currently at Mad Street Den. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.84 recruiter response rate, 90-day notice, 59 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.733134`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.84 response rate, 28.8h avg response time), healthy recruiter demand (59 saves, 888 search appearances), and production ML evidence (0.73)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 28 days, 0.84 recruiter response rate, 90-day notice period, 59 recruiter saves in 30 days, and 888 recruiter search appearances in 30 days
- Career evidence highlights: AI Engineer with 6.3 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Mad Street Den, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: BM25, Embeddings, Semantic Search, PyTorch, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.83, ranking=0.43, recommendation=0.41, evaluation=0.44, python=0.16, llm=0.36`
- Behavioral component scores: `activity=0.35, responsiveness=0.79, recruiter_attractiveness=0.77, logistics=0.76`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.73, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5358, career_evidence_score=0.8907, semantic_plus_career=0.7390, behavior_multiplier=0.9921, behavioral_score=0.7159, honeypot_penalty=0.0000, final_score=0.7331`

### Rank 10: CAND_0002025

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 5.9 years of experience in Senior AI Engineer; currently at Apple. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.80 recruiter response rate, 30-day notice, 22 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.730233`
- Top positive factors: strong responsiveness (0.80 response rate, 20.9h avg response time), healthy recruiter demand (22 saves, 949 search appearances), recent hands-on engineering evidence (0.94), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 9 days, marked open to work, 0.80 recruiter response rate, 30-day notice period, and 22 recruiter saves in 30 days
- Career evidence highlights: Senior AI Engineer with 5.9 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Apple, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: FAISS, OpenSearch, Weaviate, Sentence Transformers, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.43, ranking=0.53, recommendation=0.38, evaluation=0.45, python=0.16, llm=0.45`
- Behavioral component scores: `activity=0.99, responsiveness=0.98, recruiter_attractiveness=0.97, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.64, product_fit=0.66, ownership=0.89, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4540, career_evidence_score=0.8665, semantic_plus_career=0.6737, behavior_multiplier=1.0839, behavioral_score=0.9576, honeypot_penalty=0.0000, final_score=0.7302`

### Rank 11: CAND_0069905

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.6 years of experience in Applied ML Engineer; currently at Sarvam AI. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.78 recruiter response rate, 90-day notice, and 57 recruiter saves in 30d.
- Overall score: `0.720277`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (57 saves, 315 search appearances), strong responsiveness (0.78 response rate, 68.8h avg response time), and product/startup fit (0.72)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 44 days, though not very recent, marked open to work, 0.78 recruiter response rate, 90-day notice period, and 57 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 6.6 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Sarvam AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Sentence Transformers, Weaviate, Learning to Rank, Recommendation Systems, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.76, ranking=0.41, recommendation=0.47, evaluation=0.14, python=0.13, llm=0.23`
- Behavioral component scores: `activity=0.73, responsiveness=0.89, recruiter_attractiveness=0.90, logistics=0.78`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.59, product_fit=0.72, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4602, career_evidence_score=0.8841, semantic_plus_career=0.6884, behavior_multiplier=1.0463, behavioral_score=0.8588, honeypot_penalty=0.0000, final_score=0.7203`

### Rank 12: CAND_0046525

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.1 years of experience in Senior Machine Learning Engineer; currently at Genpact AI. Career history points to hands-on production ml ownership and matched skills include elasticsearch, information retrieval, and sentence transformers. Behavioral signals are solid with 0.88 recruiter response rate, 60-day notice, 38 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.715718`
- Top positive factors: healthy recruiter demand (38 saves, 663 search appearances), recent hands-on engineering evidence (0.94), strong responsiveness (0.88 response rate, 12.0h avg response time), and good India hybrid logistics fit (Pune, Maharashtra, India)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 12 days, marked open to work, 0.88 recruiter response rate, 60-day notice period, and 38 recruiter saves in 30 days
- Career evidence highlights: Senior Machine Learning Engineer with 6.1 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Genpact AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Elasticsearch, Information Retrieval, Sentence Transformers, Qdrant, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.66, ranking=0.60, recommendation=0.00, evaluation=0.48, python=0.00, llm=0.45`
- Behavioral component scores: `activity=0.81, responsiveness=0.92, recruiter_attractiveness=0.96, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.27, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4710, career_evidence_score=0.8271, semantic_plus_career=0.6703, behavior_multiplier=1.0677, behavioral_score=0.9151, honeypot_penalty=0.0000, final_score=0.7157`

### Rank 13: CAND_0044855

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.6 years of experience in Senior Data Scientist; currently at Flipkart. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.57 recruiter response rate, 60-day notice, and 43 recruiter saves in 30d.
- Overall score: `0.715251`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (43 saves, 821 search appearances), good India hybrid logistics fit (Coimbatore, Tamil Nadu, India), and product/startup fit (0.79)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 41 days, though not very recent, 0.57 recruiter response rate, 60-day notice period, 43 recruiter saves in 30 days, and 821 recruiter search appearances in 30 days
- Career evidence highlights: Senior Data Scientist with 6.6 years of experience, product-company background at Flipkart, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Flipkart, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: OpenSearch, Information Retrieval, Pinecone, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.41, recommendation=0.58, evaluation=0.29, python=0.07, llm=0.22`
- Behavioral component scores: `activity=0.45, responsiveness=0.70, recruiter_attractiveness=0.88, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.69, product_fit=0.79, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4739, career_evidence_score=0.9134, semantic_plus_career=0.7143, behavior_multiplier=1.0013, behavioral_score=0.7402, honeypot_penalty=0.0000, final_score=0.7153`

### Rank 14: CAND_0083307

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.8 years of experience in Search Engineer; currently at CRED. Career history points to hands-on production ml ownership and matched skills include embeddings, pinecone, and weaviate. Behavioral signals are solid with 0.70 recruiter response rate, 120-day notice, and 28 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.714179`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (28 saves, 233 search appearances), strong responsiveness (0.70 response rate, 25.7h avg response time), and strong retrieval and ranking alignment (0.79/0.54)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 75 days, though not very recent, marked open to work, 0.70 recruiter response rate, 120-day notice period, and 28 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.8 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, LLM tooling and matched skills: Embeddings, Pinecone, Weaviate, Semantic Search
- Semantic component scores: `retrieval=0.79, ranking=0.54, recommendation=0.12, evaluation=0.23, python=0.13, llm=0.33`
- Behavioral component scores: `activity=0.61, responsiveness=0.79, recruiter_attractiveness=0.95, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.63, product_fit=0.55, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4780, career_evidence_score=0.8647, semantic_plus_career=0.6926, behavior_multiplier=1.0311, behavioral_score=0.8187, honeypot_penalty=0.0000, final_score=0.7142`

### Rank 15: CAND_0071974

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.8 years of experience in Senior AI Engineer; currently at Netflix. Career history points to hands-on production ml ownership and matched skills include weaviate, bm25, and pinecone. Behavioral signals are solid with 0.76 recruiter response rate, 45-day notice, and 50 recruiter saves in 30d.
- Overall score: `0.712283`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.76 response rate, 38.2h avg response time), healthy recruiter demand (50 saves, 132 search appearances), and production ML evidence (0.67)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 49 days, though not very recent, marked open to work, 0.76 recruiter response rate, 45-day notice period, and 50 recruiter saves in 30 days
- Career evidence highlights: Senior AI Engineer with 7.8 years of experience, product-company background at Netflix, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Netflix, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Weaviate, BM25, Pinecone, Information Retrieval, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.74, ranking=0.36, recommendation=0.25, evaluation=0.35, python=0.10, llm=0.39`
- Behavioral component scores: `activity=0.82, responsiveness=0.95, recruiter_attractiveness=0.90, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.54, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4468, career_evidence_score=0.8712, semantic_plus_career=0.6733, behavior_multiplier=1.0580, behavioral_score=0.8894, honeypot_penalty=0.0000, final_score=0.7123`

### Rank 16: CAND_0008425

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.8 years of experience in Senior NLP Engineer; currently at Ola. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.66 recruiter response rate, 90-day notice, and 55 recruiter saves in 30d.
- Overall score: `0.705636`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (55 saves, 1136 search appearances), strong responsiveness (0.66 response rate, 10.8h avg response time), and product/startup fit (0.72)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 40 days, though not very recent, marked open to work, 0.66 recruiter response rate, 90-day notice period, and 55 recruiter saves in 30 days
- Career evidence highlights: Senior NLP Engineer with 7.8 years of experience, product-company background at Ola, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Ola, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Qdrant, Sentence Transformers, Semantic Search, Information Retrieval, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.74, ranking=0.40, recommendation=0.16, evaluation=0.29, python=0.16, llm=0.32`
- Behavioral component scores: `activity=0.71, responsiveness=0.76, recruiter_attractiveness=1.00, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.66, product_fit=0.72, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4388, career_evidence_score=0.8962, semantic_plus_career=0.6835, behavior_multiplier=1.0324, behavioral_score=0.8221, honeypot_penalty=0.0000, final_score=0.7056`

### Rank 17: CAND_0041669

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 8.0 years of experience in Recommendation Systems Engineer; currently at CRED. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.77 recruiter response rate, 60-day notice, and 37 recruiter saves in 30d.
- Overall score: `0.704816`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (37 saves, 326 search appearances), strong responsiveness (0.77 response rate, 3.7h avg response time), and good India hybrid logistics fit (Noida, Uttar Pradesh, India)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 59 days, though not very recent, marked open to work, 0.77 recruiter response rate, 60-day notice period, and 37 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 8.0 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, LLM tooling, matched skills: FAISS, Milvus, Semantic Search, Weaviate, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.48, ranking=0.57, recommendation=0.70, evaluation=0.23, python=0.13, llm=0.34`
- Behavioral component scores: `activity=0.67, responsiveness=0.92, recruiter_attractiveness=0.97, logistics=0.91`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.59, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4771, career_evidence_score=0.8080, semantic_plus_career=0.6644, behavior_multiplier=1.0609, behavioral_score=0.8970, honeypot_penalty=0.0000, final_score=0.7048`

### Rank 18: CAND_0080766

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.8 years of experience in Staff Machine Learning Engineer; currently at Salesforce. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.66 recruiter response rate, 0-day notice, and 27 recruiter saves in 30d.
- Overall score: `0.702248`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (27 saves, 1105 search appearances), good India hybrid logistics fit (Coimbatore, Tamil Nadu, India), and strong responsiveness (0.66 response rate, 37.9h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 56 days, though not very recent, 0.66 recruiter response rate, 0-day notice period, 27 recruiter saves in 30 days, and 1105 recruiter search appearances in 30 days
- Career evidence highlights: Staff Machine Learning Engineer with 8.8 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Salesforce, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, matched skills: Information Retrieval Systems, Elasticsearch, OpenSearch, Milvus, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.62, ranking=0.48, recommendation=0.15, evaluation=0.50, python=0.13, llm=0.13`
- Behavioral component scores: `activity=0.55, responsiveness=0.85, recruiter_attractiveness=0.96, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.63, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4354, career_evidence_score=0.8843, semantic_plus_career=0.6757, behavior_multiplier=1.0393, behavioral_score=0.8403, honeypot_penalty=0.0000, final_score=0.7022`

### Rank 19: CAND_0061265

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.6 years of experience in Recommendation Systems Engineer; currently at Zoho. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.94 recruiter response rate, 120-day notice, and 24 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.695168`
- Top positive factors: good India hybrid logistics fit (Delhi, Delhi, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (24 saves, 461 search appearances), and strong responsiveness (0.94 response rate, 5.7h avg response time)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 71 days, though not very recent, marked open to work, 0.94 recruiter response rate, 120-day notice period, and 24 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.6 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zoho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Qdrant, Vector Search, Embeddings, Milvus, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.83, ranking=0.41, recommendation=0.70, evaluation=0.19, python=0.10, llm=0.20`
- Behavioral component scores: `activity=0.61, responsiveness=0.73, recruiter_attractiveness=0.81, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.66, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5141, career_evidence_score=0.8079, semantic_plus_career=0.6883, behavior_multiplier=1.0100, behavioral_score=0.7631, honeypot_penalty=0.0000, final_score=0.6952`

### Rank 20: CAND_0075249

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.2 years of experience in Applied ML Engineer; currently at Zomato. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.82 recruiter response rate, 45-day notice, and 9 recruiter saves in 30d.
- Overall score: `0.692876`
- Top positive factors: recent hands-on engineering evidence (0.89), strong responsiveness (0.82 response rate, 23.8h avg response time), healthy recruiter demand (9 saves, 850 search appearances), and product/startup fit (0.73)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 56 days, though not very recent, marked open to work, 0.82 recruiter response rate, 45-day notice period, and 9 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 6.2 years of experience, product-company background at Zomato, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zomato, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Sentence Transformers, Milvus, BM25, Pinecone, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.77, ranking=0.45, recommendation=0.43, evaluation=0.15, python=0.07, llm=0.07`
- Behavioral component scores: `activity=0.73, responsiveness=0.85, recruiter_attractiveness=0.78, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.64, product_fit=0.73, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4460, career_evidence_score=0.8656, semantic_plus_career=0.6760, behavior_multiplier=1.0250, behavioral_score=0.8026, honeypot_penalty=0.0000, final_score=0.6929`

### Rank 21: CAND_0028793

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.2 years of experience in Search Engineer; currently at Google. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.57 recruiter response rate, 120-day notice, and 43 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.691655`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (43 saves, 1096 search appearances), good India hybrid logistics fit (Trivandrum, Kerala, India), and production ML evidence (0.66)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 52 days, though not very recent, marked open to work, 0.57 recruiter response rate, 120-day notice period, and 43 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.2 years of experience, product-company background at Google, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Google, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Embeddings, Information Retrieval, Learning to Rank, PyTorch, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.63, ranking=0.49, recommendation=0.30, evaluation=0.27, python=0.07, llm=0.34`
- Behavioral component scores: `activity=0.81, responsiveness=0.63, recruiter_attractiveness=1.00, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.66, product_fit=0.56, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4442, career_evidence_score=0.8725, semantic_plus_career=0.6754, behavior_multiplier=1.0241, behavioral_score=0.8003, honeypot_penalty=0.0000, final_score=0.6917`

### Rank 22: CAND_0064326

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.6 years of experience in Search Engineer; currently at Sarvam AI. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.94 recruiter response rate, 45-day notice, 60 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.691395`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.94 response rate, 13.5h avg response time), good India hybrid logistics fit (Gurgaon, Haryana, India), and healthy recruiter demand (60 saves, 916 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 14 days, marked open to work, 0.94 recruiter response rate, 45-day notice period, and 60 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.6 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Sarvam AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Milvus, Semantic Search, Weaviate, BM25
- Semantic component scores: `retrieval=0.48, ranking=0.57, recommendation=0.12, evaluation=0.23, python=0.13, llm=0.27`
- Behavioral component scores: `activity=0.81, responsiveness=0.95, recruiter_attractiveness=0.84, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.61, product_fit=0.76, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3894, career_evidence_score=0.8947, semantic_plus_career=0.6534, behavior_multiplier=1.0582, behavioral_score=0.8900, honeypot_penalty=0.0000, final_score=0.6914`

### Rank 23: CAND_0041610

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.7 years of experience in Recommendation Systems Engineer; currently at Zoho. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.52 recruiter response rate, 30-day notice, 18 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.690578`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (18 saves, 717 search appearances), recommendation or matching relevance (0.77), and strong responsiveness (0.52 response rate, 4.8h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 21 days, marked open to work, 0.52 recruiter response rate, 30-day notice period, and 18 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.7 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zoho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Elasticsearch, OpenSearch, BM25, Embeddings, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.52, ranking=0.60, recommendation=0.77, evaluation=0.33, python=0.16, llm=0.23`
- Behavioral component scores: `activity=0.77, responsiveness=0.72, recruiter_attractiveness=0.80, logistics=0.74`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.58, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5119, career_evidence_score=0.8059, semantic_plus_career=0.6858, behavior_multiplier=1.0070, behavioral_score=0.7553, honeypot_penalty=0.0000, final_score=0.6906`

### Rank 24: CAND_0093912

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 5.3 years of experience in Senior Data Scientist; currently at Razorpay. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.66 recruiter response rate, 30-day notice, 56 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.689927`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (56 saves, 773 search appearances), strong responsiveness (0.66 response rate, 39.7h avg response time), and product/startup fit (0.73)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 24 days, marked open to work, 0.66 recruiter response rate, 30-day notice period, and 56 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 5.3 years of experience, product-company background at Razorpay, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Razorpay, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Milvus, Embeddings, Vector Search, Elasticsearch
- Semantic component scores: `retrieval=0.67, ranking=0.55, recommendation=0.19, evaluation=0.08, python=0.07, llm=0.04`
- Behavioral component scores: `activity=0.75, responsiveness=0.88, recruiter_attractiveness=0.99, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.73, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3973, career_evidence_score=0.8795, semantic_plus_career=0.6530, behavior_multiplier=1.0565, behavioral_score=0.8855, honeypot_penalty=0.0000, final_score=0.6899`

### Rank 25: CAND_0042506

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 4.2 years of experience in Search Engineer; currently at Verloop.io. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.48 recruiter response rate, 15-day notice, 49 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.686102`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Mumbai, Maharashtra, India), product/startup fit (0.76), and healthy recruiter demand (49 saves, 41 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 13 days, marked open to work, 0.48 recruiter response rate, 15-day notice period, and 49 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 4.2 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Verloop.io, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Semantic Search, Information Retrieval, Milvus, Qdrant, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.72, ranking=0.38, recommendation=0.31, evaluation=0.25, python=0.13, llm=0.29`
- Behavioral component scores: `activity=0.96, responsiveness=0.72, recruiter_attractiveness=0.73, logistics=0.88`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.66, product_fit=0.76, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4381, career_evidence_score=0.8800, semantic_plus_career=0.6767, behavior_multiplier=1.0139, behavioral_score=0.7735, honeypot_penalty=0.0000, final_score=0.6861`

### Rank 26: CAND_0007412

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 7.4 years of experience in Applied ML Engineer; currently at Zoho. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.76 recruiter response rate, 120-day notice, and 38 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.682099`
- Top positive factors: good India hybrid logistics fit (Noida, Uttar Pradesh, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.76 response rate, 23.7h avg response time), and healthy recruiter demand (38 saves, 785 search appearances)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 46 days, though not very recent, marked open to work, 0.76 recruiter response rate, 120-day notice period, and 38 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 7.4 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zoho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Pinecone, Milvus, BM25, Recommendation Systems, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.51, ranking=0.35, recommendation=0.65, evaluation=0.29, python=0.07, llm=0.22`
- Behavioral component scores: `activity=0.82, responsiveness=0.87, recruiter_attractiveness=0.85, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.64, product_fit=0.63, ownership=1.00, recent_hands_on=1.00, tenure_fit=0.75`
- Score path: `stage1_gate=1.0000, semantic_score=0.4071, career_evidence_score=0.8802, semantic_plus_career=0.6493, behavior_multiplier=1.0506, behavioral_score=0.8700, honeypot_penalty=0.0000, final_score=0.6821`

### Rank 27: CAND_0092278

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.8 years of experience in Senior NLP Engineer; currently at Microsoft. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Main concern: candidate looks inactive and slow to engage recruiters.
- Overall score: `0.678133`
- Top positive factors: good India hybrid logistics fit (Pune, Maharashtra, India), recent hands-on engineering evidence (1.00), production ML evidence (0.75), and strong retrieval and ranking alignment (0.68/0.76)
- Top negative factors: candidate looks inactive and slow to engage recruiters and weak recruiter responsiveness (0.07)
- Behavioral signal highlights: last active 209 days ago, 0.07 recruiter response rate, 90-day notice period, 1 recruiter saves in 30 days, and 1417 recruiter search appearances in 30 days
- Career evidence highlights: Senior NLP Engineer with 6.8 years of experience, product-company background at Microsoft, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Microsoft, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Elasticsearch, Vector Search, Milvus, Semantic Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.68, ranking=0.76, recommendation=0.31, evaluation=0.54, python=0.07, llm=0.58`
- Behavioral component scores: `activity=0.26, responsiveness=0.27, recruiter_attractiveness=0.68, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.75, product_fit=0.71, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5954, career_evidence_score=0.9116, semantic_plus_career=0.7924, behavior_multiplier=0.9009, behavioral_score=0.4760, honeypot_penalty=0.0500, final_score=0.6781`

### Rank 28: CAND_0033861

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.0 years of experience in Senior NLP Engineer; currently at Mad Street Den. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.16 recruiter response rate, 30-day notice, and 4 recruiter saves in 30d. Main concern: weak recruiter responsiveness (0.16).
- Overall score: `0.674713`
- Top positive factors: recent hands-on engineering evidence (1.00), short notice period (30 days), production ML evidence (0.70), and strong retrieval and ranking alignment (0.62/0.67)
- Top negative factors: weak recruiter responsiveness (0.16)
- Behavioral signal highlights: last active 108 days ago, 0.16 recruiter response rate, 30-day notice period, 4 recruiter saves in 30 days, and 990 recruiter search appearances in 30 days
- Career evidence highlights: Senior NLP Engineer with 8.0 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Mad Street Den, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Weaviate, Elasticsearch, Pinecone, Qdrant, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.62, ranking=0.67, recommendation=0.19, evaluation=0.42, python=0.22, llm=0.63`
- Behavioral component scores: `activity=0.38, responsiveness=0.35, recruiter_attractiveness=0.64, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.70, product_fit=0.64, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5427, career_evidence_score=0.8911, semantic_plus_career=0.7468, behavior_multiplier=0.9035, behavioral_score=0.4830, honeypot_penalty=0.0000, final_score=0.6747`

### Rank 29: CAND_0010685

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.7 years of experience in NLP Engineer; currently at Rephrase.ai. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.83 recruiter response rate, 30-day notice, and 46 recruiter saves in 30d.
- Overall score: `0.674626`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.83 response rate, 77.7h avg response time), healthy recruiter demand (46 saves, 779 search appearances), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 80 days, though not very recent, marked open to work, 0.83 recruiter response rate, 30-day notice period, and 46 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 6.7 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Rephrase.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, matched skills: Information Retrieval, Elasticsearch, PyTorch, MLflow, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.63, ranking=0.35, recommendation=0.12, evaluation=0.29, python=0.23, llm=0.20`
- Behavioral component scores: `activity=0.68, responsiveness=0.94, recruiter_attractiveness=0.90, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.62, product_fit=0.70, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3841, career_evidence_score=0.8859, semantic_plus_career=0.6440, behavior_multiplier=1.0475, behavioral_score=0.8618, honeypot_penalty=0.0000, final_score=0.6746`

### Rank 30: CAND_0088025

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.6 years of experience in Staff Machine Learning Engineer; currently at Yellow.ai. Matched skills include pinecone, bm25, and elasticsearch. Behavioral signals are solid with 0.83 recruiter response rate, 90-day notice, 19 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.672888`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (19 saves, 1398 search appearances), strong responsiveness (0.83 response rate, 24.1h avg response time), and strong retrieval and ranking alignment (0.68/0.44)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 21 days, marked open to work, 0.83 recruiter response rate, 90-day notice period, and 19 recruiter saves in 30 days
- Career evidence highlights: Staff Machine Learning Engineer with 8.6 years of experience, recent role remains hands-on in engineering terms at current company Yellow.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Pinecone, BM25, Elasticsearch, Learning to Rank
- Semantic component scores: `retrieval=0.68, ranking=0.44, recommendation=0.15, evaluation=0.20, python=0.13, llm=0.30`
- Behavioral component scores: `activity=0.80, responsiveness=0.90, recruiter_attractiveness=0.93, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.46, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4159, career_evidence_score=0.8375, semantic_plus_career=0.6374, behavior_multiplier=1.0557, behavioral_score=0.8835, honeypot_penalty=0.0000, final_score=0.6729`

### Rank 31: CAND_0084819

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 4.5 years of experience in Search Engineer; currently at Dream11. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.74 recruiter response rate, 120-day notice, 50 recruiter saves in 30d, and active in the last 30 days. Main concern: long notice period (120 days).
- Overall score: `0.669602`
- Top positive factors: healthy recruiter demand (50 saves, 1056 search appearances), recent hands-on engineering evidence (0.94), strong responsiveness (0.74 response rate, 52.9h avg response time), and product/startup fit (0.58)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 26 days, marked open to work, 0.74 recruiter response rate, 120-day notice period, and 50 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 4.5 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Dream11, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Semantic Search, BM25, OpenSearch, Weaviate
- Semantic component scores: `retrieval=0.60, ranking=0.48, recommendation=0.19, evaluation=0.15, python=0.13, llm=0.29`
- Behavioral component scores: `activity=0.88, responsiveness=0.87, recruiter_attractiveness=1.00, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.56, product_fit=0.58, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4003, career_evidence_score=0.8305, semantic_plus_career=0.6291, behavior_multiplier=1.0643, behavioral_score=0.9061, honeypot_penalty=0.0000, final_score=0.6696`

### Rank 32: CAND_0052328

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 6.5 years of experience in Recommendation Systems Engineer; currently at Amazon. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.79 recruiter response rate, 30-day notice, and 31 recruiter saves in 30d.
- Overall score: `0.668989`
- Top positive factors: good India hybrid logistics fit (Pune, Maharashtra, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.79 response rate, 31.9h avg response time), and healthy recruiter demand (31 saves, 627 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 65 days, though not very recent, marked open to work, 0.79 recruiter response rate, 30-day notice period, and 31 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.5 years of experience, product-company background at Amazon, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Amazon, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: OpenSearch, Vector Search, Sentence Transformers, Learning to Rank, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.60, ranking=0.35, recommendation=0.77, evaluation=0.35, python=0.16, llm=0.36`
- Behavioral component scores: `activity=0.64, responsiveness=0.95, recruiter_attractiveness=0.86, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=0.67, production_ml=0.59, product_fit=0.57, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4838, career_evidence_score=0.7365, semantic_plus_career=0.6355, behavior_multiplier=1.0528, behavioral_score=0.8757, honeypot_penalty=0.0000, final_score=0.6690`

### Rank 33: CAND_0052682

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.6 years of experience in NLP Engineer; currently at Aganitha. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.88 recruiter response rate, 30-day notice, and 16 recruiter saves in 30d.
- Overall score: `0.667415`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (16 saves, 850 search appearances), strong responsiveness (0.88 response rate, 34.2h avg response time), and product/startup fit (0.74)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 68 days, though not very recent, marked open to work, 0.88 recruiter response rate, 30-day notice period, and 16 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 6.6 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Aganitha, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Semantic Search, FAISS, Embeddings, PyTorch, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.45, ranking=0.29, recommendation=0.43, evaluation=0.29, python=0.13, llm=0.30`
- Behavioral component scores: `activity=0.77, responsiveness=0.97, recruiter_attractiveness=1.00, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.59, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3607, career_evidence_score=0.8879, semantic_plus_career=0.6236, behavior_multiplier=1.0702, behavioral_score=0.9215, honeypot_penalty=0.0000, final_score=0.6674`

### Rank 34: CAND_0065195

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 5.1 years of experience in Search Engineer; currently at CRED. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.80 recruiter response rate, 45-day notice, 13 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.658752`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.80 response rate, 22.7h avg response time), healthy recruiter demand (13 saves, 1027 search appearances), and product/startup fit (0.58)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 11 days, marked open to work, 0.80 recruiter response rate, 45-day notice period, and 13 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 5.1 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Elasticsearch, Qdrant, Learning to Rank, BentoML, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.57, ranking=0.35, recommendation=0.12, evaluation=0.39, python=0.16, llm=0.36`
- Behavioral component scores: `activity=0.69, responsiveness=0.94, recruiter_attractiveness=0.85, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.58, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3893, career_evidence_score=0.8571, semantic_plus_career=0.6302, behavior_multiplier=1.0454, behavioral_score=0.8563, honeypot_penalty=0.0000, final_score=0.6588`

### Rank 35: CAND_0030348

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 4.5 years of experience in Machine Learning Engineer; currently at BYJU'S. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.54 recruiter response rate, 45-day notice, and 18 recruiter saves in 30d.
- Overall score: `0.657153`
- Top positive factors: healthy recruiter demand (18 saves, 593 search appearances), good India hybrid logistics fit (Noida, Uttar Pradesh, India), recent hands-on engineering evidence (0.89), and strong responsiveness (0.54 response rate, 30.9h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 66 days, though not very recent, marked open to work, 0.54 recruiter response rate, 45-day notice period, and 18 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 4.5 years of experience, product-company background at BYJU'S, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company BYJU'S, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Embeddings, Vector Search, Elasticsearch, PyTorch, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.74, ranking=0.29, recommendation=0.49, evaluation=0.14, python=0.13, llm=0.07`
- Behavioral component scores: `activity=0.78, responsiveness=0.74, recruiter_attractiveness=0.92, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.61, product_fit=0.74, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4064, career_evidence_score=0.8392, semantic_plus_career=0.6362, behavior_multiplier=1.0330, behavioral_score=0.8237, honeypot_penalty=0.0000, final_score=0.6572`

### Rank 36: CAND_0066376

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 5.7 years of experience in Applied ML Engineer; currently at Dream11. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.51 recruiter response rate, 90-day notice, and 59 recruiter saves in 30d.
- Overall score: `0.656963`
- Top positive factors: good India hybrid logistics fit (Mumbai, Maharashtra, India), recent hands-on engineering evidence (0.89), production ML evidence (0.64), and healthy recruiter demand (59 saves, 61 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 32 days, though not very recent, marked open to work, 0.51 recruiter response rate, 90-day notice period, and 59 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 5.7 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Dream11, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Information Retrieval, BM25, FAISS, Semantic Search, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.73, ranking=0.45, recommendation=0.50, evaluation=0.20, python=0.00, llm=0.20`
- Behavioral component scores: `activity=0.75, responsiveness=0.62, recruiter_attractiveness=0.63, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.64, product_fit=0.60, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4557, career_evidence_score=0.8465, semantic_plus_career=0.6711, behavior_multiplier=0.9789, behavioral_score=0.6814, honeypot_penalty=0.0000, final_score=0.6570`

### Rank 37: CAND_0027801

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 7.4 years of experience in NLP Engineer; currently at InMobi. Background fits a product or marketplace environment and matched skills include faiss, milvus, and opensearch. Behavioral signals are solid with 0.65 recruiter response rate, 120-day notice, and 65 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.656455`
- Top positive factors: good India hybrid logistics fit (Hyderabad, Telangana, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (65 saves, 521 search appearances), and strong responsiveness (0.65 response rate, 28.5h avg response time)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 53 days, though not very recent, marked open to work, 0.65 recruiter response rate, 120-day notice period, and 65 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 7.4 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company InMobi, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: FAISS, Milvus, OpenSearch, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.58, ranking=0.20, recommendation=0.58, evaluation=0.39, python=0.15, llm=0.17`
- Behavioral component scores: `activity=0.78, responsiveness=0.69, recruiter_attractiveness=1.00, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3990, career_evidence_score=0.8588, semantic_plus_career=0.6321, behavior_multiplier=1.0386, behavioral_score=0.8383, honeypot_penalty=0.0000, final_score=0.6565`

### Rank 38: CAND_0040117

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.5 years of experience in Recommendation Systems Engineer; currently at PhonePe. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.66 recruiter response rate, 15-day notice, and 28 recruiter saves in 30d.
- Overall score: `0.653431`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (28 saves, 280 search appearances), strong responsiveness (0.66 response rate, 7.1h avg response time), and product/startup fit (0.73)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 79 days, though not very recent, marked open to work, 0.66 recruiter response rate, 15-day notice period, and 28 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.5 years of experience, product-company background at PhonePe, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company PhonePe, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Embeddings, FAISS, BM25, LlamaIndex, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.54, ranking=0.34, recommendation=0.70, evaluation=0.29, python=0.00, llm=0.30`
- Behavioral component scores: `activity=0.68, responsiveness=0.81, recruiter_attractiveness=0.86, logistics=0.79`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.65, product_fit=0.73, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4207, career_evidence_score=0.8250, semantic_plus_career=0.6369, behavior_multiplier=1.0259, behavioral_score=0.8050, honeypot_penalty=0.0000, final_score=0.6534`

### Rank 39: CAND_0074735

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.5 years of experience in Applied ML Engineer; currently at Rephrase.ai. Background fits a product or marketplace environment and matched skills include weaviate, information retrieval, and semantic search. Behavioral signals are solid with 0.77 recruiter response rate, 90-day notice, and 31 recruiter saves in 30d.
- Overall score: `0.652882`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (31 saves, 391 search appearances), strong responsiveness (0.77 response rate, 10.4h avg response time), and product/startup fit (0.77)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 68 days, though not very recent, marked open to work, 0.77 recruiter response rate, 90-day notice period, and 31 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 5.5 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Rephrase.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, LLM tooling, matched skills: Weaviate, Information Retrieval, Semantic Search, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.51, ranking=0.26, recommendation=0.30, evaluation=0.35, python=0.16, llm=0.36`
- Behavioral component scores: `activity=0.77, responsiveness=0.86, recruiter_attractiveness=0.91, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.77, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3669, career_evidence_score=0.8816, semantic_plus_career=0.6267, behavior_multiplier=1.0418, behavioral_score=0.8468, honeypot_penalty=0.0000, final_score=0.6529`

### Rank 40: CAND_0042029

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.5 years of experience in Senior Data Scientist; currently at Flipkart. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.67 recruiter response rate, 45-day notice, and 16 recruiter saves in 30d.
- Overall score: `0.652280`
- Top positive factors: healthy recruiter demand (16 saves, 209 search appearances), good India hybrid logistics fit (Delhi, Delhi, India), recent hands-on engineering evidence (0.89), and strong responsiveness (0.67 response rate, 20.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 52 days, though not very recent, 0.67 recruiter response rate, 45-day notice period, 16 recruiter saves in 30 days, and 209 recruiter search appearances in 30 days
- Career evidence highlights: Senior Data Scientist with 6.5 years of experience, product-company background at Flipkart, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Flipkart, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, matched skills: Elasticsearch, Embeddings, OpenSearch, Weaviate, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.60, ranking=0.45, recommendation=0.12, evaluation=0.29, python=0.07, llm=0.16`
- Behavioral component scores: `activity=0.35, responsiveness=0.76, recruiter_attractiveness=0.98, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.62, product_fit=0.74, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3803, career_evidence_score=0.8757, semantic_plus_career=0.6407, behavior_multiplier=1.0182, behavioral_score=0.7846, honeypot_penalty=0.0000, final_score=0.6523`

### Rank 41: CAND_0079064

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.2 years of experience in Senior Data Scientist; currently at Niramai. Matched skills include opensearch, semantic search, and pinecone. Behavioral signals are solid with 0.91 recruiter response rate, 120-day notice, and 39 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.650013`
- Top positive factors: good India hybrid logistics fit (Noida, Uttar Pradesh, India), healthy recruiter demand (39 saves, 386 search appearances), recent hands-on engineering evidence (0.89), and strong responsiveness (0.91 response rate, 2.7h avg response time)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 52 days, though not very recent, marked open to work, 0.91 recruiter response rate, 120-day notice period, and 39 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 5.2 years of experience, recent role remains hands-on in engineering terms at current company Niramai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, LLM tooling, matched skills: OpenSearch, Semantic Search, Pinecone, Recommendation Systems, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.33, recommendation=0.37, evaluation=0.14, python=0.00, llm=0.34`
- Behavioral component scores: `activity=0.79, responsiveness=0.87, recruiter_attractiveness=0.93, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.44, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3991, career_evidence_score=0.8165, semantic_plus_career=0.6147, behavior_multiplier=1.0575, behavioral_score=0.8882, honeypot_penalty=0.0000, final_score=0.6500`

### Rank 42: CAND_0098846

- Recruiter summary: Strong semantic alignment with ranking requirements; 7.6 years of experience in AI Engineer; currently at upGrad. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.62 recruiter response rate, 45-day notice, and 13 recruiter saves in 30d.
- Overall score: `0.649545`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (13 saves, 747 search appearances), good India hybrid logistics fit (Indore, Madhya Pradesh, India), and strong responsiveness (0.62 response rate, 12.0h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 42 days, though not very recent, marked open to work, 0.62 recruiter response rate, 45-day notice period, and 13 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 7.6 years of experience, product-company background at upGrad, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company upGrad, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: ranking, ranking evaluation, matched skills: Qdrant, Recommendation Systems, BentoML, PEFT, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.35, ranking=0.49, recommendation=0.19, evaluation=0.33, python=0.16, llm=0.30`
- Behavioral component scores: `activity=0.83, responsiveness=0.80, recruiter_attractiveness=0.96, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3556, career_evidence_score=0.8805, semantic_plus_career=0.6195, behavior_multiplier=1.0484, behavioral_score=0.8643, honeypot_penalty=0.0000, final_score=0.6495`

### Rank 43: CAND_0030953

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.8 years of experience in Search Engineer; currently at Nykaa. Career history points to hands-on production ml ownership and matched skills include qdrant, weaviate, and learning to rank. Behavioral signals are solid with 0.63 recruiter response rate, 45-day notice, and 46 recruiter saves in 30d.
- Overall score: `0.649288`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (46 saves, 472 search appearances), and strong responsiveness (0.63 response rate, 62.1h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 54 days, though not very recent, 0.63 recruiter response rate, 45-day notice period, 46 recruiter saves in 30 days, and 472 recruiter search appearances in 30 days
- Career evidence highlights: Search Engineer with 7.8 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Nykaa, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Qdrant, Weaviate, Learning to Rank, Python, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.55, ranking=0.41, recommendation=0.49, evaluation=0.29, python=0.07, llm=0.23`
- Behavioral component scores: `activity=0.46, responsiveness=0.68, recruiter_attractiveness=0.84, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.65, product_fit=0.52, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4193, career_evidence_score=0.8639, semantic_plus_career=0.6508, behavior_multiplier=0.9977, behavioral_score=0.7307, honeypot_penalty=0.0000, final_score=0.6493`

### Rank 44: CAND_0007009

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.9 years of experience in Recommendation Systems Engineer; currently at Wysa. Career history points to hands-on production ml ownership and matched skills include weaviate, embeddings, and bm25. Behavioral signals are solid with 0.62 recruiter response rate, 30-day notice, and 5 recruiter saves in 30d.
- Overall score: `0.649173`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Noida, Uttar Pradesh, India), strong responsiveness (0.62 response rate, 41.8h avg response time), and recommendation or matching relevance (0.70)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 77 days, though not very recent, marked open to work, 0.62 recruiter response rate, 30-day notice period, and 5 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 7.9 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Wysa, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, LLM tooling, matched skills: Weaviate, Embeddings, BM25, Sentence Transformers, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.40, recommendation=0.70, evaluation=0.23, python=0.07, llm=0.40`
- Behavioral component scores: `activity=0.75, responsiveness=0.83, recruiter_attractiveness=0.70, logistics=0.88`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=0.75, production_ml=0.58, product_fit=0.45, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4970, career_evidence_score=0.7307, semantic_plus_career=0.6394, behavior_multiplier=1.0153, behavioral_score=0.7772, honeypot_penalty=0.0000, final_score=0.6492`

### Rank 45: CAND_0094056

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.9 years of experience in NLP Engineer; currently at Rephrase.ai. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.82 recruiter response rate, 120-day notice, and 4 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.648971`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (0.89), strong responsiveness (0.82 response rate, 55.8h avg response time), and product/startup fit (0.77)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 49 days, though not very recent, 0.82 recruiter response rate, 120-day notice period, 4 recruiter saves in 30 days, and 788 recruiter search appearances in 30 days
- Career evidence highlights: NLP Engineer with 5.9 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Rephrase.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Pinecone, Milvus, BM25, Sentence Transformers, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.26, recommendation=0.58, evaluation=0.19, python=0.16, llm=0.20`
- Behavioral component scores: `activity=0.30, responsiveness=0.79, recruiter_attractiveness=0.69, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.77, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4256, career_evidence_score=0.8684, semantic_plus_career=0.6569, behavior_multiplier=0.9879, behavioral_score=0.7049, honeypot_penalty=0.0000, final_score=0.6490`

### Rank 46: CAND_0086151

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.7 years of experience in Recommendation Systems Engineer; currently at Wysa. Career history points to hands-on production ml ownership and matched skills include qdrant, opensearch, and embeddings. Behavioral signals are solid with 0.52 recruiter response rate, 120-day notice, and 55 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.648913`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (55 saves, 432 search appearances), recommendation or matching relevance (0.77), and production ML evidence (0.66)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 73 days, though not very recent, marked open to work, 0.52 recruiter response rate, 120-day notice period, and 55 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 7.7 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Wysa, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Qdrant, OpenSearch, Embeddings, Sentence Transformers, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.71, ranking=0.40, recommendation=0.77, evaluation=0.10, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.74, responsiveness=0.53, recruiter_attractiveness=1.00, logistics=0.74`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.66, product_fit=0.44, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4700, career_evidence_score=0.7827, semantic_plus_career=0.6485, behavior_multiplier=1.0007, behavioral_score=0.7386, honeypot_penalty=0.0000, final_score=0.6489`

### Rank 47: CAND_0068811

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 8.0 years of experience in Applied ML Engineer; currently at Freshworks. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.42 recruiter response rate, 30-day notice, 4 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.647074`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Pune, Maharashtra, India), product/startup fit (0.74), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 14 days, marked open to work, 0.42 recruiter response rate, 30-day notice period, and 4 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 8.0 years of experience, product-company background at Freshworks, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Freshworks, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Vector Search, Qdrant, Embeddings, Pinecone, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.49, ranking=0.39, recommendation=0.53, evaluation=0.48, python=0.10, llm=0.16`
- Behavioral component scores: `activity=0.82, responsiveness=0.62, recruiter_attractiveness=0.54, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.65, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4213, career_evidence_score=0.8989, semantic_plus_career=0.6679, behavior_multiplier=0.9688, behavioral_score=0.6547, honeypot_penalty=0.0000, final_score=0.6471`

### Rank 48: CAND_0060054

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.4 years of experience in AI Engineer; currently at Mad Street Den. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.86 recruiter response rate, 15-day notice, and 39 recruiter saves in 30d.
- Overall score: `0.646480`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Jaipur, Rajasthan, India), strong responsiveness (0.86 response rate, 66.3h avg response time), and healthy recruiter demand (39 saves, 256 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 79 days, though not very recent, 0.86 recruiter response rate, 15-day notice period, 39 recruiter saves in 30 days, and 256 recruiter search appearances in 30 days
- Career evidence highlights: AI Engineer with 6.4 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Mad Street Den, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Weaviate, FAISS, Elasticsearch, Semantic Search, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.29, recommendation=0.65, evaluation=0.14, python=0.00, llm=0.07`
- Behavioral component scores: `activity=0.28, responsiveness=0.86, recruiter_attractiveness=0.70, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.66, product_fit=0.61, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4034, career_evidence_score=0.8796, semantic_plus_career=0.6506, behavior_multiplier=0.9937, behavioral_score=0.7202, honeypot_penalty=0.0000, final_score=0.6465`

### Rank 49: CAND_0041611

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.4 years of experience in Staff Machine Learning Engineer; currently at Locobuzz. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.07 recruiter response rate and 30-day notice. Main concern: candidate looks inactive and slow to engage recruiters.
- Overall score: `0.646128`
- Top positive factors: recent hands-on engineering evidence (1.00), strong retrieval and ranking alignment (0.74/0.80), production ML evidence (0.75), and short notice period (30 days)
- Top negative factors: candidate looks inactive and slow to engage recruiters and weak recruiter responsiveness (0.07)
- Behavioral signal highlights: last active 183 days ago, 0.07 recruiter response rate, 30-day notice period, and 1004 recruiter search appearances in 30 days
- Career evidence highlights: Staff Machine Learning Engineer with 6.4 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Locobuzz, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Qdrant, Weaviate, BM25, OpenSearch, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.74, ranking=0.80, recommendation=0.00, evaluation=0.62, python=0.07, llm=0.51`
- Behavioral component scores: `activity=0.26, responsiveness=0.28, recruiter_attractiveness=0.57, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.75, product_fit=0.57, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.5820, career_evidence_score=0.8911, semantic_plus_career=0.7768, behavior_multiplier=0.8756, behavioral_score=0.4093, honeypot_penalty=0.0500, final_score=0.6461`

### Rank 50: CAND_0018722

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.6 years of experience in Recommendation Systems Engineer; currently at Saarthi.ai. Career history points to hands-on production ml ownership and matched skills include weaviate, recommendation systems, and python. Behavioral signals are solid with 0.79 recruiter response rate, 90-day notice, and 16 recruiter saves in 30d.
- Overall score: `0.643800`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (16 saves, 1034 search appearances), strong responsiveness (0.79 response rate, 5.2h avg response time), and recommendation or matching relevance (0.77)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 41 days, though not very recent, marked open to work, 0.79 recruiter response rate, 90-day notice period, and 16 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.6 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Saarthi.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Weaviate, Recommendation Systems, Python, Flask, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.34, recommendation=0.77, evaluation=0.04, python=0.13, llm=0.13`
- Behavioral component scores: `activity=0.67, responsiveness=0.88, recruiter_attractiveness=0.90, logistics=0.67`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.58, product_fit=0.43, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4421, career_evidence_score=0.7671, semantic_plus_career=0.6206, behavior_multiplier=1.0374, behavioral_score=0.8352, honeypot_penalty=0.0000, final_score=0.6438`

### Rank 51: CAND_0029367

- Recruiter summary: Strong semantic alignment with retrieval requirements; 5.7 years of experience in Senior Data Scientist; currently at Rephrase.ai. Background fits a product or marketplace environment and matched skills include faiss, sentence transformers, and pinecone. Behavioral signals are solid with 0.77 recruiter response rate, 90-day notice, 7 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.640040`
- Top positive factors: good India hybrid logistics fit (Bangalore, Karnataka, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.77 response rate, 7.8h avg response time), and product/startup fit (0.74)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 15 days, marked open to work, 0.77 recruiter response rate, 90-day notice period, and 7 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 5.7 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Rephrase.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search and matched skills: FAISS, Sentence Transformers, Pinecone, Vector Search
- Semantic component scores: `retrieval=0.70, ranking=0.29, recommendation=0.19, evaluation=0.10, python=0.20, llm=0.30`
- Behavioral component scores: `activity=0.81, responsiveness=0.79, recruiter_attractiveness=0.69, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.52, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3749, career_evidence_score=0.8749, semantic_plus_career=0.6292, behavior_multiplier=1.0173, behavioral_score=0.7823, honeypot_penalty=0.0000, final_score=0.6400`

### Rank 52: CAND_0030031

- Recruiter summary: Strong semantic alignment with recommendation requirements; 5.7 years of experience in AI Engineer; currently at Microsoft. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.94 recruiter response rate, 30-day notice, 13 recruiter saves in 30d, and active in the last 30 days. Main concern: Direct ranking-system evidence is thinner than the strongest profiles.
- Overall score: `0.637404`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.94 response rate, 71.5h avg response time), healthy recruiter demand (13 saves, 784 search appearances), and product/startup fit (0.72)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 13 days, 0.94 recruiter response rate, 30-day notice period, 13 recruiter saves in 30 days, and 784 recruiter search appearances in 30 days
- Career evidence highlights: AI Engineer with 5.7 years of experience, product-company background at Microsoft, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Microsoft, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Information Retrieval, BM25, Sentence Transformers, Milvus, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.36, ranking=0.23, recommendation=0.61, evaluation=0.39, python=0.23, llm=0.24`
- Behavioral component scores: `activity=0.71, responsiveness=0.93, recruiter_attractiveness=0.83, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.59, product_fit=0.72, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3567, career_evidence_score=0.8837, semantic_plus_career=0.6137, behavior_multiplier=1.0387, behavioral_score=0.8386, honeypot_penalty=0.0000, final_score=0.6374`

### Rank 53: CAND_0011687

- Recruiter summary: Strong semantic alignment with retrieval requirements; 7.8 years of experience in Senior NLP Engineer; currently at Niramai. Career history points to hands-on production ml ownership and matched skills include opensearch, faiss, and embeddings. Behavioral signals are solid with 0.89 recruiter response rate, 15-day notice, 27 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.637110`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (27 saves, 403 search appearances), strong responsiveness (0.89 response rate, 7.5h avg response time), and short notice period (15 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 25 days, marked open to work, 0.89 recruiter response rate, 15-day notice period, and 27 recruiter saves in 30 days
- Career evidence highlights: Senior NLP Engineer with 7.8 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Niramai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking evaluation, LLM tooling, matched skills: OpenSearch, FAISS, Embeddings, Weaviate, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.65, ranking=0.28, recommendation=0.15, evaluation=0.28, python=0.16, llm=0.39`
- Behavioral component scores: `activity=0.80, responsiveness=0.93, recruiter_attractiveness=0.95, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.61, product_fit=0.42, ownership=0.67, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3805, career_evidence_score=0.8037, semantic_plus_career=0.5993, behavior_multiplier=1.0630, behavioral_score=0.9027, honeypot_penalty=0.0000, final_score=0.6371`

### Rank 54: CAND_0050454

- Recruiter summary: Strong semantic alignment with retrieval requirements; 6.8 years of experience in AI Engineer; currently at Rephrase.ai. Background fits a product or marketplace environment and matched skills include faiss, qdrant, and bm25. Behavioral signals are solid with 0.77 recruiter response rate, 30-day notice, and 30 recruiter saves in 30d.
- Overall score: `0.635228`
- Top positive factors: recent hands-on engineering evidence (0.94), strong responsiveness (0.77 response rate, 32.2h avg response time), good India hybrid logistics fit (Delhi, Delhi, India), and healthy recruiter demand (30 saves, 248 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 38 days, though not very recent, marked open to work, 0.77 recruiter response rate, 30-day notice period, and 30 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 6.8 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Rephrase.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search and matched skills: FAISS, Qdrant, BM25, PyTorch
- Semantic component scores: `retrieval=0.74, ranking=0.29, recommendation=0.12, evaluation=0.04, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.82, responsiveness=0.91, recruiter_attractiveness=0.79, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.51, product_fit=0.74, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3429, career_evidence_score=0.8674, semantic_plus_career=0.6070, behavior_multiplier=1.0466, behavioral_score=0.8594, honeypot_penalty=0.0000, final_score=0.6352`

### Rank 55: CAND_0058575

- Recruiter summary: Strong semantic alignment with retrieval requirements; 5.8 years of experience in AI Engineer; currently at Krutrim. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.69 recruiter response rate, 90-day notice, and 47 recruiter saves in 30d.
- Overall score: `0.634350`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.69 response rate, 16.1h avg response time), and healthy recruiter demand (47 saves, 120 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 60 days, though not very recent, marked open to work, 0.69 recruiter response rate, 90-day notice period, and 47 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 5.8 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Krutrim, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking evaluation, matched skills: Pinecone, Sentence Transformers, Recommendation Systems, PyTorch, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.63, ranking=0.29, recommendation=0.19, evaluation=0.36, python=0.16, llm=0.20`
- Behavioral component scores: `activity=0.64, responsiveness=0.75, recruiter_attractiveness=0.72, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.56, product_fit=0.67, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3801, career_evidence_score=0.8723, semantic_plus_career=0.6315, behavior_multiplier=1.0045, behavioral_score=0.7487, honeypot_penalty=0.0000, final_score=0.6343`

### Rank 56: CAND_0027691

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.5 years of experience in NLP Engineer; currently at Haptik. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.68 recruiter response rate, 15-day notice, and 25 recruiter saves in 30d.
- Overall score: `0.633804`
- Top positive factors: good India hybrid logistics fit (Pune, Maharashtra, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.68 response rate, 14.7h avg response time), and short notice period (15 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 65 days, though not very recent, marked open to work, 0.68 recruiter response rate, 15-day notice period, and 25 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 6.5 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Haptik, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, Python stack, matched skills: Weaviate, Embeddings, Semantic Search, Learning to Rank, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.58, ranking=0.26, recommendation=0.37, evaluation=0.35, python=0.29, llm=0.20`
- Behavioral component scores: `activity=0.63, responsiveness=0.79, recruiter_attractiveness=0.63, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.56, product_fit=0.62, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3954, career_evidence_score=0.8639, semantic_plus_career=0.6347, behavior_multiplier=0.9986, behavioral_score=0.7332, honeypot_penalty=0.0000, final_score=0.6338`

### Rank 57: CAND_0054123

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 4.7 years of experience in Applied ML Engineer; currently at Meta. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.87 recruiter response rate, 60-day notice, 11 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.632930`
- Top positive factors: good India hybrid logistics fit (Gurgaon, Haryana, India), recent hands-on engineering evidence (0.89), strong responsiveness (0.87 response rate, 72.8h avg response time), and healthy recruiter demand (11 saves, 147 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 27 days, 0.87 recruiter response rate, 60-day notice period, 11 recruiter saves in 30 days, and 147 recruiter search appearances in 30 days
- Career evidence highlights: Applied ML Engineer with 4.7 years of experience, product-company background at Meta, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Meta, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Weaviate, Qdrant, Vector Search, Semantic Search, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.73, ranking=0.34, recommendation=0.43, evaluation=0.20, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.32, responsiveness=0.80, recruiter_attractiveness=0.76, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.62, product_fit=0.57, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4228, career_evidence_score=0.8149, semantic_plus_career=0.6339, behavior_multiplier=0.9985, behavioral_score=0.7330, honeypot_penalty=0.0000, final_score=0.6329`

### Rank 58: CAND_0049896

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 7.3 years of experience in Search Engineer; currently at Unacademy. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.43 recruiter response rate, 90-day notice, 44 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.631294`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Vizag, Andhra Pradesh, India), healthy recruiter demand (44 saves, 1097 search appearances), and strong retrieval/search alignment (0.64)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 18 days, marked open to work, 0.43 recruiter response rate, 90-day notice period, and 44 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.3 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Unacademy, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, LLM tooling, matched skills: Sentence Transformers, Information Retrieval, Vector Search, PyTorch, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.64, ranking=0.34, recommendation=0.31, evaluation=0.25, python=0.07, llm=0.36`
- Behavioral component scores: `activity=0.78, responsiveness=0.51, recruiter_attractiveness=0.76, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.63, product_fit=0.59, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4028, career_evidence_score=0.8721, semantic_plus_career=0.6472, behavior_multiplier=0.9754, behavioral_score=0.6722, honeypot_penalty=0.0000, final_score=0.6313`

### Rank 59: CAND_0057563

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.8 years of experience in NLP Engineer; currently at Locobuzz. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.83 recruiter response rate, 60-day notice, and 33 recruiter saves in 30d.
- Overall score: `0.630471`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Indore, Madhya Pradesh, India), strong responsiveness (0.83 response rate, 63.7h avg response time), and healthy recruiter demand (33 saves, 680 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 44 days, though not very recent, 0.83 recruiter response rate, 60-day notice period, 33 recruiter saves in 30 days, and 680 recruiter search appearances in 30 days
- Career evidence highlights: NLP Engineer with 6.8 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Locobuzz, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Elasticsearch, OpenSearch, RAG, QLoRA, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.63, ranking=0.31, recommendation=0.31, evaluation=0.10, python=0.00, llm=0.20`
- Behavioral component scores: `activity=0.43, responsiveness=0.86, recruiter_attractiveness=0.83, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.58, product_fit=0.73, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3470, career_evidence_score=0.8835, semantic_plus_career=0.6193, behavior_multiplier=1.0180, behavioral_score=0.7841, honeypot_penalty=0.0000, final_score=0.6305`

### Rank 60: CAND_0001610

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 3.0 years of experience in Machine Learning Engineer; currently at Dream11. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.57 recruiter response rate, 90-day notice, and 53 recruiter saves in 30d.
- Overall score: `0.630355`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (53 saves, 306 search appearances), good India hybrid logistics fit (Trivandrum, Kerala, India), and strong retrieval/search alignment (0.82)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 53 days, though not very recent, marked open to work, 0.57 recruiter response rate, 90-day notice period, and 53 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 3.0 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Dream11, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Pinecone, Milvus, Sentence Transformers, Information Retrieval, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.82, ranking=0.29, recommendation=0.31, evaluation=0.10, python=0.07, llm=0.07`
- Behavioral component scores: `activity=0.81, responsiveness=0.65, recruiter_attractiveness=0.94, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=0.65, role_depth=1.00, production_ml=0.65, product_fit=0.59, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3882, career_evidence_score=0.8228, semantic_plus_career=0.6172, behavior_multiplier=1.0214, behavioral_score=0.7931, honeypot_penalty=0.0000, final_score=0.6304`

### Rank 61: CAND_0055905

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.1 years of experience in Senior Machine Learning Engineer; currently at Flipkart. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.87 recruiter response rate, 30-day notice, 13 recruiter saves in 30d, and active in the last 30 days. Main concern: outside India without relocation flexibility.
- Overall score: `0.629362`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.87 response rate, 11.3h avg response time), healthy recruiter demand (13 saves, 392 search appearances), and product/startup fit (0.74)
- Top negative factors: outside India without relocation flexibility and outside India without relocation flexibility
- Behavioral signal highlights: active in the last 18 days, marked open to work, 0.87 recruiter response rate, 30-day notice period, and 13 recruiter saves in 30 days
- Career evidence highlights: Senior Machine Learning Engineer with 8.1 years of experience, product-company background at Flipkart, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Flipkart, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Elasticsearch, OpenSearch, Information Retrieval, Embeddings, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.83, ranking=0.48, recommendation=0.00, evaluation=0.44, python=0.16, llm=0.76`
- Behavioral component scores: `activity=0.78, responsiveness=0.89, recruiter_attractiveness=0.88, logistics=0.36`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.70, product_fit=0.74, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=0.8200, semantic_score=0.5286, career_evidence_score=0.9066, semantic_plus_career=0.7445, behavior_multiplier=1.0310, behavioral_score=0.8183, honeypot_penalty=0.0000, final_score=0.6294`

### Rank 62: CAND_0020877

- Recruiter summary: Strong semantic alignment with retrieval requirements; 5.1 years of experience in Applied ML Engineer; currently at CRED. Background fits a product or marketplace environment and matched skills include elasticsearch, opensearch, and information retrieval. Behavioral signals are solid with 0.66 recruiter response rate, 60-day notice, and 19 recruiter saves in 30d.
- Overall score: `0.628996`
- Top positive factors: good India hybrid logistics fit (Gurgaon, Haryana, India), healthy recruiter demand (19 saves, 781 search appearances), recent hands-on engineering evidence (0.89), and strong responsiveness (0.66 response rate, 66.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 62 days, though not very recent, 0.66 recruiter response rate, 60-day notice period, 19 recruiter saves in 30 days, and 781 recruiter search appearances in 30 days
- Career evidence highlights: Applied ML Engineer with 5.1 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, LLM tooling and matched skills: Elasticsearch, OpenSearch, Information Retrieval, Weaviate
- Semantic component scores: `retrieval=0.70, ranking=0.33, recommendation=0.12, evaluation=0.17, python=0.07, llm=0.34`
- Behavioral component scores: `activity=0.45, responsiveness=0.75, recruiter_attractiveness=1.00, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.52, product_fit=0.60, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3757, career_evidence_score=0.8366, semantic_plus_career=0.6119, behavior_multiplier=1.0280, behavioral_score=0.8105, honeypot_penalty=0.0000, final_score=0.6290`

### Rank 63: CAND_0081852

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.9 years of experience in Senior Data Scientist; currently at Mad Street Den. Background fits a product or marketplace environment and matched skills include semantic search, milvus, and weaviate. Behavioral signals are solid with 0.44 recruiter response rate, 45-day notice, 25 recruiter saves in 30d, and active in the last 30 days. Main concern: thin direct ranking evidence (0.20).
- Overall score: `0.627551`
- Top positive factors: good India hybrid logistics fit (Delhi, Delhi, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (25 saves, 438 search appearances), and strong responsiveness (0.44 response rate, 51.6h avg response time)
- Top negative factors: thin direct ranking evidence (0.20)
- Behavioral signal highlights: active in the last 12 days, marked open to work, 0.44 recruiter response rate, 45-day notice period, and 25 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 5.9 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Mad Street Den, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Semantic Search, Milvus, Weaviate, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.55, ranking=0.20, recommendation=0.30, evaluation=0.39, python=0.16, llm=0.22`
- Behavioral component scores: `activity=0.97, responsiveness=0.65, recruiter_attractiveness=0.97, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.62, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3510, career_evidence_score=0.8601, semantic_plus_career=0.6046, behavior_multiplier=1.0379, behavioral_score=0.8366, honeypot_penalty=0.0000, final_score=0.6276`

### Rank 64: CAND_0026532

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 4.8 years of experience in Recommendation Systems Engineer; currently at Zomato. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.52 recruiter response rate, 90-day notice, and 42 recruiter saves in 30d.
- Overall score: `0.626502`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (0.89), product/startup fit (0.75), and healthy recruiter demand (42 saves, 59 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 68 days, though not very recent, marked open to work, 0.52 recruiter response rate, 90-day notice period, and 42 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 4.8 years of experience, product-company background at Zomato, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zomato, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Embeddings, Semantic Search, Information Retrieval, Pinecone, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.83, ranking=0.38, recommendation=0.70, evaluation=0.14, python=0.07, llm=0.24`
- Behavioral component scores: `activity=0.53, responsiveness=0.58, recruiter_attractiveness=0.74, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=0.85, role_depth=0.67, production_ml=0.64, product_fit=0.75, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4993, career_evidence_score=0.7200, semantic_plus_career=0.6439, behavior_multiplier=0.9729, behavioral_score=0.6656, honeypot_penalty=0.0000, final_score=0.6265`

### Rank 65: CAND_0036863

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 4.3 years of experience in Senior Data Scientist; currently at upGrad. Background fits a product or marketplace environment and matched skills include qdrant, opensearch, and bm25. Behavioral signals are solid with 0.46 recruiter response rate, 60-day notice, and 57 recruiter saves in 30d.
- Overall score: `0.626357`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (57 saves, 987 search appearances), and product/startup fit (0.71)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 50 days, though not very recent, marked open to work, 0.46 recruiter response rate, 60-day notice period, and 57 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 4.3 years of experience, product-company background at upGrad, recent role remains hands-on in engineering terms at current company upGrad, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, LLM tooling, matched skills: Qdrant, OpenSearch, BM25, FAISS, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.39, ranking=0.48, recommendation=0.58, evaluation=0.14, python=0.00, llm=0.34`
- Behavioral component scores: `activity=0.76, responsiveness=0.65, recruiter_attractiveness=0.80, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.55, product_fit=0.71, ownership=1.00, recent_hands_on=1.00, tenure_fit=0.75`
- Score path: `stage1_gate=1.0000, semantic_score=0.3794, career_evidence_score=0.8525, semantic_plus_career=0.6224, behavior_multiplier=1.0063, behavioral_score=0.7535, honeypot_penalty=0.0000, final_score=0.6264`

### Rank 66: CAND_0062247

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.3 years of experience in AI Engineer; currently at Google. Background fits a product or marketplace environment and matched skills include pinecone, vector search, and qdrant. Behavioral signals are solid with 0.78 recruiter response rate, 30-day notice, and 9 recruiter saves in 30d.
- Overall score: `0.625309`
- Top positive factors: strong responsiveness (0.78 response rate, 21.0h avg response time), recent hands-on engineering evidence (0.83), healthy recruiter demand (9 saves, 839 search appearances), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 42 days, though not very recent, marked open to work, 0.78 recruiter response rate, 30-day notice period, and 9 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 7.3 years of experience, product-company background at Google, recent role remains hands-on in engineering terms at current company Google, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Pinecone, Vector Search, Qdrant, Information Retrieval, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.74, ranking=0.36, recommendation=0.30, evaluation=0.00, python=0.00, llm=0.13`
- Behavioral component scores: `activity=0.70, responsiveness=0.95, recruiter_attractiveness=0.80, logistics=0.78`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.52, product_fit=0.55, ownership=0.87, recent_hands_on=0.83, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3690, career_evidence_score=0.8176, semantic_plus_career=0.6000, behavior_multiplier=1.0422, behavioral_score=0.8478, honeypot_penalty=0.0000, final_score=0.6253`

### Rank 67: CAND_0053695

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.8 years of experience in Recommendation Systems Engineer; currently at Meesho. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.60 recruiter response rate, 15-day notice, and 34 recruiter saves in 30d.
- Overall score: `0.622705`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (34 saves, 742 search appearances), recommendation or matching relevance (0.77), and short notice period (15 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 63 days, though not very recent, marked open to work, 0.60 recruiter response rate, 15-day notice period, and 34 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 5.8 years of experience, product-company background at Meesho, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Meesho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Pinecone, Embeddings, Sentence Transformers, Recommendation Systems, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.70, ranking=0.25, recommendation=0.77, evaluation=0.15, python=0.00, llm=0.07`
- Behavioral component scores: `activity=0.63, responsiveness=0.66, recruiter_attractiveness=0.90, logistics=0.70`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.67, product_fit=0.58, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4105, career_evidence_score=0.8049, semantic_plus_career=0.6219, behavior_multiplier=1.0014, behavioral_score=0.7404, honeypot_penalty=0.0000, final_score=0.6227`

### Rank 68: CAND_0037566

- Recruiter summary: Strong semantic alignment with retrieval requirements; 6.9 years of experience in Machine Learning Engineer; currently at LinkedIn. Background fits a product or marketplace environment and matched skills include pinecone, bm25, and elasticsearch. Behavioral signals are solid with 0.50 recruiter response rate, 15-day notice, and 23 recruiter saves in 30d.
- Overall score: `0.622383`
- Top positive factors: good India hybrid logistics fit (Bangalore, Karnataka, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (23 saves, 708 search appearances), and strong responsiveness (0.50 response rate, 70.4h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 45 days, though not very recent, marked open to work, 0.50 recruiter response rate, 15-day notice period, and 23 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 6.9 years of experience, product-company background at LinkedIn, recent role remains hands-on in engineering terms at current company LinkedIn, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, LLM tooling and matched skills: Pinecone, BM25, Elasticsearch, MLflow
- Semantic component scores: `retrieval=0.64, ranking=0.29, recommendation=0.12, evaluation=0.20, python=0.07, llm=0.40`
- Behavioral component scores: `activity=0.68, responsiveness=0.70, recruiter_attractiveness=1.00, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.51, product_fit=0.57, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3547, career_evidence_score=0.8471, semantic_plus_career=0.6017, behavior_multiplier=1.0343, behavioral_score=0.8271, honeypot_penalty=0.0000, final_score=0.6224`

### Rank 69: CAND_0044222

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 7.7 years of experience in AI Engineer; currently at PolicyBazaar. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.60 recruiter response rate, 60-day notice, 54 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.622264`
- Top positive factors: healthy recruiter demand (54 saves, 666 search appearances), strong responsiveness (0.60 response rate, 47.0h avg response time), recent hands-on engineering evidence (0.77), and strong retrieval/search alignment (0.74)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 20 days, marked open to work, 0.60 recruiter response rate, 60-day notice period, and 54 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 7.7 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company PolicyBazaar, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Vector Search, OpenSearch, Qdrant, Weaviate, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.74, ranking=0.29, recommendation=0.30, evaluation=0.14, python=0.00, llm=0.20`
- Behavioral component scores: `activity=0.86, responsiveness=0.79, recruiter_attractiveness=0.94, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.58, ownership=0.70, recent_hands_on=0.77, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3752, career_evidence_score=0.8020, semantic_plus_career=0.5968, behavior_multiplier=1.0426, behavioral_score=0.8489, honeypot_penalty=0.0000, final_score=0.6223`

### Rank 70: CAND_0076251

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.6 years of experience in Search Engineer; currently at Haptik. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.51 recruiter response rate, 60-day notice, and 47 recruiter saves in 30d.
- Overall score: `0.621270`
- Top positive factors: recent hands-on engineering evidence (1.00), product/startup fit (0.60), strong responsiveness (0.51 response rate, 24.1h avg response time), and strong retrieval and ranking alignment (0.83/0.35)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 50 days, though not very recent, marked open to work, 0.51 recruiter response rate, 60-day notice period, and 47 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.6 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Haptik, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Weaviate, Elasticsearch, Semantic Search, Learning to Rank
- Semantic component scores: `retrieval=0.83, ranking=0.35, recommendation=0.12, evaluation=0.23, python=0.10, llm=0.20`
- Behavioral component scores: `activity=0.75, responsiveness=0.60, recruiter_attractiveness=0.56, logistics=0.78`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.57, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4160, career_evidence_score=0.8624, semantic_plus_career=0.6488, behavior_multiplier=0.9575, behavioral_score=0.6251, honeypot_penalty=0.0000, final_score=0.6213`

### Rank 71: CAND_0039383

- Recruiter summary: Strong semantic alignment with retrieval requirements; 7.1 years of experience in Applied ML Engineer; currently at Meesho. Background fits a product or marketplace environment and matched skills include faiss, vector search, and elasticsearch. Behavioral signals are solid with 0.61 recruiter response rate, 90-day notice, and 34 recruiter saves in 30d.
- Overall score: `0.619628`
- Top positive factors: good India hybrid logistics fit (Gurgaon, Haryana, India), recent hands-on engineering evidence (0.89), healthy recruiter demand (34 saves, 388 search appearances), and strong responsiveness (0.61 response rate, 67.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 77 days, though not very recent, marked open to work, 0.61 recruiter response rate, 90-day notice period, and 34 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 7.1 years of experience, product-company background at Meesho, recent role remains hands-on in engineering terms at current company Meesho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search and matched skills: FAISS, Vector Search, Elasticsearch, Recommendation Systems
- Semantic component scores: `retrieval=0.70, ranking=0.25, recommendation=0.19, evaluation=0.15, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.75, responsiveness=0.75, recruiter_attractiveness=0.84, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.74, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3462, career_evidence_score=0.8613, semantic_plus_career=0.6064, behavior_multiplier=1.0219, behavioral_score=0.7944, honeypot_penalty=0.0000, final_score=0.6196`

### Rank 72: CAND_0075439

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 4.3 years of experience in Machine Learning Engineer; currently at Flipkart. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.56 recruiter response rate, 30-day notice, 42 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.619333`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (42 saves, 914 search appearances), strong responsiveness (0.56 response rate, 30.5h avg response time), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 28 days, 0.56 recruiter response rate, 30-day notice period, 42 recruiter saves in 30 days, and 914 recruiter search appearances in 30 days
- Career evidence highlights: Machine Learning Engineer with 4.3 years of experience, product-company background at Flipkart, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Flipkart, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, ranking evaluation, matched skills: Elasticsearch, OpenSearch, Vector Search, Information Retrieval, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.55, ranking=0.36, recommendation=0.31, evaluation=0.29, python=0.07, llm=0.26`
- Behavioral component scores: `activity=0.62, responsiveness=0.75, recruiter_attractiveness=0.76, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.62, product_fit=0.59, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3787, career_evidence_score=0.8464, semantic_plus_career=0.6196, behavior_multiplier=0.9996, behavioral_score=0.7359, honeypot_penalty=0.0000, final_score=0.6193`

### Rank 73: CAND_0037980

- Recruiter summary: Strong semantic alignment with ranking requirements; 9.0 years of experience in Senior Applied Scientist; currently at Niramai. Career history points to hands-on production ml ownership and matched skills include bm25, information retrieval systems, and recommendation systems. Behavioral signals are solid with 0.63 recruiter response rate, 0-day notice, and 65 recruiter saves in 30d.
- Overall score: `0.617196`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (65 saves, 748 search appearances), good India hybrid logistics fit (Kolkata, West Bengal, India), and strong responsiveness (0.63 response rate, 42.4h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 68 days, though not very recent, marked open to work, 0.63 recruiter response rate, 0-day notice period, and 65 recruiter saves in 30 days
- Career evidence highlights: Senior Applied Scientist with 9.0 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Niramai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, matched skills: BM25, Information Retrieval Systems, Recommendation Systems, PyTorch, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.35, ranking=0.45, recommendation=0.16, evaluation=0.44, python=0.13, llm=0.20`
- Behavioral component scores: `activity=0.64, responsiveness=0.82, recruiter_attractiveness=0.92, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.59, product_fit=0.51, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3453, career_evidence_score=0.8517, semantic_plus_career=0.5956, behavior_multiplier=1.0363, behavioral_score=0.8324, honeypot_penalty=0.0000, final_score=0.6172`

### Rank 74: CAND_0043228

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.8 years of experience in Applied ML Engineer; currently at Zoho. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.41 recruiter response rate, 30-day notice, 65 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.616087`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (65 saves, 316 search appearances), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 13 days, 0.41 recruiter response rate, 30-day notice period, 65 recruiter saves in 30 days, and 316 recruiter search appearances in 30 days
- Career evidence highlights: Applied ML Engineer with 6.8 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Zoho, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Vector Search, Sentence Transformers, Weaviate, OpenSearch
- Semantic component scores: `retrieval=0.70, ranking=0.38, recommendation=0.12, evaluation=0.19, python=0.16, llm=0.00`
- Behavioral component scores: `activity=0.56, responsiveness=0.62, recruiter_attractiveness=0.81, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.57, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3692, career_evidence_score=0.8625, semantic_plus_career=0.6225, behavior_multiplier=0.9897, behavioral_score=0.7098, honeypot_penalty=0.0000, final_score=0.6161`

### Rank 75: CAND_0006557

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 7.9 years of experience in NLP Engineer; currently at Paytm. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.63 recruiter response rate, 120-day notice, and 53 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.615385`
- Top positive factors: recent hands-on engineering evidence (0.94), healthy recruiter demand (53 saves, 482 search appearances), good India hybrid logistics fit (Jaipur, Rajasthan, India), and product/startup fit (0.74)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 55 days, though not very recent, marked open to work, 0.63 recruiter response rate, 120-day notice period, and 53 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 7.9 years of experience, product-company background at Paytm, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Paytm, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Elasticsearch, OpenSearch, Vector Search, Weaviate, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.39, ranking=0.48, recommendation=0.41, evaluation=0.17, python=0.00, llm=0.24`
- Behavioral component scores: `activity=0.65, responsiveness=0.60, recruiter_attractiveness=0.90, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.56, product_fit=0.74, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3509, career_evidence_score=0.8769, semantic_plus_career=0.6164, behavior_multiplier=0.9984, behavioral_score=0.7325, honeypot_penalty=0.0000, final_score=0.6154`

### Rank 76: CAND_0070398

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 7.2 years of experience in Machine Learning Engineer; currently at Genpact AI. Career history points to hands-on production ml ownership and matched skills include bm25, faiss, and embeddings. Behavioral signals are solid with 0.60 recruiter response rate, 120-day notice, and 13 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.614198`
- Top positive factors: recent hands-on engineering evidence (0.94), good India hybrid logistics fit (Kochi, Kerala, India), healthy recruiter demand (13 saves, 69 search appearances), and strong responsiveness (0.60 response rate, 67.5h avg response time)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 51 days, though not very recent, marked open to work, 0.60 recruiter response rate, 120-day notice period, and 13 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 7.2 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Genpact AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: BM25, FAISS, Embeddings, Information Retrieval
- Semantic component scores: `retrieval=0.79, ranking=0.41, recommendation=0.19, evaluation=0.14, python=0.13, llm=0.20`
- Behavioral component scores: `activity=0.65, responsiveness=0.60, recruiter_attractiveness=0.70, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.59, product_fit=0.31, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4220, career_evidence_score=0.8184, semantic_plus_career=0.6305, behavior_multiplier=0.9741, behavioral_score=0.6686, honeypot_penalty=0.0000, final_score=0.6142`

### Rank 77: CAND_0075574

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 5.7 years of experience in Machine Learning Engineer; currently at Haptik. Career history points to hands-on production ml ownership and matched skills include weaviate, opensearch, and qdrant. Behavioral signals are solid with 0.58 recruiter response rate, 60-day notice, 24 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.612951`
- Top positive factors: recent hands-on engineering evidence (1.00), good India hybrid logistics fit (Bangalore, Karnataka, India), healthy recruiter demand (24 saves, 625 search appearances), and strong responsiveness (0.58 response rate, 44.7h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 18 days, marked open to work, 0.58 recruiter response rate, 60-day notice period, and 24 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 5.7 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Haptik, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Weaviate, OpenSearch, Qdrant, Vector Search, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.39, ranking=0.48, recommendation=0.37, evaluation=0.23, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.69, responsiveness=0.75, recruiter_attractiveness=0.76, logistics=0.88`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.60, product_fit=0.51, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3605, career_evidence_score=0.8544, semantic_plus_career=0.6083, behavior_multiplier=1.0077, behavioral_score=0.7570, honeypot_penalty=0.0000, final_score=0.6130`

### Rank 78: CAND_0095528

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.3 years of experience in Senior Data Scientist; currently at Netflix. Career history points to hands-on production ml ownership and matched skills include opensearch, semantic search, and vector search. Behavioral signals are solid with 0.55 recruiter response rate, 45-day notice, and 25 recruiter saves in 30d.
- Overall score: `0.612812`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.55 response rate, 53.3h avg response time), production ML evidence (0.61), and healthy recruiter demand (25 saves, 46 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 32 days, though not very recent, marked open to work, 0.55 recruiter response rate, 45-day notice period, and 25 recruiter saves in 30 days
- Career evidence highlights: Senior Data Scientist with 5.3 years of experience, product-company background at Netflix, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Netflix, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: OpenSearch, Semantic Search, Vector Search, Qdrant, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.45, ranking=0.29, recommendation=0.53, evaluation=0.39, python=0.23, llm=0.13`
- Behavioral component scores: `activity=0.84, responsiveness=0.75, recruiter_attractiveness=0.61, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.61, product_fit=0.54, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3782, career_evidence_score=0.8614, semantic_plus_career=0.6184, behavior_multiplier=0.9910, behavioral_score=0.7131, honeypot_penalty=0.0000, final_score=0.6128`

### Rank 79: CAND_0017960

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 7.7 years of experience in Recommendation Systems Engineer; currently at Nykaa. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.72 recruiter response rate, 60-day notice, and 43 recruiter saves in 30d.
- Overall score: `0.611008`
- Top positive factors: good India hybrid logistics fit (Bangalore, Karnataka, India), recent hands-on engineering evidence (1.00), strong responsiveness (0.72 response rate, 35.2h avg response time), and healthy recruiter demand (43 saves, 899 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 38 days, though not very recent, marked open to work, 0.72 recruiter response rate, 60-day notice period, and 43 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 7.7 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Nykaa, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Qdrant, Information Retrieval, Python, BentoML, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.44, ranking=0.25, recommendation=0.70, evaluation=0.29, python=0.13, llm=0.30`
- Behavioral component scores: `activity=0.70, responsiveness=0.82, recruiter_attractiveness=0.80, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.61, product_fit=0.61, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3806, career_evidence_score=0.7995, semantic_plus_career=0.5940, behavior_multiplier=1.0286, behavioral_score=0.8122, honeypot_penalty=0.0000, final_score=0.6110`

### Rank 80: CAND_0077285

- Recruiter summary: Strong semantic alignment with recommendation requirements; 5.5 years of experience in Recommendation Systems Engineer; currently at Nykaa. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.56 recruiter response rate, 60-day notice, and 65 recruiter saves in 30d.
- Overall score: `0.610960`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (65 saves, 494 search appearances), recommendation or matching relevance (0.70), and strong responsiveness (0.56 response rate, 15.9h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 32 days, though not very recent, marked open to work, 0.56 recruiter response rate, 60-day notice period, and 65 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 5.5 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Nykaa, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Pinecone, Sentence Transformers, Embeddings, Information Retrieval, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.39, ranking=0.25, recommendation=0.70, evaluation=0.48, python=0.16, llm=0.30`
- Behavioral component scores: `activity=0.77, responsiveness=0.66, recruiter_attractiveness=0.97, logistics=0.79`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.62, product_fit=0.58, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3941, career_evidence_score=0.7969, semantic_plus_career=0.5980, behavior_multiplier=1.0216, behavioral_score=0.7938, honeypot_penalty=0.0000, final_score=0.6110`

### Rank 81: CAND_0094759

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 8.6 years of experience in Lead AI Engineer; currently at Meta. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.11 recruiter response rate, 30-day notice, and 5 recruiter saves in 30d. Main concern: weak recruiter responsiveness (0.11).
- Overall score: `0.610801`
- Top positive factors: good India hybrid logistics fit (Mumbai, Maharashtra, India), recent hands-on engineering evidence (0.94), short notice period (30 days), and healthy recruiter demand (5 saves, 146 search appearances)
- Top negative factors: weak recruiter responsiveness (0.11)
- Behavioral signal highlights: last active 147 days ago, 0.11 recruiter response rate, 30-day notice period, 5 recruiter saves in 30 days, and 146 recruiter search appearances in 30 days
- Career evidence highlights: Lead AI Engineer with 8.6 years of experience, product-company background at Meta, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Meta, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Semantic Search, Qdrant, Vector Search, FAISS, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.62, ranking=0.53, recommendation=0.00, evaluation=0.48, python=0.00, llm=0.38`
- Behavioral component scores: `activity=0.28, responsiveness=0.31, recruiter_attractiveness=0.69, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.65, product_fit=0.62, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.4319, career_evidence_score=0.8766, semantic_plus_career=0.6717, behavior_multiplier=0.9093, behavioral_score=0.4981, honeypot_penalty=0.0000, final_score=0.6108`

### Rank 82: CAND_0052335

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 6.4 years of experience in Applied ML Engineer; currently at Aganitha. Background fits a product or marketplace environment and matched skills include semantic search, sentence transformers, and learning to rank. Behavioral signals are solid with 0.79 recruiter response rate, 60-day notice, and 35 recruiter saves in 30d.
- Overall score: `0.607443`
- Top positive factors: recent hands-on engineering evidence (0.94), strong responsiveness (0.79 response rate, 27.3h avg response time), healthy recruiter demand (35 saves, 499 search appearances), and product/startup fit (0.68)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 55 days, though not very recent, marked open to work, 0.79 recruiter response rate, 60-day notice period, and 35 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 6.4 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Aganitha, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Semantic Search, Sentence Transformers, Learning to Rank, PyTorch
- Semantic component scores: `retrieval=0.44, ranking=0.47, recommendation=0.12, evaluation=0.14, python=0.07, llm=0.23`
- Behavioral component scores: `activity=0.76, responsiveness=0.82, recruiter_attractiveness=0.77, logistics=0.76`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.51, product_fit=0.68, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3272, career_evidence_score=0.8590, semantic_plus_career=0.5960, behavior_multiplier=1.0191, behavioral_score=0.7872, honeypot_penalty=0.0000, final_score=0.6074`

### Rank 83: CAND_0051292

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 5.2 years of experience in Applied ML Engineer; currently at Freshworks. Background fits a product or marketplace environment and matched skills include faiss, vector search, and elasticsearch. Behavioral signals are solid with 0.52 recruiter response rate, 30-day notice, and 9 recruiter saves in 30d.
- Overall score: `0.606355`
- Top positive factors: recent hands-on engineering evidence (1.00), product/startup fit (0.73), short notice period (30 days), and healthy recruiter demand (9 saves, 56 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 53 days, though not very recent, marked open to work, 0.52 recruiter response rate, 30-day notice period, and 9 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 5.2 years of experience, product-company background at Freshworks, recent role remains hands-on in engineering terms at current company Freshworks, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: FAISS, Vector Search, Elasticsearch, BentoML
- Semantic component scores: `retrieval=0.58, ranking=0.45, recommendation=0.12, evaluation=0.10, python=0.07, llm=0.30`
- Behavioral component scores: `activity=0.65, responsiveness=0.60, recruiter_attractiveness=0.67, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.73, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3603, career_evidence_score=0.8767, semantic_plus_career=0.6267, behavior_multiplier=0.9676, behavioral_score=0.6516, honeypot_penalty=0.0000, final_score=0.6064`

### Rank 84: CAND_0049538

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 5.8 years of experience in Applied ML Engineer; currently at Saarthi.ai. Matched skills include opensearch, vector search, and milvus. Behavioral signals are solid with 0.72 recruiter response rate, 30-day notice, 60 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.604514`
- Top positive factors: recent hands-on engineering evidence (1.00), strong responsiveness (0.72 response rate, 27.2h avg response time), healthy recruiter demand (60 saves, 996 search appearances), and short notice period (30 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 8 days, 0.72 recruiter response rate, 30-day notice period, 60 recruiter saves in 30 days, and 996 recruiter search appearances in 30 days
- Career evidence highlights: Applied ML Engineer with 5.8 years of experience, recent role remains hands-on in engineering terms at current company Saarthi.ai, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: ranking, recommendation, matched skills: OpenSearch, Vector Search, Milvus, Embeddings, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.33, ranking=0.51, recommendation=0.47, evaluation=0.19, python=0.23, llm=0.20`
- Behavioral component scores: `activity=0.45, responsiveness=0.83, recruiter_attractiveness=0.82, logistics=0.67`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.53, product_fit=0.43, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3710, career_evidence_score=0.8312, semantic_plus_career=0.6013, behavior_multiplier=1.0053, behavioral_score=0.7507, honeypot_penalty=0.0000, final_score=0.6045`

### Rank 85: CAND_0031593

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 7.8 years of experience in Search Engineer; currently at Genpact AI. Career history points to hands-on production ml ownership and matched skills include bm25, embeddings, and elasticsearch. Behavioral signals are solid with 0.58 recruiter response rate, 90-day notice, and 17 recruiter saves in 30d.
- Overall score: `0.603105`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (17 saves, 900 search appearances), strong responsiveness (0.58 response rate, 6.9h avg response time), and production ML evidence (0.61)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 77 days, though not very recent, marked open to work, 0.58 recruiter response rate, 90-day notice period, and 17 recruiter saves in 30 days
- Career evidence highlights: Search Engineer with 7.8 years of experience, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Genpact AI, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: BM25, Embeddings, Elasticsearch, Recommendation Systems, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.43, ranking=0.41, recommendation=0.56, evaluation=0.19, python=0.07, llm=0.16`
- Behavioral component scores: `activity=0.59, responsiveness=0.67, recruiter_attractiveness=0.94, logistics=0.74`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.61, product_fit=0.35, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3683, career_evidence_score=0.8323, semantic_plus_career=0.5996, behavior_multiplier=1.0059, behavioral_score=0.7523, honeypot_penalty=0.0000, final_score=0.6031`

### Rank 86: CAND_0070202

- Recruiter summary: Strong semantic alignment with retrieval, ranking, and recommendation requirements; 5.1 years of experience in Machine Learning Engineer; currently at BYJU'S. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.60 recruiter response rate, 90-day notice, 28 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.602802`
- Top positive factors: recent hands-on engineering evidence (0.94), healthy recruiter demand (28 saves, 450 search appearances), product/startup fit (0.72), and strong responsiveness (0.60 response rate, 11.5h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 15 days, 0.60 recruiter response rate, 90-day notice period, 28 recruiter saves in 30 days, and 450 recruiter search appearances in 30 days
- Career evidence highlights: Machine Learning Engineer with 5.1 years of experience, product-company background at BYJU'S, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company BYJU'S, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, recommendation, matched skills: Embeddings, Qdrant, Semantic Search, BM25, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.43, ranking=0.51, recommendation=0.31, evaluation=0.10, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.50, responsiveness=0.67, recruiter_attractiveness=0.76, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.55, product_fit=0.72, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3497, career_evidence_score=0.8737, semantic_plus_career=0.6164, behavior_multiplier=0.9779, behavioral_score=0.6788, honeypot_penalty=0.0000, final_score=0.6028`

### Rank 87: CAND_0089552

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.0 years of experience in Machine Learning Engineer; currently at Netflix. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.49 recruiter response rate, 120-day notice, and 50 recruiter saves in 30d. Main concern: long notice period (120 days).
- Overall score: `0.600277`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (50 saves, 383 search appearances), production ML evidence (0.63), and strong retrieval/search alignment (0.63)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 38 days, though not very recent, 0.49 recruiter response rate, 120-day notice period, 50 recruiter saves in 30 days, and 383 recruiter search appearances in 30 days
- Career evidence highlights: Machine Learning Engineer with 6.0 years of experience, product-company background at Netflix, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Netflix, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Weaviate, Qdrant, Semantic Search, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.63, ranking=0.29, recommendation=0.41, evaluation=0.29, python=0.00, llm=0.22`
- Behavioral component scores: `activity=0.46, responsiveness=0.44, recruiter_attractiveness=0.83, logistics=0.78`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.63, product_fit=0.55, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3840, career_evidence_score=0.8668, semantic_plus_career=0.6317, behavior_multiplier=0.9502, behavioral_score=0.6059, honeypot_penalty=0.0000, final_score=0.6003`

### Rank 88: CAND_0039754

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 16.2 years of experience in Senior Applied Scientist; currently at Meta. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.81 recruiter response rate, 30-day notice, 51 recruiter saves in 30d, and active in the last 30 days. Main concern: well above the target experience band.
- Overall score: `0.599076`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (51 saves, 541 search appearances), strong responsiveness (0.81 response rate, 38.5h avg response time), and good India hybrid logistics fit (Indore, Madhya Pradesh, India)
- Top negative factors: well above the target experience band
- Behavioral signal highlights: active in the last 21 days, marked open to work, 0.81 recruiter response rate, 30-day notice period, and 51 recruiter saves in 30 days
- Career evidence highlights: Senior Applied Scientist with 16.2 years of experience, product-company background at Meta, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Meta, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking, ranking evaluation, LLM tooling, matched skills: Qdrant, OpenSearch, BM25, Weaviate, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.74, ranking=0.70, recommendation=0.15, evaluation=0.48, python=0.07, llm=0.39`
- Behavioral component scores: `activity=0.70, responsiveness=0.96, recruiter_attractiveness=0.98, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=0.20, role_depth=1.00, production_ml=0.73, product_fit=0.56, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=0.8000, semantic_score=0.5476, career_evidence_score=0.7660, semantic_plus_career=0.7009, behavior_multiplier=1.0684, behavioral_score=0.9169, honeypot_penalty=0.0000, final_score=0.5991`

### Rank 89: CAND_0014440

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 6.4 years of experience in Recommendation Systems Engineer; currently at CRED. Background fits a product or marketplace environment and matched skills include elasticsearch, milvus, and faiss. Behavioral signals are solid with 0.64 recruiter response rate, 60-day notice, 33 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.598990`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (33 saves, 735 search appearances), and strong responsiveness (0.64 response rate, 14.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 25 days, marked open to work, 0.64 recruiter response rate, 60-day notice period, and 33 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.4 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: ranking, recommendation, matched skills: Elasticsearch, Milvus, FAISS, Qdrant, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.33, ranking=0.40, recommendation=0.70, evaluation=0.23, python=0.10, llm=0.07`
- Behavioral component scores: `activity=0.70, responsiveness=0.80, recruiter_attractiveness=0.99, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.60, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3497, career_evidence_score=0.7860, semantic_plus_career=0.5702, behavior_multiplier=1.0505, behavioral_score=0.8697, honeypot_penalty=0.0000, final_score=0.5990`

### Rank 90: CAND_0036184

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.0 years of experience in Recommendation Systems Engineer; currently at CRED. Background fits a product or marketplace environment and matched skills include faiss, semantic search, and embeddings. Behavioral signals are solid with 0.90 recruiter response rate, 30-day notice, 30 recruiter saves in 30d, and active in the last 30 days. Main concern: thin direct ranking evidence (0.15).
- Overall score: `0.598974`
- Top positive factors: healthy recruiter demand (30 saves, 971 search appearances), strong responsiveness (0.90 response rate, 52.3h avg response time), recent hands-on engineering evidence (0.77), and strong retrieval/search alignment (0.74)
- Top negative factors: thin direct ranking evidence (0.15)
- Behavioral signal highlights: active in the last 9 days, marked open to work, 0.90 recruiter response rate, 30-day notice period, and 30 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.0 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company CRED, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: FAISS, Semantic Search, Embeddings, Vector Search, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.74, ranking=0.15, recommendation=0.70, evaluation=0.00, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.99, responsiveness=0.90, recruiter_attractiveness=0.98, logistics=0.79`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.46, product_fit=0.58, ownership=0.70, recent_hands_on=0.77, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3859, career_evidence_score=0.7138, semantic_plus_career=0.5584, behavior_multiplier=1.0728, behavioral_score=0.9283, honeypot_penalty=0.0000, final_score=0.5990`

### Rank 91: CAND_0096172

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.2 years of experience in NLP Engineer; currently at Krutrim. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.47 recruiter response rate, 45-day notice, and 11 recruiter saves in 30d.
- Overall score: `0.598637`
- Top positive factors: good India hybrid logistics fit (Chennai, Tamil Nadu, India), recent hands-on engineering evidence (0.89), healthy recruiter demand (11 saves, 712 search appearances), and strong retrieval/search alignment (0.74)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 32 days, though not very recent, 0.47 recruiter response rate, 45-day notice period, 11 recruiter saves in 30 days, and 712 recruiter search appearances in 30 days
- Career evidence highlights: NLP Engineer with 5.2 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Krutrim, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: OpenSearch, Elasticsearch, Semantic Search, Sentence Transformers, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.74, ranking=0.25, recommendation=0.31, evaluation=0.10, python=0.07, llm=0.20`
- Behavioral component scores: `activity=0.53, responsiveness=0.58, recruiter_attractiveness=0.87, logistics=0.91`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.58, product_fit=0.61, ownership=0.83, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3675, career_evidence_score=0.8365, semantic_plus_career=0.6074, behavior_multiplier=0.9855, behavioral_score=0.6987, honeypot_penalty=0.0000, final_score=0.5986`

### Rank 92: CAND_0005538

- Recruiter summary: Strong semantic alignment with retrieval/search and ranking evaluation requirements; 5.9 years of experience in Senior AI Engineer; currently at Adobe. Background fits a product or marketplace environment and matched skills include information retrieval systems, python, and pytorch. Behavioral signals are solid with 0.81 recruiter response rate, 90-day notice, 20 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.598568`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (20 saves, 1147 search appearances), strong responsiveness (0.81 response rate, 28.4h avg response time), and product/startup fit (0.61)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 18 days, marked open to work, 0.81 recruiter response rate, 90-day notice period, and 20 recruiter saves in 30 days
- Career evidence highlights: Senior AI Engineer with 5.9 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Adobe, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking evaluation, matched skills: Information Retrieval Systems, Python, PyTorch, QLoRA, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.36, ranking=0.29, recommendation=0.19, evaluation=0.29, python=0.13, llm=0.23`
- Behavioral component scores: `activity=0.93, responsiveness=0.87, recruiter_attractiveness=0.95, logistics=0.70`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.61, ownership=1.00, recent_hands_on=1.00, tenure_fit=0.75`
- Score path: `stage1_gate=1.0000, semantic_score=0.2912, career_evidence_score=0.8598, semantic_plus_career=0.5652, behavior_multiplier=1.0590, behavioral_score=0.8920, honeypot_penalty=0.0000, final_score=0.5986`

### Rank 93: CAND_0081053

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 5.4 years of experience in NLP Engineer; currently at Glance. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.83 recruiter response rate, 90-day notice, and 40 recruiter saves in 30d. Main concern: Direct ranking-system evidence is thinner than the strongest profiles.
- Overall score: `0.596121`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (40 saves, 185 search appearances), good India hybrid logistics fit (Chandigarh, Chandigarh, India), and strong responsiveness (0.83 response rate, 21.6h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 65 days, though not very recent, marked open to work, 0.83 recruiter response rate, 90-day notice period, and 40 recruiter saves in 30 days
- Career evidence highlights: NLP Engineer with 5.4 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Glance, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Qdrant, Semantic Search, Weaviate, OpenSearch, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.42, ranking=0.20, recommendation=0.31, evaluation=0.41, python=0.15, llm=0.13`
- Behavioral component scores: `activity=0.52, responsiveness=0.83, recruiter_attractiveness=0.94, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.57, product_fit=0.61, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3098, career_evidence_score=0.8636, semantic_plus_career=0.5772, behavior_multiplier=1.0328, behavioral_score=0.8232, honeypot_penalty=0.0000, final_score=0.5961`

### Rank 94: CAND_0064904

- Recruiter summary: Strong semantic alignment with recommendation requirements; 4.9 years of experience in AI Engineer; currently at LinkedIn. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.78 recruiter response rate, 90-day notice, and 39 recruiter saves in 30d. Main concern: thin direct ranking evidence (0.14).
- Overall score: `0.595571`
- Top positive factors: good India hybrid logistics fit (Hyderabad, Telangana, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (39 saves, 942 search appearances), and strong responsiveness (0.78 response rate, 40.8h avg response time)
- Top negative factors: thin direct ranking evidence (0.14)
- Behavioral signal highlights: active in the last 79 days, though not very recent, marked open to work, 0.78 recruiter response rate, 90-day notice period, and 39 recruiter saves in 30 days
- Career evidence highlights: AI Engineer with 4.9 years of experience, product-company background at LinkedIn, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company LinkedIn, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: recommendation, ranking evaluation, Python stack, matched skills: Embeddings, Elasticsearch, Weaviate, Vector Search, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.34, ranking=0.14, recommendation=0.56, evaluation=0.41, python=0.29, llm=0.13`
- Behavioral component scores: `activity=0.68, responsiveness=0.88, recruiter_attractiveness=0.98, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.56, product_fit=0.57, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3144, career_evidence_score=0.8346, semantic_plus_career=0.5618, behavior_multiplier=1.0601, behavioral_score=0.8950, honeypot_penalty=0.0000, final_score=0.5956`

### Rank 95: CAND_0061655

- Recruiter summary: Strong semantic alignment with ranking and recommendation requirements; 4.6 years of experience in Machine Learning Engineer; currently at Krutrim. Background fits a product or marketplace environment and matched skills include pinecone, qdrant, and bm25. Behavioral signals are solid with 0.88 recruiter response rate, 15-day notice, 19 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.594780`
- Top positive factors: healthy recruiter demand (19 saves, 851 search appearances), recent hands-on engineering evidence (0.94), strong responsiveness (0.88 response rate, 47.8h avg response time), and short notice period (15 days)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 14 days, 0.88 recruiter response rate, 15-day notice period, 19 recruiter saves in 30 days, and 851 recruiter search appearances in 30 days
- Career evidence highlights: Machine Learning Engineer with 4.6 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Krutrim, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: ranking, recommendation, matched skills: Pinecone, Qdrant, BM25, OpenSearch, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.30, ranking=0.35, recommendation=0.58, evaluation=0.14, python=0.13, llm=0.13`
- Behavioral component scores: `activity=0.61, responsiveness=0.94, recruiter_attractiveness=1.00, logistics=0.79`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.53, product_fit=0.60, ownership=1.00, recent_hands_on=0.94, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3086, career_evidence_score=0.8276, semantic_plus_career=0.5609, behavior_multiplier=1.0604, behavioral_score=0.8959, honeypot_penalty=0.0000, final_score=0.5948`

### Rank 96: CAND_0000031

- Recruiter summary: Strong semantic alignment with recommendation requirements; 6.0 years of experience in Recommendation Systems Engineer; currently at Swiggy. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.91 recruiter response rate, 60-day notice, 13 recruiter saves in 30d, and active in the last 30 days.
- Overall score: `0.593093`
- Top positive factors: good India hybrid logistics fit (Hyderabad, Telangana, India), recent hands-on engineering evidence (1.00), healthy recruiter demand (13 saves, 778 search appearances), and strong responsiveness (0.91 response rate, 76.1h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 11 days, marked open to work, 0.91 recruiter response rate, 60-day notice period, and 13 recruiter saves in 30 days
- Career evidence highlights: Recommendation Systems Engineer with 6.0 years of experience, product-company background at Swiggy, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Swiggy, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: recommendation, matched skills: FAISS, Pinecone, Embeddings, Information Retrieval, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.33, ranking=0.34, recommendation=0.70, evaluation=0.15, python=0.13, llm=0.00`
- Behavioral component scores: `activity=0.83, responsiveness=0.83, recruiter_attractiveness=0.85, logistics=1.00`
- Career component scores: `title_fit=0.55, experience_fit=1.00, role_depth=1.00, production_ml=0.58, product_fit=0.75, ownership=1.00, recent_hands_on=1.00, tenure_fit=0.75`
- Score path: `stage1_gate=1.0000, semantic_score=0.3227, career_evidence_score=0.8158, semantic_plus_career=0.5682, behavior_multiplier=1.0437, behavioral_score=0.8519, honeypot_penalty=0.0000, final_score=0.5931`

### Rank 97: CAND_0006418

- Recruiter summary: Strong semantic alignment with ranking requirements; 5.7 years of experience in Machine Learning Engineer; currently at Verloop.io. Background fits a product or marketplace environment and matched skills include semantic search, embeddings, and weaviate. Behavioral signals are solid with 0.92 recruiter response rate, 60-day notice, and 9 recruiter saves in 30d.
- Overall score: `0.592831`
- Top positive factors: strong responsiveness (0.92 response rate, 47.0h avg response time), recent hands-on engineering evidence (0.89), good India hybrid logistics fit (Gurgaon, Haryana, India), and healthy recruiter demand (9 saves, 372 search appearances)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 65 days, though not very recent, marked open to work, 0.92 recruiter response rate, 60-day notice period, and 9 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 5.7 years of experience, career history shows solid product or marketplace exposure, recent role remains hands-on in engineering terms at current company Verloop.io, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: ranking, ranking evaluation, matched skills: Semantic Search, Embeddings, Weaviate, Elasticsearch, and profile text includes ranking-evaluation style terminology
- Semantic component scores: `retrieval=0.29, ranking=0.39, recommendation=0.12, evaluation=0.42, python=0.16, llm=0.04`
- Behavioral component scores: `activity=0.71, responsiveness=0.92, recruiter_attractiveness=0.79, logistics=0.88`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.54, product_fit=0.76, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.2906, career_evidence_score=0.8652, semantic_plus_career=0.5704, behavior_multiplier=1.0393, behavioral_score=0.8402, honeypot_penalty=0.0000, final_score=0.5928`

### Rank 98: CAND_0009691

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 6.2 years of experience in Applied ML Engineer; currently at LinkedIn. Career history points to hands-on production ml ownership and matched skills include pinecone, sentence transformers, and qdrant. Behavioral signals are solid with 0.64 recruiter response rate, 120-day notice, 7 recruiter saves in 30d, and active in the last 30 days. Main concern: thin direct ranking evidence (0.20).
- Overall score: `0.592314`
- Top positive factors: recent hands-on engineering evidence (1.00), healthy recruiter demand (7 saves, 425 search appearances), recommendation or matching relevance (0.68), and strong responsiveness (0.64 response rate, 72.1h avg response time)
- Top negative factors: thin direct ranking evidence (0.20) and long notice period (120 days)
- Behavioral signal highlights: active in the last 19 days, marked open to work, 0.64 recruiter response rate, 120-day notice period, and 7 recruiter saves in 30 days
- Career evidence highlights: Applied ML Engineer with 6.2 years of experience, product-company background at LinkedIn, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company LinkedIn, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, matched skills: Pinecone, Sentence Transformers, Qdrant, FAISS, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.48, ranking=0.20, recommendation=0.68, evaluation=0.20, python=0.13, llm=0.20`
- Behavioral component scores: `activity=0.86, responsiveness=0.65, recruiter_attractiveness=0.84, logistics=0.74`
- Career component scores: `title_fit=1.00, experience_fit=1.00, role_depth=1.00, production_ml=0.56, product_fit=0.45, ownership=1.00, recent_hands_on=1.00, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3483, career_evidence_score=0.8390, semantic_plus_career=0.5882, behavior_multiplier=1.0069, behavioral_score=0.7551, honeypot_penalty=0.0000, final_score=0.5923`

### Rank 99: CAND_0074225

- Recruiter summary: Strong semantic alignment with retrieval and recommendation requirements; 4.3 years of experience in Machine Learning Engineer; currently at Unacademy. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.91 recruiter response rate, 120-day notice, 53 recruiter saves in 30d, and active in the last 30 days. Main concern: long notice period (120 days).
- Overall score: `0.590877`
- Top positive factors: healthy recruiter demand (53 saves, 654 search appearances), recent hands-on engineering evidence (0.89), good India hybrid logistics fit (Vizag, Andhra Pradesh, India), and strong responsiveness (0.91 response rate, 34.1h avg response time)
- Top negative factors: long notice period (120 days)
- Behavioral signal highlights: active in the last 15 days, marked open to work, 0.91 recruiter response rate, 120-day notice period, and 53 recruiter saves in 30 days
- Career evidence highlights: Machine Learning Engineer with 4.3 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Unacademy, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, recommendation, ranking evaluation, matched skills: Semantic Search, Elasticsearch, Milvus, Qdrant, profile text includes ranking-evaluation style terminology, and recommendation or matching evidence appears alongside search signals
- Semantic component scores: `retrieval=0.43, ranking=0.25, recommendation=0.37, evaluation=0.25, python=0.07, llm=0.16`
- Behavioral component scores: `activity=0.91, responsiveness=0.86, recruiter_attractiveness=0.92, logistics=0.86`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.56, product_fit=0.59, ownership=0.94, recent_hands_on=0.89, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3071, career_evidence_score=0.8196, semantic_plus_career=0.5588, behavior_multiplier=1.0574, behavioral_score=0.8879, honeypot_penalty=0.0000, final_score=0.5909`

### Rank 100: CAND_0064270

- Recruiter summary: Strong semantic alignment with retrieval and ranking requirements; 4.2 years of experience in Applied ML Engineer; currently at Verloop.io. Career history points to hands-on production ml ownership and background fits a product or marketplace environment. Behavioral signals are solid with 0.82 recruiter response rate, 45-day notice, and 22 recruiter saves in 30d.
- Overall score: `0.587711`
- Top positive factors: good India hybrid logistics fit (Pune, Maharashtra, India), healthy recruiter demand (22 saves, 692 search appearances), recent hands-on engineering evidence (0.83), and strong responsiveness (0.82 response rate, 74.5h avg response time)
- Top negative factors: no major red flags after timeline and behavioral sanity checks
- Behavioral signal highlights: active in the last 76 days, though not very recent, 0.82 recruiter response rate, 45-day notice period, 22 recruiter saves in 30 days, and 692 recruiter search appearances in 30 days
- Career evidence highlights: Applied ML Engineer with 4.2 years of experience, career history shows solid product or marketplace exposure, career evidence suggests hands-on production ML ownership, recent role remains hands-on in engineering terms at current company Verloop.io, and descriptions show ownership, implementation, or delivery language
- Skill alignment highlights: aligned themes: retrieval/search, ranking and matched skills: Sentence Transformers, Embeddings, OpenSearch, Elasticsearch
- Semantic component scores: `retrieval=0.41, ranking=0.45, recommendation=0.12, evaluation=0.20, python=0.13, llm=0.13`
- Behavioral component scores: `activity=0.29, responsiveness=0.80, recruiter_attractiveness=0.90, logistics=1.00`
- Career component scores: `title_fit=1.00, experience_fit=0.85, role_depth=1.00, production_ml=0.55, product_fit=0.77, ownership=0.87, recent_hands_on=0.83, tenure_fit=1.00`
- Score path: `stage1_gate=1.0000, semantic_score=0.3171, career_evidence_score=0.8335, semantic_plus_career=0.5792, behavior_multiplier=1.0146, behavioral_score=0.7753, honeypot_penalty=0.0000, final_score=0.5877`

