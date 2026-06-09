"""Core ranking pipeline."""

from __future__ import annotations

import csv
import heapq
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import (
    ADJACENT_SIGNAL_TITLES,
    ARCHITECTURE_ONLY_TERMS,
    BEHAVIOR_QUANTILES,
    CONSULTING_COMPANIES,
    HANDS_ON_TERMS,
    HIGH_SIGNAL_TITLES,
    NON_TECHNICAL_TITLES,
    OWNERSHIP_TERMS,
    PREFERRED_COUNTRY,
    PRODUCT_BRANDS,
    PRODUCT_INDUSTRY_KEYWORDS,
    REFERENCE_DATE,
    RELEVANCE_TERMS,
    RESEARCH_TERMS,
    STAGE7_WEIGHTS,
    STARTUP_SIZE_BUCKETS,
    TIER1_INDIA_CITY_KEYWORDS,
)


@dataclass
class CandidateResult:
    candidate_id: str
    rank: int = 0
    score: float = 0.0
    reasoning: str = ""
    current_title: str = ""
    current_company: str = ""
    location: str = ""
    country: str = ""
    years_of_experience: float = 0.0
    stage1_gate: float = 1.0
    stage1_flags: list[str] = field(default_factory=list)
    semantic_score: float = 0.0
    behavioral_score: float = 0.0
    career_evidence_score: float = 0.0
    honeypot_penalty: float = 0.0
    honeypot_flags: list[str] = field(default_factory=list)
    retrieval_relevance: float = 0.0
    ranking_relevance: float = 0.0
    recommendation_relevance: float = 0.0
    production_ml_experience: float = 0.0
    startup_product_fit: float = 0.0
    ownership_impact_evidence: float = 0.0
    recent_hands_on_engineering: float = 0.0
    recruiter_attractiveness: float = 0.0
    candidate_responsiveness: float = 0.0
    evaluation_relevance: float = 0.0
    python_strength: float = 0.0
    location_fit: float = 0.0
    title_fit: float = 0.0
    experience_fit: float = 0.0
    product_depth: float = 0.0
    role_depth: float = 0.0
    tenure_fit: float = 0.0
    llm_stack_score: float = 0.0
    matched_skills: list[str] = field(default_factory=list)
    matched_themes: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    semantic_components: dict[str, float] = field(default_factory=dict)
    behavioral_components: dict[str, float] = field(default_factory=dict)
    career_components: dict[str, float] = field(default_factory=dict)
    score_breakdown: dict[str, float] = field(default_factory=dict)
    positive_factors: list[str] = field(default_factory=list)
    negative_factors: list[str] = field(default_factory=list)
    behavioral_highlights: list[str] = field(default_factory=list)
    career_highlights: list[str] = field(default_factory=list)
    skill_alignment_highlights: list[str] = field(default_factory=list)
    response_rate: float = 0.0
    avg_response_time_hours: float = 0.0
    notice_period_days: int = 0
    open_to_work: bool = False
    willing_to_relocate: bool = False
    last_active_days: int = 999
    saved_by_recruiters_30d: int = 0
    profile_views_received_30d: int = 0
    search_appearance_30d: int = 0
    applications_submitted_30d: int = 0
    profile_completeness_score: float = 0.0
    github_activity_score: float = -1.0
    interview_completion_rate: float = 0.0
    preferred_work_mode: str = ""
    connection_count: int = 0
    endorsements_received: int = 0


