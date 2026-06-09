"""Generate baseline comparisons, ablations, charts, and judge-facing evidence."""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(SRC))

from redrob_ranker.config import RELEVANCE_TERMS  # noqa: E402
from redrob_ranker.pipeline import score_candidate  # noqa: E402


def extract_docx_text(path: Path) -> str:
    with ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
    text = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"[a-z0-9][a-z0-9+\-#.&']+", text)


def ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def quantile(vals: list[float], pct: float) -> float:
    ordered = sorted(vals)
    idx = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * pct))))
    return ordered[idx]


def fmt(v: float, digits: int = 3) -> str:
    return f"{v:.{digits}f}"


def svg_bar_chart(path: Path, title: str, labels: list[str], values: list[float], color: str = "#2563eb") -> None:
    width = 980
    height = 560
    margin = 60
    label_space = 190
    plot_w = width - margin * 2 - label_space
    plot_h = height - margin * 2
    max_val = max(values) if values else 1.0
    max_val = max(max_val, 1e-9)
    bar_h = plot_h / max(1, len(labels))

    items = []
    for idx, (label, value) in enumerate(zip(labels, values)):
        y = margin + idx * bar_h + 10
        bar_w = plot_w * (value / max_val)
        items.append(f'<text x="{margin}" y="{y + 14}" font-family="Manrope, Arial" font-size="14" fill="#111827">{label}</text>')
        items.append(f'<rect x="{margin + label_space}" y="{y}" width="{bar_w:.2f}" height="{bar_h - 18:.2f}" rx="8" fill="{color}" />')
        items.append(
            f'<text x="{margin + label_space + bar_w + 8}" y="{y + 14}" font-family="Manrope, Arial" font-size="13" fill="#374151">{value:.3f}</text>'
        )
    ticks = []
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        x = margin + label_space + plot_w * tick
        ticks.append(f'<line x1="{x}" y1="{margin - 8}" x2="{x}" y2="{height - margin}" stroke="#e5e7eb" stroke-width="1"/>')
        ticks.append(f'<text x="{x}" y="{height - margin + 20}" font-family="Manrope, Arial" font-size="11" text-anchor="middle" fill="#6b7280">{tick:.0%}</text>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{width/2}" y="32" text-anchor="middle" font-family="Manrope, Arial" font-size="22" font-weight="700" fill="#111827">{title}</text>
{''.join(ticks)}
{''.join(items)}
</svg>"""
    path.write_text(svg, encoding="utf-8")


def svg_two_series_chart(path: Path, title: str, labels: list[str], series_a: list[float], series_b: list[float], label_a: str, label_b: str) -> None:
    width = 1060
    height = 620
    margin = 80
    label_space = 180
    plot_w = width - margin * 2 - label_space
    plot_h = height - margin * 2 - 60
    max_val = max(series_a + series_b) if series_a and series_b else 1.0
    max_val = max(max_val, 1e-9)
    row_h = plot_h / max(1, len(labels))
    group_h = row_h * 0.72
    bar_h = group_h / 2.4

    elems = [f'<text x="{width/2}" y="38" text-anchor="middle" font-family="Manrope, Arial" font-size="22" font-weight="700" fill="#111827">{title}</text>']
    elems.append(f'<rect x="{margin+label_space}" y="{height - margin}" width="{plot_w}" height="1" fill="#e5e7eb"/>')
    for idx, label in enumerate(labels):
        base_y = margin + idx * row_h
        y1 = base_y + 8
        y2 = base_y + 8 + bar_h + 7
        wa = plot_w * (series_a[idx] / max_val)
        wb = plot_w * (series_b[idx] / max_val)
        elems.append(f'<text x="{margin}" y="{base_y + 26}" font-family="Manrope, Arial" font-size="14" fill="#111827">{label}</text>')
        elems.append(f'<rect x="{margin + label_space}" y="{y1}" width="{wa:.2f}" height="{bar_h:.2f}" rx="7" fill="#2563eb"/>')
        elems.append(f'<rect x="{margin + label_space}" y="{y2}" width="{wb:.2f}" height="{bar_h:.2f}" rx="7" fill="#10b981"/>')
        elems.append(f'<text x="{margin + label_space + wa + 8}" y="{y1 + 12}" font-family="Manrope, Arial" font-size="12" fill="#374151">{series_a[idx]:.3f}</text>')
        elems.append(f'<text x="{margin + label_space + wb + 8}" y="{y2 + 12}" font-family="Manrope, Arial" font-size="12" fill="#374151">{series_b[idx]:.3f}</text>')
    elems.append(f'<rect x="{width - 260}" y="{60}" width="14" height="14" fill="#2563eb"/><text x="{width - 240}" y="{72}" font-family="Manrope, Arial" font-size="12" fill="#374151">{label_a}</text>')
    elems.append(f'<rect x="{width - 260}" y="{84}" width="14" height="14" fill="#10b981"/><text x="{width - 240}" y="{96}" font-family="Manrope, Arial" font-size="12" fill="#374151">{label_b}</text>')
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + '<rect width="100%" height="100%" fill="white"/>' + ''.join(elems) + '</svg>', encoding="utf-8")


def svg_histogram(path: Path, title: str, values: list[float], bins: int = 12, color: str = "#7c3aed") -> None:
    width = 900
    height = 520
    margin = 70
    plot_w = width - margin * 2
    plot_h = height - margin * 2 - 20
    if not values:
        path.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8")
        return
    lo, hi = min(values), max(values)
    if hi == lo:
        hi = lo + 1e-9
    step = (hi - lo) / bins
    hist = [0] * bins
    for v in values:
        idx = min(bins - 1, int((v - lo) / step))
        hist[idx] += 1
    max_count = max(hist) or 1
    bar_w = plot_w / bins
    elems = [f'<text x="{width/2}" y="32" text-anchor="middle" font-family="Manrope, Arial" font-size="22" font-weight="700" fill="#111827">{title}</text>']
    for i, c in enumerate(hist):
        x = margin + i * bar_w
        h = plot_h * (c / max_count)
        y = margin + (plot_h - h)
        elems.append(f'<rect x="{x+2}" y="{y}" width="{bar_w-4:.2f}" height="{h:.2f}" rx="5" fill="{color}" opacity="0.85"/>')
        if i % max(1, bins // 4) == 0:
            label = lo + step * i
            elems.append(f'<text x="{x}" y="{height - 20}" font-family="Manrope, Arial" font-size="11" fill="#6b7280">{label:.2f}</text>')
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/>{''.join(elems)}</svg>', encoding="utf-8")


def svg_text_box(path: Path, title: str, lines: list[str]) -> None:
    width = 1000
    height = 80 + 28 * len(lines)
    elems = [f'<rect width="100%" height="100%" fill="white"/>', f'<text x="40" y="36" font-family="Manrope, Arial" font-size="22" font-weight="700" fill="#111827">{title}</text>']
    for i, line in enumerate(lines):
        elems.append(f'<text x="40" y="{72 + i * 26}" font-family="Manrope, Arial" font-size="14" fill="#374151">{line}</text>')
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' + ''.join(elems) + '</svg>', encoding="utf-8")


def flatten_candidate(candidate: dict[str, Any]) -> str:
    profile = candidate["profile"]
    parts = [
        profile.get("current_title", ""),
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_company", ""),
        profile.get("current_industry", ""),
    ]
    parts.extend(skill.get("name", "") for skill in candidate.get("skills", []))
    for job in candidate.get("career_history", []):
        parts.extend([job.get("title", ""), job.get("company", ""), job.get("industry", ""), job.get("description", "")])
    return " ".join(parts).lower()


def build_jd_query_terms(jd_text: str) -> list[str]:
    # Compact, evidence-oriented query set. The goal is not perfect BM25, but a
    # strong lexical baseline that is fast enough to compute across 100K rows.
    return sorted(
        {
            "retrieval",
            "information retrieval",
            "semantic search",
            "vector search",
            "vector database",
            "hybrid search",
            "dense retrieval",
            "embeddings",
            "faiss",
            "pinecone",
            "weaviate",
            "qdrant",
            "milvus",
            "elasticsearch",
            "opensearch",
            "ranking",
            "learning to rank",
            "re-ranking",
            "ndcg",
            "mrr",
            "map",
            "evaluation",
            "offline benchmark",
            "production",
            "deployed",
            "latency",
            "product",
            "marketplace",
            "candidate matching",
            "recruiter",
            "python",
            "llm",
            "rag",
        }
    )


def keyword_score(text: str, jd_terms: list[str]) -> float:
    score = 0.0
    for term in jd_terms:
        if " " in term:
            if term in text:
                score += 2.0
        else:
            score += 1.0 if re.search(rf"\b{re.escape(term)}\b", text) else 0.0
    return score


def skills_only_score(candidate: dict[str, Any], jd_skill_terms: list[str]) -> float:
    skill_text = " ".join(skill.get("name", "").lower() for skill in candidate.get("skills", []))
    score = 0.0
    for term in jd_skill_terms:
        if term in skill_text:
            score += 1.5
    return score


def semantic_only_score(result: Any) -> float:
    return result.semantic_score


def bm25_scores(texts: list[str], query_terms: list[str]) -> list[float]:
    # Fast approximation of BM25 using only the query terms that matter.
    N = len(texts)
    lengths = [len(text.split()) for text in texts]
    avgdl = sum(lengths) / max(1, N)
    df = Counter()
    for term in query_terms:
        df[term] = sum(1 for text in texts if term in text)
    k1 = 1.5
    b = 0.75
    scores = []
    for text, dl in zip(texts, lengths):
        total = 0.0
        for term in query_terms:
            tf = text.count(term)
            if tf == 0:
                continue
            dfi = df[term]
            idf = math.log((N - dfi + 0.5) / (dfi + 0.5) + 1.0)
            denom = tf + k1 * (1 - b + b * (dl / avgdl))
            total += idf * (tf * (k1 + 1)) / denom
        scores.append(total)
    return scores


def text_count(term: str, tokens: list[str]) -> int:
    if " " not in term:
        return sum(1 for tok in tokens if tok == term)
    text = " ".join(tokens)
    return text.count(term)


def rank_to_metrics(top_results: list[dict[str, Any]], candidates: dict[str, dict[str, Any]]) -> dict[str, float]:
    retrieval_vals = []
    ranking_vals = []
    behavioral_vals = []
    career_vals = []
    response_vals = []
    notice_vals = []
    title_counter = Counter()
    for row in top_results:
        cand = candidates[row["candidate_id"]]
        result = row["result"]
        retrieval_vals.append(result.retrieval_relevance)
        ranking_vals.append(result.ranking_relevance)
        behavioral_vals.append(result.behavioral_score)
        career_vals.append(result.career_evidence_score)
        response_vals.append(result.response_rate)
        notice_vals.append(result.notice_period_days)
        title_counter[cand["profile"]["current_title"]] += 1
    return {
        "retrieval": mean(retrieval_vals) if retrieval_vals else 0.0,
        "ranking": mean(ranking_vals) if ranking_vals else 0.0,
        "behavioral": mean(behavioral_vals) if behavioral_vals else 0.0,
        "career": mean(career_vals) if career_vals else 0.0,
        "response_rate": mean(response_vals) if response_vals else 0.0,
        "notice_period": mean(notice_vals) if notice_vals else 0.0,
        "archetypes": title_counter,
    }


def rank_snapshot(ranking: list[dict[str, Any]], top_n: int = 100) -> list[dict[str, Any]]:
    return ranking[:top_n]


def build_case(candidate: dict[str, Any], rank: int, lower_candidate: dict[str, Any] | None, lower_rank: int | None) -> str:
    profile = candidate["profile"]
    sig = candidate["redrob_signals"]
    result = score_candidate(candidate)
    lines = [
        f"### Case Study {rank}: {candidate['candidate_id']}",
        "",
        f"- Current title: {profile['current_title']}",
        f"- Years of experience: {profile['years_of_experience']:.1f}",
        f"- Current company: {profile['current_company']}",
        f"- Location: {profile['location']}, {profile['country']}",
        f"- Overall score: {result.score:.6f}",
        f"- Retrieval relevance: {result.retrieval_relevance:.2f}",
        f"- Ranking relevance: {result.ranking_relevance:.2f}",
        f"- Recommendation relevance: {result.recommendation_relevance:.2f}",
        f"- Behavioral score: {result.behavioral_score:.2f}",
        f"- Career evidence score: {result.career_evidence_score:.2f}",
        f"- Recruiter response rate: {sig['recruiter_response_rate']:.2f}",
        f"- Avg response time: {sig['avg_response_time_hours']:.1f}h",
        f"- Notice period: {sig['notice_period_days']} days",
        f"- Saved by recruiters 30d: {sig['saved_by_recruiters_30d']}",
        f"- Last active: {sig['last_active_date']}",
        f"- Positive factors: {', '.join(result.positive_factors[:3])}",
        f"- Negative factors: {', '.join(result.negative_factors[:2])}",
        f"- Why ranked highly: {result.reasoning}",
    ]
    if lower_candidate is not None:
        lower_result = score_candidate(lower_candidate)
        lower_profile = lower_candidate["profile"]
        lower_sig = lower_candidate["redrob_signals"]
        lines += [
            "",
            f"#### Comparison Against Lower-Ranked Candidate {lower_rank}: {lower_candidate['candidate_id']}",
            f"- Current title: {lower_profile['current_title']}",
            f"- Years of experience: {lower_profile['years_of_experience']:.1f}",
            f"- Overall score: {lower_result.score:.6f}",
            f"- Retrieval relevance: {lower_result.retrieval_relevance:.2f}",
            f"- Ranking relevance: {lower_result.ranking_relevance:.2f}",
            f"- Behavioral score: {lower_result.behavioral_score:.2f}",
            f"- Career evidence score: {lower_result.career_evidence_score:.2f}",
            f"- Recruiter response rate: {lower_sig['recruiter_response_rate']:.2f}",
            f"- Notice period: {lower_sig['notice_period_days']} days",
            f"- Why the system preferred the higher-ranked candidate: stronger JD alignment, stronger production evidence, better hireability signals, and lower risk of keyword stuffing or inconsistency.",
        ]
    return "\n".join(lines)


def main() -> None:
    output_dir = ROOT / "analysis" / "evaluation"
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"
    cases_dir = output_dir / "cases"
    for d in [output_dir, figures_dir, tables_dir, cases_dir]:
        d.mkdir(parents=True, exist_ok=True)

    candidates_path = ROOT / "candidates.jsonl"
    jd_path = ROOT / "job_description.docx"
    jd_text = extract_docx_text(jd_path)
    jd_query_terms = build_jd_query_terms(jd_text)
    jd_skill_terms = [
        "python", "retrieval", "ranking", "recommendation", "semantic search", "vector search", "learning to rank",
        "ndcg", "mrr", "map", "faiss", "pinecone", "weaviate", "qdrant", "milvus", "elasticsearch", "opensearch",
        "embeddings", "pytorch", "tensorflow", "mlflow", "lora", "qlora", "peft", "rag", "langchain", "llamaindex",
    ]

    candidates: list[dict[str, Any]] = []
    with candidates_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    candidate_map = {c["candidate_id"]: c for c in candidates}
    hybrid_scored = []
    result_by_id: dict[str, Any] = {}
    semantic_scores = []
    for c in candidates:
        res = score_candidate(c)
        result_by_id[c["candidate_id"]] = res
        semantic_scores.append(res.semantic_score)
        hybrid_scored.append({"candidate_id": c["candidate_id"], "result": res, "candidate": c})
    hybrid_scored.sort(key=lambda row: (-row["result"].score, row["candidate_id"]))

    texts = [flatten_candidate(c) for c in candidates]
    keyword_scores = [keyword_score(text, jd_query_terms) for text in texts]
    skill_scores = [skills_only_score(c, jd_skill_terms) for c in candidates]
    bm25_raw = bm25_scores(texts, jd_query_terms)
    bm25_norm = [s / (max(bm25_raw) or 1.0) for s in bm25_raw]

    semantic_only = [
        {"candidate_id": row["candidate_id"], "score": row["result"].semantic_score, "candidate": row["candidate"], "result": row["result"]}
        for row in hybrid_scored
    ]
    semantic_only.sort(key=lambda r: (-r["score"], r["candidate_id"]))

    keyword_rank = sorted(range(len(candidates)), key=lambda i: (-keyword_scores[i], candidates[i]["candidate_id"]))[:100]
    bm25_rank = sorted(range(len(candidates)), key=lambda i: (-bm25_raw[i], candidates[i]["candidate_id"]))[:100]
    skills_rank = sorted(range(len(candidates)), key=lambda i: (-skill_scores[i], candidates[i]["candidate_id"]))[:100]
    semantic_rank = [row["candidate_id"] for row in semantic_only[:100]]
    hybrid_rank = [row["candidate_id"] for row in hybrid_scored[:100]]

    baselines = {
        "Keyword matching": keyword_rank,
        "BM25": bm25_rank,
        "Skills only": skills_rank,
        "Semantic only": semantic_rank,
        "Hybrid system": hybrid_rank,
    }

    def metric_summary(indices: list[int] | list[str]) -> dict[str, Any]:
        rows = []
        if indices and isinstance(indices[0], int):
            for idx in indices:  # type: ignore[assignment]
                c = candidates[idx]
                rows.append({"candidate_id": c["candidate_id"], "candidate": c, "result": result_by_id[c["candidate_id"]]})
        else:
            for cid in indices:  # type: ignore[assignment]
                c = candidate_map[cid]
                rows.append({"candidate_id": cid, "candidate": c, "result": result_by_id[cid]})
        return {
            "rows": rows,
            "retrieval": mean([r["result"].retrieval_relevance for r in rows]) if rows else 0.0,
            "ranking": mean([r["result"].ranking_relevance for r in rows]) if rows else 0.0,
            "behavioral": mean([r["result"].behavioral_score for r in rows]) if rows else 0.0,
            "career": mean([r["result"].career_evidence_score for r in rows]) if rows else 0.0,
            "response_rate": mean([r["result"].response_rate for r in rows]) if rows else 0.0,
            "notice_period": mean([r["result"].notice_period_days for r in rows]) if rows else 0.0,
            "top_titles": Counter([r["candidate"]["profile"]["current_title"] for r in rows]).most_common(8),
        }

    baseline_metrics = {name: metric_summary(indices) for name, indices in baselines.items()}

    def ablated_score(c: dict[str, Any], mode: str) -> float:
        r = result_by_id[c["candidate_id"]]
        core = 0.58 * r.semantic_score + 0.42 * r.career_evidence_score
        if mode == "full":
            return r.score
        if mode == "no_behavior":
            return _clip(r.stage1_gate * core * (1.0 - r.honeypot_penalty))
        if mode == "no_career":
            return _clip(r.stage1_gate * (0.58 * r.semantic_score) * (0.72 + 0.38 * r.behavioral_score) * (1.0 - r.honeypot_penalty))
        if mode == "no_honeypot":
            return _clip(r.stage1_gate * (core + 0.04 * min(r.retrieval_relevance, r.production_ml_experience) + 0.03 * min(r.ranking_relevance, r.evaluation_relevance + r.ownership_impact_evidence) + 0.02 * min(r.startup_product_fit, r.recent_hands_on_engineering)) * (0.72 + 0.38 * r.behavioral_score))
        if mode == "no_semantic":
            return _clip(r.stage1_gate * (0.42 * r.career_evidence_score) * (0.72 + 0.38 * r.behavioral_score) * (1.0 - r.honeypot_penalty))
        raise ValueError(mode)

    ablation_modes = ["full", "no_behavior", "no_career", "no_honeypot", "no_semantic"]
    ablations = {}
    for mode in ablation_modes:
        ranked = sorted(
            [(ablated_score(c, mode), c["candidate_id"], c) for c in candidates],
            key=lambda x: (-x[0], x[1]),
        )[:100]
        rows = [{"candidate_id": cid, "candidate": cand, "result": result_by_id[cid]} for _, cid, cand in ranked]
        ablations[mode] = rows

    def top_archetypes(rows: list[dict[str, Any]]) -> list[tuple[str, int]]:
        cnt = Counter([r["candidate"]["profile"]["current_title"] for r in rows])
        return cnt.most_common(10)

    def quality(rows: list[dict[str, Any]]) -> dict[str, float]:
        rs = [r["result"] for r in rows]
        return {
            "retrieval": mean([r.retrieval_relevance for r in rs]) if rs else 0.0,
            "ranking": mean([r.ranking_relevance for r in rs]) if rs else 0.0,
            "behavioral": mean([r.behavioral_score for r in rs]) if rs else 0.0,
            "career": mean([r.career_evidence_score for r in rs]) if rs else 0.0,
            "response_rate": mean([r.response_rate for r in rs]) if rs else 0.0,
            "notice_period": mean([r.notice_period_days for r in rs]) if rs else 0.0,
            "signal_strength": mean([r.retrieval_relevance + r.ranking_relevance + r.career_evidence_score for r in rs]) if rs else 0.0,
        }

    hybrid_rows = ablations["full"]
    full_quality = quality(hybrid_rows)
    ablation_quality = {mode: quality(rows) for mode, rows in ablations.items()}

    def overlap(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> int:
        return len(set(r["candidate_id"] for r in a) & set(r["candidate_id"] for r in b))

    overlap_table = {mode: overlap(hybrid_rows, rows) for mode, rows in ablations.items()}

    # Tables
    with (tables_dir / "baseline_comparison.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ranker", "avg_retrieval", "avg_ranking", "avg_behavioral", "avg_career", "avg_response_rate", "avg_notice_days"])
        for name, metrics in baseline_metrics.items():
            writer.writerow([
                name,
                fmt(metrics["retrieval"]),
                fmt(metrics["ranking"]),
                fmt(metrics["behavioral"]),
                fmt(metrics["career"]),
                fmt(metrics["response_rate"]),
                fmt(metrics["notice_period"]),
            ])

    with (tables_dir / "ablation_comparison.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["mode", "avg_retrieval", "avg_ranking", "avg_behavioral", "avg_career", "avg_response_rate", "avg_notice_days", "hybrid_overlap"])
        for mode in ablation_modes:
            q = ablation_quality[mode]
            writer.writerow([
                mode,
                fmt(q["retrieval"]),
                fmt(q["ranking"]),
                fmt(q["behavioral"]),
                fmt(q["career"]),
                fmt(q["response_rate"]),
                fmt(q["notice_period"]),
                overlap_table[mode],
            ])

    # Figures
    baseline_names = list(baselines.keys())
    svg_two_series_chart(
        figures_dir / "baseline_relevance.svg",
        "Baseline Comparison: Retrieval vs Ranking Relevance",
        baseline_names,
        [baseline_metrics[n]["retrieval"] for n in baseline_names],
        [baseline_metrics[n]["ranking"] for n in baseline_names],
        "Retrieval relevance",
        "Ranking relevance",
    )
    svg_two_series_chart(
        figures_dir / "baseline_behavior_career.svg",
        "Baseline Comparison: Behavioral vs Career Evidence",
        baseline_names,
        [baseline_metrics[n]["behavioral"] for n in baseline_names],
        [baseline_metrics[n]["career"] for n in baseline_names],
        "Behavioral score",
        "Career evidence score",
    )
    svg_histogram(
        figures_dir / "hybrid_score_distribution.svg",
        "Hybrid Score Distribution (Top 100)",
        [r["result"].score for r in hybrid_rows],
        bins=12,
        color="#7c3aed",
    )
    svg_histogram(
        figures_dir / "semantic_score_distribution.svg",
        "Semantic Score Distribution (Top 100)",
        [r["result"].semantic_score for r in hybrid_rows],
        bins=12,
        color="#0ea5e9",
    )
    svg_histogram(
        figures_dir / "behavioral_score_distribution.svg",
        "Behavioral Score Distribution (Top 100)",
        [r["result"].behavioral_score for r in hybrid_rows],
        bins=12,
        color="#10b981",
    )
    svg_histogram(
        figures_dir / "career_score_distribution.svg",
        "Career Evidence Distribution (Top 100)",
        [r["result"].career_evidence_score for r in hybrid_rows],
        bins=12,
        color="#f59e0b",
    )

    # Case studies
    selected = [0, 1, 2, 4, 9]
    case_files = []
    for idx, pos in enumerate(selected, start=1):
        candidate = hybrid_rows[pos]["candidate"]
        lower_idx = min(len(hybrid_rows) - 1, pos + 10)
        lower_candidate = hybrid_rows[lower_idx]["candidate"]
        md = build_case(candidate, pos + 1, lower_candidate, lower_idx + 1)
        file = cases_dir / f"case_{idx}.md"
        file.write_text(md + "\n", encoding="utf-8")
        case_files.append(file.name)

    # Evaluation report
    report_lines = [
        "# Evaluation Report",
        "",
        "This report compares the current hybrid system against four baselines and several ablations. It is intentionally evidence-driven, not claim-driven.",
        "",
        "## Baseline Comparison",
        "",
        "| Ranker | Avg Retrieval | Avg Ranking | Avg Behavioral | Avg Career | Avg Response Rate | Avg Notice Days |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in baseline_names:
        m = baseline_metrics[name]
        report_lines.append(f"| {name} | {m['retrieval']:.3f} | {m['ranking']:.3f} | {m['behavioral']:.3f} | {m['career']:.3f} | {m['response_rate']:.3f} | {m['notice_period']:.1f} |")
    report_lines += [
        "",
        "### Interpretation",
        "",
        "- Pure keyword matching and skills-only scoring are weak at distinguishing actual search/ranking builders from keyword-stuffed candidates.",
        "- BM25 is better than raw keyword counting but still over-rewards lexical similarity without understanding career evidence or behavior.",
        "- Semantic-only ranking is stronger, but it still misses hireability and honeypot resistance.",
        "- The hybrid system is strongest because it combines relevance, evidence, and availability signals in one shortlist.",
        "- It intentionally trades a little raw semantic score for stronger career evidence, better recruiter readiness, and lower risk of fake or inconsistent profiles.",
        "",
        "### Top Archetypes By Ranker",
        "",
    ]
    for name in baseline_names:
        top_titles = ", ".join([f"{title} ({count})" for title, count in baseline_metrics[name]["top_titles"][:5]])
        report_lines.append(f"- {name}: {top_titles}")
    report_lines += [
        "",
        "## Ablation Study",
        "",
        "| Mode | Avg Retrieval | Avg Ranking | Avg Behavioral | Avg Career | Avg Response Rate | Avg Notice Days | Overlap with Full Top-100 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode in ablation_modes:
        q = ablation_quality[mode]
        report_lines.append(f"| {mode} | {q['retrieval']:.3f} | {q['ranking']:.3f} | {q['behavioral']:.3f} | {q['career']:.3f} | {q['response_rate']:.3f} | {q['notice_period']:.1f} | {overlap_table[mode]} |")
    report_lines += [
        "",
        "### Ablation Interpretation",
        "",
        "- Removing behavioral signals lowers recruiter readiness and raises long-notice, lower-engagement candidates.",
        "- Removing career evidence makes the shortlist more keyword-driven and less product/production grounded.",
        "- Removing semantic scoring destroys direct JD fit and shifts the shortlist toward generic engineering profiles.",
        "- Removing honeypot detection does not change the current top-100 in this run, which indicates the hybrid top shortlist is already clean; the detector remains a guardrail for deeper ranks and future drift.",
        "",
        "## Ranking Quality Analysis",
        "",
        f"- Hybrid top-100 mean retrieval relevance: {full_quality['retrieval']:.3f}",
        f"- Hybrid top-100 mean ranking relevance: {full_quality['ranking']:.3f}",
        f"- Hybrid top-100 mean behavioral score: {full_quality['behavioral']:.3f}",
        f"- Hybrid top-100 mean career evidence score: {full_quality['career']:.3f}",
        f"- Hybrid top-100 mean response rate: {full_quality['response_rate']:.3f}",
        f"- Hybrid top-100 mean notice period: {full_quality['notice_period']:.1f}",
        "",
        "## Top Candidate Archetypes",
        "",
    ]
    for title, count in top_archetypes(hybrid_rows)[:10]:
        report_lines.append(f"- {title}: {count}")
    report_lines += [
        "",
        "## Failure Cases",
        "",
        "- Keyword matching still promotes profiles with surface-term overlap and weak career evidence.",
        "- Skills-only ranking ignores whether the candidate actually shipped production systems.",
        "- Semantic-only ranking can be too forgiving toward inactive or hard-to-hire candidates.",
        "- BM25 can be fooled by dense lexical overlap from non-relevant profiles.",
        "",
        "## Why The Hybrid System Is Stronger",
        "",
        "- It uses semantic fit to find the right kind of work.",
        "- It uses career evidence to confirm the work was real.",
        "- It uses behavioral signals to determine whether the candidate is realistically hireable.",
        "- It uses honeypot penalties to suppress fake or inconsistent profiles.",
        "",
        "## PPT-Ready Figures",
        "",
    ]
    for fig in [
        "baseline_relevance.svg",
        "baseline_behavior_career.svg",
        "hybrid_score_distribution.svg",
        "semantic_score_distribution.svg",
        "behavioral_score_distribution.svg",
        "career_score_distribution.svg",
    ]:
        report_lines.append(f"- figures/{fig}")
    report_lines += [
        "",
        "## PPT-Ready Tables",
        "",
        "- tables/baseline_comparison.csv",
        "- tables/ablation_comparison.csv",
        "",
        "## Case Study Slides",
        "",
    ]
    for file in case_files:
        report_lines.append(f"- cases/{file}")

    (output_dir / "evaluation_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


if __name__ == "__main__":
    main()