@dataclass
class TextBundle:
    title_text: str
    headline_text: str
    summary_text: str
    profile_text: str
    skill_text: str
    career_text: str
    current_role_text: str
    full_text: str
    skills_lower: list[str]
    skill_names: list[str]
    current_title_lower: str
    current_company_lower: str
    current_industry_lower: str
    location_lower: str
    country_lower: str


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _linear(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return _clip((value - low) / (high - low))


def _inverse_linear(value: float, low: float, high: float) -> float:
    return 1.0 - _linear(value, low, high)


def _contains_any(text: str, terms: tuple[str, ...] | list[str] | set[str]) -> bool:
    return any(term in text for term in terms)


def _count_contains(text: str, terms: tuple[str, ...] | list[str] | set[str]) -> int:
    return sum(1 for term in terms if term in text)


def _distinct_skill_matches(skill_names: list[str], skills_lower: list[str], term_group: tuple[str, ...]) -> list[str]:
    matches: list[str] = []
    for original, lowered in zip(skill_names, skills_lower):
        if any(term in lowered for term in term_group):
            matches.append(original)
    # Stable de-dupe while preserving order.
    seen: set[str] = set()
    result: list[str] = []
    for skill in matches:
        if skill not in seen:
            seen.add(skill)
            result.append(skill)
    return result


def _exact_title_fit(title_lower: str) -> float:
    if any(term in title_lower for term in HIGH_SIGNAL_TITLES):
        return 1.0
    if any(term in title_lower for term in ADJACENT_SIGNAL_TITLES):
        return 0.72
    if any(term in title_lower for term in NON_TECHNICAL_TITLES):
        return 0.12
    if "engineer" in title_lower or "developer" in title_lower:
        return 0.55
    return 0.28


def _experience_fit(years: float) -> float:
    # Peak around 6-8 years; still keep strong adjacent candidates in play.
    if 5.0 <= years <= 9.0:
        return 1.0
    if 4.0 <= years < 5.0:
        return 0.85
    if 9.0 < years <= 11.0:
        return 0.82
    if 3.0 <= years < 4.0:
        return 0.65
    if 11.0 < years <= 14.0:
        return 0.6
    if 2.0 <= years < 3.0:
        return 0.4
    return 0.2


def _location_fit(country_lower: str, location_lower: str, willing_to_relocate: bool) -> float:
    in_india = country_lower == PREFERRED_COUNTRY
    if in_india and any(city in location_lower for city in TIER1_INDIA_CITY_KEYWORDS):
        return 1.0
    if in_india:
        return 0.82 if willing_to_relocate else 0.72
    return 0.68 if willing_to_relocate else 0.32


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def _months_between(start: datetime | None, end: datetime | None) -> int | None:
    if start is None or end is None:
        return None
    return max(0, (end.year - start.year) * 12 + (end.month - start.month) + (1 if end.day >= start.day else 0))


def _normalize_upper(value: float, q1: float, q2: float, q3: float, q4: float) -> float:
    if value <= q1:
        return 0.0
    if value >= q4:
        return 1.0
    if value <= q2:
        return 0.35 * _linear(value, q1, q2)
    if value <= q3:
        return 0.35 + 0.35 * _linear(value, q2, q3)
    return 0.7 + 0.3 * _linear(value, q3, q4)


def _normalize_lower(value: float, q1: float, q2: float, q3: float, q4: float) -> float:
    return 1.0 - _normalize_upper(value, q1, q2, q3, q4)


def _top_phrases(items: list[str], limit: int = 3) -> str:
    filtered = [item for item in items if item]
    if not filtered:
        return ""
    limit = min(limit, len(filtered))
    if len(filtered) == 1:
        return filtered[0]
    if limit == 2:
        return f"{filtered[0]} and {filtered[1]}"
    return ", ".join(filtered[: limit - 1]) + f", and {filtered[limit - 1]}"


def _describe_stage1_flag(flag: str) -> str:
    mapping = {
        "low_core_relevance": "very weak direct relevance to retrieval/ranking work",
        "weak_direct_relevance": "only partial direct relevance to the JD",
        "below_preferred_experience_band": "below the preferred experience band",
        "well_above_preferred_experience_band": "well above the target experience band",
        "consulting_heavy_background": "career history leans consulting-heavy versus product-native",
        "research_without_production": "research signals without enough production deployment evidence",
        "architecture_heavy_recent_role": "recent role looks more architecture-led than hands-on",
        "outside_india_no_relocation": "outside India without relocation flexibility",
    }
    return mapping.get(flag, flag.replace("_", " "))


def _describe_honeypot_flag(flag: str) -> str:
    mapping = {
        "timeline_mismatch": "timeline math between dates and durations looks inconsistent",
        "heavy_overlap_timeline": "career timeline appears to overlap unusually heavily",
        "unrealistic_skill_depth": "advanced skill depth looks too compressed for the stated durations",
        "keyword_stuffer_title_mismatch": "AI/search keywords are not backed by the current title or role history",
        "suspiciously_perfect_junior_profile": "junior profile has unusually perfect behavioral signals",
        "seniority_experience_mismatch": "seniority label does not match stated years of experience",
        "junior_label_with_senior_experience": "junior title conflicts with very senior experience",
        "vision_speech_without_ir": "profile leans CV/speech without enough retrieval or ranking evidence",
        "inactive_low_responsiveness": "candidate looks inactive and slow to engage recruiters",
    }
    return mapping.get(flag, flag.replace("_", " "))


def _build_text_bundle(candidate: dict[str, Any]) -> TextBundle:
    profile = candidate["profile"]
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])

    title_text = (profile.get("current_title") or "").lower()
    headline_text = (profile.get("headline") or "").lower()
    summary_text = (profile.get("summary") or "").lower()
    skill_names = [str(skill.get("name") or "") for skill in skills]
    skills_lower = [name.lower() for name in skill_names]
    skill_text = " ".join(skills_lower)

    career_chunks: list[str] = []
    current_role_text = ""
    for job in career:
        chunk = " ".join(
            (
                str(job.get("title") or ""),
                str(job.get("company") or ""),
                str(job.get("industry") or ""),
                str(job.get("description") or ""),
            )
        ).lower()
        career_chunks.append(chunk)
        if job.get("is_current"):
            current_role_text = chunk
    career_text = " ".join(career_chunks)
    profile_text = " ".join((title_text, headline_text, summary_text))
    full_text = " ".join((profile_text, skill_text, career_text))
    return TextBundle(
        title_text=title_text,
        headline_text=headline_text,
        summary_text=summary_text,
        profile_text=profile_text,
        skill_text=skill_text,
        career_text=career_text,
        current_role_text=current_role_text,
        full_text=full_text,
        skills_lower=skills_lower,
        skill_names=skill_names,
        current_title_lower=title_text,
        current_company_lower=(profile.get("current_company") or "").lower(),
        current_industry_lower=(profile.get("current_industry") or "").lower(),
        location_lower=(profile.get("location") or "").lower(),
        country_lower=(profile.get("country") or "").lower(),
    )


def _concept_score(bundle: TextBundle, concept: str) -> tuple[float, list[str]]:
    terms = RELEVANCE_TERMS[concept]
    title_hits = _count_contains(bundle.title_text + " " + bundle.headline_text, terms)
    summary_hits = _count_contains(bundle.summary_text, terms)
    career_hits = _count_contains(bundle.career_text, terms)
    skill_matches = _distinct_skill_matches(bundle.skill_names, bundle.skills_lower, terms)
    current_hits = _count_contains(bundle.current_role_text, terms)

    title_score = min(1.0, title_hits / 2.0)
    summary_score = min(1.0, summary_hits / 3.0)
    career_score = min(1.0, career_hits / 4.0)
    skill_score = min(1.0, len(skill_matches) / 3.0)
    current_score = min(1.0, current_hits / 2.0)

    score = _clip(
        0.18 * title_score
        + 0.12 * summary_score
        + 0.38 * career_score
        + 0.20 * skill_score
        + 0.12 * current_score
    )
    return score, skill_matches[:4]


def _stage1_gate(
    result: CandidateResult,
    bundle: TextBundle,
    candidate: dict[str, Any],
    title_fit: float,
    semantic_seed: float,
    role_depth: float,
) -> None:
    gate = 1.0
    flags: list[str] = []
    years = result.years_of_experience

    if semantic_seed < 0.12 and title_fit < 0.35 and role_depth < 0.2:
        gate *= 0.18
        flags.append("low_core_relevance")
    elif semantic_seed < 0.2 and title_fit < 0.55:
        gate *= 0.5
        flags.append("weak_direct_relevance")

    if years < 3.0:
        gate *= 0.55
        flags.append("below_preferred_experience_band")
    elif years > 14.0:
        gate *= 0.8
        flags.append("well_above_preferred_experience_band")

    career = candidate.get("career_history", [])
    if career:
        companies = [(job.get("company") or "").lower() for job in career]
        consulting_only = all(
            company in CONSULTING_COMPANIES or "consult" in (job.get("industry") or "").lower() or "it services" in (job.get("industry") or "").lower()
            for company, job in zip(companies, career)
        )
        if consulting_only:
            gate *= 0.86
            flags.append("consulting_heavy_background")

    if any(term in bundle.full_text for term in RESEARCH_TERMS) and not _contains_any(bundle.full_text, RELEVANCE_TERMS["production_ml"]):
        gate *= 0.72
        flags.append("research_without_production")

    if any(term in bundle.current_title_lower for term in ARCHITECTURE_ONLY_TERMS) and result.recent_hands_on_engineering < 0.4:
        gate *= 0.75
        flags.append("architecture_heavy_recent_role")

    if bundle.country_lower != PREFERRED_COUNTRY and not result.willing_to_relocate:
        gate *= 0.82
        flags.append("outside_india_no_relocation")

    result.stage1_gate = _clip(gate, 0.05, 1.0)
    result.stage1_flags = flags


def _behavior_scores(candidate: dict[str, Any], result: CandidateResult) -> None:
    signals = candidate["redrob_signals"]
    profile = candidate["profile"]

    last_active = _parse_date(signals.get("last_active_date"))
    last_active_days = 365
    if last_active is not None:
        last_active_days = max(0, (REFERENCE_DATE - last_active.date()).days)

    activity_score = _clip(
        0.40 * _normalize_lower(last_active_days, 7, 30, 90, 180)
        + 0.25 * (1.0 if signals.get("open_to_work_flag") else 0.0)
        + 0.15 * _normalize_upper(float(signals.get("applications_submitted_30d", 0)), 2, 5, 8, 10)
        + 0.20 * _normalize_upper(float(signals.get("profile_completeness_score", 0)), *BEHAVIOR_QUANTILES["profile_completeness_score"])
    )
    responsiveness = _clip(
        0.45 * _normalize_upper(float(signals.get("recruiter_response_rate", 0.0)), *BEHAVIOR_QUANTILES["recruiter_response_rate"])
        + 0.15 * _normalize_lower(float(signals.get("avg_response_time_hours", 9999.0)), *BEHAVIOR_QUANTILES["avg_response_time_hours"])
        + 0.15 * _normalize_upper(float(signals.get("interview_completion_rate", 0.0)), *BEHAVIOR_QUANTILES["interview_completion_rate"])
        + 0.10 * _normalize_lower(float(signals.get("notice_period_days", 180)), *BEHAVIOR_QUANTILES["notice_period_days"])
        + 0.15 * activity_score
    )
    attractiveness = _clip(
        0.22 * _normalize_upper(float(signals.get("search_appearance_30d", 0)), *BEHAVIOR_QUANTILES["search_appearance_30d"])
        + 0.24 * _normalize_upper(float(signals.get("saved_by_recruiters_30d", 0)), *BEHAVIOR_QUANTILES["saved_by_recruiters_30d"])
        + 0.18 * _normalize_upper(float(signals.get("profile_views_received_30d", 0)), *BEHAVIOR_QUANTILES["profile_views_received_30d"])
        + 0.10 * _normalize_upper(float(signals.get("connection_count", 0)), *BEHAVIOR_QUANTILES["connection_count"])
        + 0.08 * _normalize_upper(float(signals.get("endorsements_received", 0)), *BEHAVIOR_QUANTILES["endorsements_received"])
        + 0.08 * _normalize_upper(max(0.0, float(signals.get("github_activity_score", -1))), *BEHAVIOR_QUANTILES["github_activity_score"])
        + 0.05 * (1.0 if signals.get("verified_email") else 0.0)
        + 0.03 * (1.0 if signals.get("verified_phone") else 0.0)
        + 0.02 * (1.0 if signals.get("linkedin_connected") else 0.0)
    )
    logistics = _clip(
        0.75 * _location_fit(
            country_lower=(profile.get("country") or "").lower(),
            location_lower=(profile.get("location") or "").lower(),
            willing_to_relocate=bool(signals.get("willing_to_relocate")),
        )
        + 0.25 * (1.0 if signals.get("preferred_work_mode") in {"hybrid", "flexible"} else 0.65 if signals.get("preferred_work_mode") == "onsite" else 0.5)
    )

    result.candidate_responsiveness = responsiveness
    result.recruiter_attractiveness = attractiveness
    result.behavioral_score = _clip(0.42 * responsiveness + 0.33 * attractiveness + 0.15 * activity_score + 0.10 * logistics)
    result.location_fit = logistics
    result.response_rate = float(signals.get("recruiter_response_rate", 0.0))
    result.avg_response_time_hours = float(signals.get("avg_response_time_hours", 0.0))
    result.notice_period_days = int(signals.get("notice_period_days", 180))
    result.open_to_work = bool(signals.get("open_to_work_flag"))
    result.willing_to_relocate = bool(signals.get("willing_to_relocate"))
    result.last_active_days = last_active_days
    result.saved_by_recruiters_30d = int(signals.get("saved_by_recruiters_30d", 0))
    result.profile_views_received_30d = int(signals.get("profile_views_received_30d", 0))
    result.search_appearance_30d = int(signals.get("search_appearance_30d", 0))
    result.applications_submitted_30d = int(signals.get("applications_submitted_30d", 0))
    result.profile_completeness_score = float(signals.get("profile_completeness_score", 0.0))
    result.github_activity_score = float(signals.get("github_activity_score", -1.0))
    result.interview_completion_rate = float(signals.get("interview_completion_rate", 0.0))
    result.preferred_work_mode = str(signals.get("preferred_work_mode", ""))
    result.connection_count = int(signals.get("connection_count", 0))
    result.endorsements_received = int(signals.get("endorsements_received", 0))
    result.behavioral_components = {
        "activity": activity_score,
        "responsiveness": responsiveness,
        "recruiter_attractiveness": attractiveness,
        "logistics": logistics,
    }

    highlights: list[str] = []
    if result.last_active_days <= 30:
        highlights.append(f"active in the last {result.last_active_days} days")
    elif result.last_active_days <= 90:
        highlights.append(f"active in the last {result.last_active_days} days, though not very recent")
    else:
        highlights.append(f"last active {result.last_active_days} days ago")
    if result.open_to_work:
        highlights.append("marked open to work")
    highlights.append(f"{result.response_rate:.2f} recruiter response rate")
    highlights.append(f"{result.notice_period_days}-day notice period")
    if result.saved_by_recruiters_30d > 0:
        highlights.append(f"{result.saved_by_recruiters_30d} recruiter saves in 30 days")
    if result.search_appearance_30d > 0:
        highlights.append(f"{result.search_appearance_30d} recruiter search appearances in 30 days")
    result.behavioral_highlights = highlights[:5]


def _career_scores(candidate: dict[str, Any], bundle: TextBundle, result: CandidateResult) -> None:
    career = candidate.get("career_history", [])
    title_fit = _exact_title_fit(bundle.current_title_lower)

    relevant_roles = 0
    product_roles = 0
    startup_roles = 0
    ownership_hits = 0
    hands_on_hits = 0
    avg_duration = 0.0
    current_role_relevant = 0.0
    technical_roles = 0

    for job in career:
        job_title = (job.get("title") or "").lower()
        job_desc = (job.get("description") or "").lower()
        job_industry = (job.get("industry") or "").lower()
        job_company = (job.get("company") or "").lower()
        job_text = f"{job_title} {job_desc} {job_industry} {job_company}"

        if any(term in job_text for term in HIGH_SIGNAL_TITLES + ADJACENT_SIGNAL_TITLES):
            relevant_roles += 1
        if "engineer" in job_title or "developer" in job_title or "scientist" in job_title:
            technical_roles += 1
        if _contains_any(job_text, RELEVANCE_TERMS["retrieval"]) or _contains_any(job_text, RELEVANCE_TERMS["ranking"]) or _contains_any(job_text, RELEVANCE_TERMS["recommendation"]):
            relevant_roles += 1
        if job_company in PRODUCT_BRANDS or any(term in job_industry for term in PRODUCT_INDUSTRY_KEYWORDS):
            product_roles += 1
        if (job.get("company_size") or "") in STARTUP_SIZE_BUCKETS:
            startup_roles += 1
        ownership_hits += _count_contains(job_text, OWNERSHIP_TERMS)
        hands_on_hits += _count_contains(job_text, HANDS_ON_TERMS)
        avg_duration += float(job.get("duration_months") or 0)
        if job.get("is_current"):
            current_role_relevant = 1.0 if relevant_roles > 0 else 0.65 if technical_roles > 0 else 0.2

    total_roles = max(1, len(career))
    avg_duration /= total_roles
    role_depth = _clip(relevant_roles / max(2.0, total_roles + 1.0))
    product_depth = _clip((0.65 * product_roles + 0.35 * startup_roles) / max(1.0, total_roles))
    tenure_fit = 1.0 if avg_duration >= 18 else 0.75 if avg_duration >= 12 else 0.45
    ownership_score = _clip(0.55 * min(1.0, ownership_hits / 5.0) + 0.45 * min(1.0, hands_on_hits / 7.0))
    hands_on_score = _clip(
        0.45 * min(1.0, hands_on_hits / 8.0)
        + 0.35 * current_role_relevant
        + 0.20 * min(1.0, technical_roles / max(1.0, total_roles))
    )
    product_fit = _clip(
        0.45 * product_depth
        + 0.15 * (1.0 if bundle.current_company_lower in PRODUCT_BRANDS else 0.0)
        + 0.18 * (1.0 if any(term in bundle.current_industry_lower for term in PRODUCT_INDUSTRY_KEYWORDS) else 0.0)
        + 0.12 * (1.0 if candidate["profile"].get("current_company_size") in STARTUP_SIZE_BUCKETS else 0.4 if candidate["profile"].get("current_company_size") in {"201-500", "501-1000"} else 0.25)
        + 0.10 * result.location_fit
    )
    production_ml = _clip(
        0.25 * result.retrieval_relevance
        + 0.18 * result.ranking_relevance
        + 0.10 * result.recommendation_relevance
        + 0.12 * result.evaluation_relevance
        + 0.15 * min(1.0, _count_contains(bundle.career_text, RELEVANCE_TERMS["production_ml"]) / 5.0)
        + 0.10 * hands_on_score
        + 0.10 * role_depth
    )

    result.title_fit = title_fit
    result.experience_fit = _experience_fit(result.years_of_experience)
    result.role_depth = role_depth
    result.product_depth = product_depth
    result.tenure_fit = tenure_fit
    result.ownership_impact_evidence = ownership_score
    result.recent_hands_on_engineering = hands_on_score
    result.startup_product_fit = product_fit
    result.production_ml_experience = production_ml
    result.career_evidence_score = _clip(
        0.16 * title_fit
        + 0.15 * result.experience_fit
        + 0.16 * role_depth
        + 0.18 * production_ml
        + 0.15 * product_fit
        + 0.12 * ownership_score
        + 0.08 * hands_on_score
    )
    result.career_components = {
        "title_fit": title_fit,
        "experience_fit": result.experience_fit,
        "role_depth": role_depth,
        "production_ml": production_ml,
        "product_fit": product_fit,
        "ownership": ownership_score,
        "recent_hands_on": hands_on_score,
        "tenure_fit": tenure_fit,
    }

    company_reference = f"current company {result.current_company}" if result.current_company else "current company"
    career_highlights: list[str] = [f"{result.current_title} with {result.years_of_experience:.1f} years of experience"]
    if bundle.current_company_lower in PRODUCT_BRANDS:
        career_highlights.append(f"product-company background at {result.current_company}")
    elif product_fit >= 0.55:
        career_highlights.append("career history shows solid product or marketplace exposure")
    if production_ml >= 0.55:
        career_highlights.append("career evidence suggests hands-on production ML ownership")
    if hands_on_score >= 0.55:
        career_highlights.append(f"recent role remains hands-on in engineering terms at {company_reference}")
    if ownership_score >= 0.55:
        career_highlights.append("descriptions show ownership, implementation, or delivery language")
    result.career_highlights = career_highlights[:5]


def _semantic_scores(bundle: TextBundle, result: CandidateResult) -> None:
    retrieval_score, retrieval_skills = _concept_score(bundle, "retrieval")
    ranking_score, ranking_skills = _concept_score(bundle, "ranking")
    recommendation_score, recommendation_skills = _concept_score(bundle, "recommendation")
    evaluation_score, _ = _concept_score(bundle, "evaluation")
    python_score, python_skills = _concept_score(bundle, "python")
    llm_score, llm_skills = _concept_score(bundle, "llm")
    cv_speech_score, _ = _concept_score(bundle, "cv_speech")

    result.retrieval_relevance = retrieval_score
    result.ranking_relevance = ranking_score
    result.recommendation_relevance = recommendation_score
    result.evaluation_relevance = evaluation_score
    result.python_strength = python_score
    result.llm_stack_score = llm_score

    keyword_only_penalty_seed = 0.0
    if any(term in bundle.current_title_lower for term in NON_TECHNICAL_TITLES) and (retrieval_score + ranking_score + recommendation_score) > 0.8:
        keyword_only_penalty_seed = 0.18

    synergy_bonus = 0.05 * min(retrieval_score, ranking_score) + 0.03 * min(retrieval_score, recommendation_score)
    cv_penalty = 0.08 * max(0.0, cv_speech_score - max(retrieval_score, ranking_score, recommendation_score))

    llm_wrapper_penalty = 0.0
    if llm_score >= 0.45 and max(ranking_score, recommendation_score) < 0.2 and evaluation_score < 0.22:
        llm_wrapper_penalty += 0.08
    if "chatbot" in bundle.full_text and max(ranking_score, recommendation_score) < 0.2:
        llm_wrapper_penalty += 0.05

    result.semantic_score = _clip(
        0.28 * retrieval_score
        + 0.24 * ranking_score
        + 0.12 * recommendation_score
        + 0.14 * evaluation_score
        + 0.12 * python_score
        + 0.10 * llm_score
        + synergy_bonus
        - cv_penalty
        - keyword_only_penalty_seed
        - llm_wrapper_penalty
    )

    matched_skills = []
    for skill in retrieval_skills + ranking_skills + recommendation_skills + python_skills + llm_skills:
        pretty = skill.strip()
        if pretty and pretty not in matched_skills:
            matched_skills.append(pretty)
    result.matched_skills = matched_skills[:6]

    matched_themes: list[str] = []
    if retrieval_score >= 0.35:
        matched_themes.append("retrieval/search")
    if ranking_score >= 0.35:
        matched_themes.append("ranking")
    if recommendation_score >= 0.3:
        matched_themes.append("recommendation")
    if evaluation_score >= 0.25:
        matched_themes.append("ranking evaluation")
    if llm_score >= 0.3:
        matched_themes.append("LLM tooling")
    if python_score >= 0.25:
        matched_themes.append("Python stack")
    result.matched_themes = matched_themes[:4]
    result.semantic_components = {
        "retrieval": retrieval_score,
        "ranking": ranking_score,
        "recommendation": recommendation_score,
        "evaluation": evaluation_score,
        "python": python_score,
        "llm": llm_score,
    }
    skill_alignment_highlights: list[str] = []
    if result.matched_themes:
        skill_alignment_highlights.append("aligned themes: " + ", ".join(result.matched_themes))
    if result.matched_skills:
        skill_alignment_highlights.append("matched skills: " + ", ".join(result.matched_skills[:4]))
    if evaluation_score >= 0.25:
        skill_alignment_highlights.append("profile text includes ranking-evaluation style terminology")
    if recommendation_score >= 0.3:
        skill_alignment_highlights.append("recommendation or matching evidence appears alongside search signals")
    result.skill_alignment_highlights = skill_alignment_highlights[:4]


def _honeypot_penalty(candidate: dict[str, Any], bundle: TextBundle, result: CandidateResult) -> None:
    skills = candidate.get("skills", [])
    career = candidate.get("career_history", [])
    flags: list[str] = []
    penalty = 0.0

    timeline_span_total = 0
    duration_total = 0
    earliest_start = None
    latest_end = None

    for job in career:
        start = _parse_date(job.get("start_date"))
        end = _parse_date(job.get("end_date")) or datetime.combine(REFERENCE_DATE, datetime.min.time())
        computed_months = _months_between(start, end)
        stated_months = int(job.get("duration_months") or 0)
        if computed_months is None or abs(computed_months - stated_months) > 8:
            penalty += 0.22
            flags.append("timeline_mismatch")
            break
        duration_total += stated_months
        if start and (earliest_start is None or start < earliest_start):
            earliest_start = start
        if end and (latest_end is None or end > latest_end):
            latest_end = end

    if earliest_start and latest_end:
        timeline_span_total = _months_between(earliest_start, latest_end) or 0
        if duration_total > timeline_span_total + 48:
            penalty += 0.08
            flags.append("heavy_overlap_timeline")

    expert_short = sum(
        1
        for skill in skills
        if (skill.get("proficiency") in {"advanced", "expert"}) and int(skill.get("duration_months") or 0) <= 6
    )
    if expert_short >= 4:
        penalty += 0.16
        flags.append("unrealistic_skill_depth")

    non_technical_title = any(term in bundle.current_title_lower for term in NON_TECHNICAL_TITLES)
    semantic_strength = result.retrieval_relevance + result.ranking_relevance + result.recommendation_relevance
    if non_technical_title and semantic_strength >= 1.0 and result.role_depth < 0.25:
        penalty += 0.2
        flags.append("keyword_stuffer_title_mismatch")

    if result.years_of_experience < 2.5 and result.recruiter_attractiveness > 0.92 and result.candidate_responsiveness > 0.92:
        penalty += 0.12
        flags.append("suspiciously_perfect_junior_profile")

    if "senior" in bundle.current_title_lower and result.years_of_experience < 3.0:
        penalty += 0.06
        flags.append("seniority_experience_mismatch")
    if "junior" in bundle.current_title_lower and result.years_of_experience > 8.0:
        penalty += 0.05
        flags.append("junior_label_with_senior_experience")

    if any(term in bundle.full_text for term in RELEVANCE_TERMS["cv_speech"]) and max(result.retrieval_relevance, result.ranking_relevance, result.recommendation_relevance) < 0.2:
        penalty += 0.08
        flags.append("vision_speech_without_ir")

    if result.response_rate < 0.08 and result.last_active_days > 180:
        penalty += 0.05
        flags.append("inactive_low_responsiveness")

    result.honeypot_penalty = _clip(penalty, 0.0, 0.75)
    result.honeypot_flags = list(dict.fromkeys(flags))


def _build_reasoning(result: CandidateResult) -> str:
    alignment_bits: list[str] = []
    if result.retrieval_relevance >= 0.4:
        alignment_bits.append("retrieval")
    if result.ranking_relevance >= 0.35:
        alignment_bits.append("ranking")
    if result.recommendation_relevance >= 0.3:
        alignment_bits.append("recommendation")
    if not alignment_bits and result.matched_themes:
        alignment_bits = result.matched_themes[:2]

    sentence_1_parts: list[str] = []
    if alignment_bits:
        sentence_1_parts.append(f"Strong semantic alignment with {_top_phrases(alignment_bits, limit=3)} requirements")
    else:
        sentence_1_parts.append("Reasonable semantic alignment with the JD")
    sentence_1_parts.append(f"{result.years_of_experience:.1f} years of experience in {result.current_title}")
    if result.current_company and result.current_company.lower() not in {"unknown", "na"}:
        sentence_1_parts.append(f"currently at {result.current_company}")
    first_sentence = "; ".join(sentence_1_parts[:2])
    if len(sentence_1_parts) > 2:
        first_sentence += f"; {sentence_1_parts[2]}"
    first_sentence += "."

    career_clauses: list[str] = []
    if result.production_ml_experience >= 0.55:
        career_clauses.append("career history points to hands-on production ML ownership")
    if result.startup_product_fit >= 0.55:
        career_clauses.append("background fits a product or marketplace environment")
    if result.matched_skills:
        career_clauses.append("matched skills include " + _top_phrases(result.matched_skills[:3], limit=3))

    behavioral_clause = ""
    if result.candidate_responsiveness >= 0.55 or result.saved_by_recruiters_30d >= 10 or result.notice_period_days <= 30 or result.last_active_days <= 30:
        behavioral_bits = [f"{result.response_rate:.2f} recruiter response rate", f"{result.notice_period_days}-day notice"]
        if result.saved_by_recruiters_30d > 0:
            behavioral_bits.append(f"{result.saved_by_recruiters_30d} recruiter saves in 30d")
        if result.last_active_days <= 30:
            behavioral_bits.append("active in the last 30 days")
        behavioral_clause = "Behavioral signals are solid with " + _top_phrases(behavioral_bits, limit=4) + "."

    if not career_clauses:
        career_clauses.append("profile shows adjacent engineering signals but with less decisive evidence than the very top cohort")
    second_sentence = _top_phrases(career_clauses[:2], limit=min(2, len(career_clauses))).capitalize() + "."

    concern: str | None = None
    if result.negative_factors and not result.negative_factors[0].startswith("no major red flags"):
        concern = result.negative_factors[0]
    elif result.ranking_relevance < 0.25:
        concern = "Direct ranking-system evidence is thinner than the strongest profiles"
    if concern:
        if behavioral_clause:
            return f"{first_sentence} {second_sentence} {behavioral_clause} Main concern: {concern}."
        return f"{first_sentence} {second_sentence} Main concern: {concern}."
    if behavioral_clause:
        return f"{first_sentence} {second_sentence} {behavioral_clause}"
    return f"{first_sentence} {second_sentence}"


def _finalize_explainability(result: CandidateResult) -> None:
    positive_candidates: list[tuple[float, str]] = []
    negative_candidates: list[tuple[float, str]] = []

    if min(result.retrieval_relevance, result.ranking_relevance) >= 0.35:
        positive_candidates.append(
            (
                (result.retrieval_relevance + result.ranking_relevance) / 2.0,
                f"strong retrieval and ranking alignment ({result.retrieval_relevance:.2f}/{result.ranking_relevance:.2f})",
            )
        )
    elif result.retrieval_relevance >= 0.4:
        positive_candidates.append((result.retrieval_relevance, f"strong retrieval/search alignment ({result.retrieval_relevance:.2f})"))
    if result.recommendation_relevance >= 0.32:
        positive_candidates.append((result.recommendation_relevance, f"recommendation or matching relevance ({result.recommendation_relevance:.2f})"))
    if result.production_ml_experience >= 0.52:
        positive_candidates.append((result.production_ml_experience, f"production ML evidence ({result.production_ml_experience:.2f})"))
    if result.startup_product_fit >= 0.55:
        positive_candidates.append((result.startup_product_fit, f"product/startup fit ({result.startup_product_fit:.2f})"))
    if result.recent_hands_on_engineering >= 0.55:
        positive_candidates.append((result.recent_hands_on_engineering, f"recent hands-on engineering evidence ({result.recent_hands_on_engineering:.2f})"))
    if result.candidate_responsiveness >= 0.55:
        positive_candidates.append(
            (
                result.candidate_responsiveness,
                f"strong responsiveness ({result.response_rate:.2f} response rate, {result.avg_response_time_hours:.1f}h avg response time)",
            )
        )
    if result.recruiter_attractiveness >= 0.55:
        positive_candidates.append(
            (
                result.recruiter_attractiveness,
                f"healthy recruiter demand ({result.saved_by_recruiters_30d} saves, {result.search_appearance_30d} search appearances)",
            )
        )
    if result.notice_period_days <= 30:
        positive_candidates.append((0.7, f"short notice period ({result.notice_period_days} days)"))
    if result.location_fit >= 0.8:
        positive_candidates.append((result.location_fit, f"good India hybrid logistics fit ({result.location}, {result.country})"))

    if result.ranking_relevance < 0.2:
        negative_candidates.append((1.0 - result.ranking_relevance, f"thin direct ranking evidence ({result.ranking_relevance:.2f})"))
    if result.response_rate < 0.2:
        negative_candidates.append((0.8, f"weak recruiter responsiveness ({result.response_rate:.2f})"))
    if result.notice_period_days > 90:
        negative_candidates.append((0.7, f"long notice period ({result.notice_period_days} days)"))
    if result.country.lower() != "india" and not result.willing_to_relocate:
        negative_candidates.append((0.85, "outside India without relocation flexibility"))
    for flag in result.stage1_flags:
        negative_candidates.append((0.65, _describe_stage1_flag(flag)))
    for flag in result.honeypot_flags:
        negative_candidates.append((0.9, _describe_honeypot_flag(flag)))

    positive_candidates.sort(key=lambda item: (-item[0], item[1]))
    negative_candidates.sort(key=lambda item: (-item[0], item[1]))
    result.positive_factors = [text for _, text in positive_candidates[:4]]
    if negative_candidates:
        result.negative_factors = [text for _, text in negative_candidates[:3]]
    else:
        result.negative_factors = ["no major red flags after timeline and behavioral sanity checks"]


def score_candidate(candidate: dict[str, Any]) -> CandidateResult:
    profile = candidate["profile"]
    bundle = _build_text_bundle(candidate)
    result = CandidateResult(
        candidate_id=str(candidate["candidate_id"]),
        current_title=str(profile.get("current_title") or ""),
        current_company=str(profile.get("current_company") or ""),
        location=str(profile.get("location") or ""),
        country=str(profile.get("country") or ""),
        years_of_experience=float(profile.get("years_of_experience") or 0.0),
    )

    _behavior_scores(candidate, result)
    _semantic_scores(bundle, result)
    _career_scores(candidate, bundle, result)
    _stage1_gate(
        result=result,
        bundle=bundle,
        candidate=candidate,
        title_fit=result.title_fit,
        semantic_seed=result.semantic_score,
        role_depth=result.role_depth,
    )
    _honeypot_penalty(candidate, bundle, result)

    semantic_plus_career = (
        STAGE7_WEIGHTS["semantic"] * result.semantic_score
        + STAGE7_WEIGHTS["career"] * result.career_evidence_score
    )
    semantic_plus_career = _clip(
        semantic_plus_career
        + 0.04 * min(result.retrieval_relevance, result.production_ml_experience)
        + 0.03 * min(result.ranking_relevance, result.evaluation_relevance + result.ownership_impact_evidence)
        + 0.02 * min(result.startup_product_fit, result.recent_hands_on_engineering)
    )
    behavior_multiplier = 0.72 + 0.38 * result.behavioral_score
    final_score = result.stage1_gate * semantic_plus_career * behavior_multiplier * (1.0 - result.honeypot_penalty)

    result.score = _clip(final_score)
    result.score_breakdown = {
        "stage1_gate": result.stage1_gate,
        "semantic_score": result.semantic_score,
        "career_evidence_score": result.career_evidence_score,
        "semantic_plus_career": semantic_plus_career,
        "behavior_multiplier": behavior_multiplier,
        "behavioral_score": result.behavioral_score,
        "honeypot_penalty": result.honeypot_penalty,
        "final_score": result.score,
    }

    if result.stage1_flags:
        if "consulting_heavy_background" in result.stage1_flags:
            result.concerns.append("consulting-heavy background")
        if "outside_india_no_relocation" in result.stage1_flags:
            result.concerns.append("relocation risk")
    if result.honeypot_flags:
        result.concerns.extend(result.honeypot_flags[:2])

    _finalize_explainability(result)
    result.reasoning = _build_reasoning(result)
    return result


def rank_candidates(input_path: Path, top_k: int = 100) -> list[CandidateResult]:
    heap: list[tuple[float, str, CandidateResult]] = []
    reservoir_size = max(400, top_k * 4)

    with input_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            candidate = json.loads(line)
            scored = score_candidate(candidate)
            item = (scored.score, scored.candidate_id, scored)
            if len(heap) < reservoir_size:
                heapq.heappush(heap, item)
            else:
                if item[0] > heap[0][0] or (math.isclose(item[0], heap[0][0]) and item[1] < heap[0][1]):
                    heapq.heapreplace(heap, item)

    ordered = [item[2] for item in heap]
    ordered.sort(key=lambda row: (-row.score, row.candidate_id))
    top = ordered[:top_k]
    for index, row in enumerate(top, start=1):
        row.rank = index
    return top


def write_submission(results: list[CandidateResult], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for row in results:
            writer.writerow([row.candidate_id, row.rank, f"{row.score:.6f}", row.reasoning])


def write_explainability_report(results: list[CandidateResult], output_path: Path) -> None:
    lines: list[str] = [
        "# Explainability Report",
        "",
        "## Audit Of The Previous Explainability Layer",
        "",
        "### How reasoning was generated before the redesign",
        "",
        "- A short threshold-based template selected a few generic strengths from high-level scores such as title, matched skills, product fit, and one concern.",
        "- The template used aggregated scores like `semantic_score`, `career_evidence_score`, and `behavioral_score`, but did not expose their component values.",
        "- Gate penalties and honeypot penalties influenced rank but were not clearly surfaced to the recruiter-facing explanation.",
        "",
        "### Where it fell short",
        "",
        "- Candidate-specific: partially yes, but often too templated.",
        "- Recruiter-readable: mostly yes, but too abstract for decision support.",
        "- Traceable to actual features: only partially, because many statements hid the underlying metrics.",
        "- Useful for human decision making: limited, because it did not consistently show concrete positives, negatives, or behavioral evidence.",
        "",
        "## Redesign Summary",
        "",
        "- Explanations are now grounded in explicit feature groups: semantic fit, behavioral signals, career evidence, and penalties.",
        "- Every ranked candidate now has:",
        "  - overall score",
        "  - recruiter-style summary",
        "  - top positive factors",
        "  - top negative factors",
        "  - behavioral signal highlights",
        "  - career evidence highlights",
        "  - skill alignment highlights",
        "- Non-explainable parts of the old pipeline were redesigned by exposing score components and penalty sources in `score_breakdown`, `semantic_components`, `behavioral_components`, and `career_components`.",
        "",
        "## Scoring Methodology",
        "",
        "Final score formula:",
        "",
        "```text",
        "final_score = stage1_gate",
        "              * (0.58 * semantic_score + 0.42 * career_evidence_score + synergy_terms)",
        "              * (0.72 + 0.38 * behavioral_score)",
        "              * (1 - honeypot_penalty)",
        "```",
        "",
        "### Feature importance by design",
        "",
        "- `semantic_score` is the largest single driver because the JD strongly emphasizes retrieval, ranking, recommendation, and evaluation evidence.",
        "- `career_evidence_score` is nearly as important because the challenge explicitly warns against skill-list-only ranking.",
        "- `behavioral_score` is multiplicative so that availability and recruiter engagement can down-rank weakly available candidates without rescuing weak technical fits.",
        "- `stage1_gate` and `honeypot_penalty` act as safety controls for obvious non-fits and suspicious profiles.",
        "",
        "### Weight rationale",
        "",
        "- Retrieval and ranking evidence got the heaviest semantic weights because they map most directly to the JD.",
        "- Product/startup fit, recent hands-on work, and production ML evidence are emphasized because the JD prefers shippers over pure researchers.",
        "- Response rate, recency, recruiter saves, and notice period are emphasized because the behavioral-signal doc says availability can be more predictive than static profile quality.",
        "",
        "## Sample Explanations For Top Candidates",
        "",
    ]

    for row in results[:5]:
        lines.extend(
            [
                f"### Rank {row.rank}: {row.candidate_id}",
                "",
                f"- Summary: {row.reasoning}",
                f"- Overall score: `{row.score:.6f}`",
                f"- Positive factors: {_top_phrases(row.positive_factors, limit=min(4, len(row.positive_factors) or 1))}",
                f"- Negative factors: {_top_phrases(row.negative_factors, limit=min(3, len(row.negative_factors) or 1))}",
                "",
            ]
        )

    lines.extend(
        [
            "## Justification For Ranking Decisions",
            "",
            "- Candidates rise when they show combined retrieval/ranking evidence, product-context delivery, recent hands-on engineering, and realistic hireability signals.",
            "- Candidates fall when they rely on skill keywords without matching role history, have slow recruiter responsiveness, long notice periods, relocation friction, or profile inconsistency flags.",
            "- This keeps the final ranking aligned with both hidden relevance judgments and recruiter usability.",
            "",
            "## Ranked Candidate Explainability",
            "",
        ]
    )

    for row in results:
        semantic_parts = ", ".join(f"{name}={value:.2f}" for name, value in row.semantic_components.items())
        behavior_parts = ", ".join(f"{name}={value:.2f}" for name, value in row.behavioral_components.items())
        career_parts = ", ".join(f"{name}={value:.2f}" for name, value in row.career_components.items())
        score_parts = ", ".join(f"{name}={value:.4f}" for name, value in row.score_breakdown.items())
        lines.extend(
            [
                f"### Rank {row.rank}: {row.candidate_id}",
                "",
                f"- Recruiter summary: {row.reasoning}",
                f"- Overall score: `{row.score:.6f}`",
                f"- Top positive factors: {_top_phrases(row.positive_factors, limit=min(4, len(row.positive_factors) or 1))}",
                f"- Top negative factors: {_top_phrases(row.negative_factors, limit=min(3, len(row.negative_factors) or 1))}",
                f"- Behavioral signal highlights: {_top_phrases(row.behavioral_highlights, limit=min(5, len(row.behavioral_highlights) or 1))}",
                f"- Career evidence highlights: {_top_phrases(row.career_highlights, limit=min(5, len(row.career_highlights) or 1))}",
                f"- Skill alignment highlights: {_top_phrases(row.skill_alignment_highlights, limit=min(4, len(row.skill_alignment_highlights) or 1))}",
                f"- Semantic component scores: `{semantic_parts}`",
                f"- Behavioral component scores: `{behavior_parts}`",
                f"- Career component scores: `{career_parts}`",
                f"- Score path: `{score_parts}`",
                "",
            ]
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
