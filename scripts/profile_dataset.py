"""Profile the challenge dataset and emit a markdown summary."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path


def quantile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * pct))))
    return ordered[idx]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    input_path = repo_root / "candidates.jsonl"
    output_path = repo_root / "analysis" / "dataset_profile.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    exp_vals: list[float] = []
    response_vals: list[float] = []
    notice_vals: list[int] = []
    github_vals: list[float] = []
    saved_vals: list[int] = []
    title_counter: Counter[str] = Counter()
    skill_counter: Counter[str] = Counter()
    country_counter: Counter[str] = Counter()

    total = 0
    with input_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            total += 1
            candidate = json.loads(line)
            profile = candidate["profile"]
            signals = candidate["redrob_signals"]
            exp_vals.append(float(profile["years_of_experience"]))
            response_vals.append(float(signals["recruiter_response_rate"]))
            notice_vals.append(int(signals["notice_period_days"]))
            if float(signals["github_activity_score"]) >= 0:
                github_vals.append(float(signals["github_activity_score"]))
            saved_vals.append(int(signals["saved_by_recruiters_30d"]))
            title_counter[profile["current_title"]] += 1
            country_counter[profile["country"]] += 1
            for skill in candidate.get("skills", []):
                skill_counter[skill["name"]] += 1

    lines = [
        "# Dataset Profile",
        "",
        f"- Total candidates profiled: `{total}`",
        f"- Experience mean: `{statistics.mean(exp_vals):.2f}` years",
        f"- Experience p10/p50/p90: `{quantile(exp_vals, 0.1):.1f}` / `{quantile(exp_vals, 0.5):.1f}` / `{quantile(exp_vals, 0.9):.1f}`",
        f"- Recruiter response mean: `{statistics.mean(response_vals):.2f}`",
        f"- Notice p25/p50/p75: `{quantile(notice_vals, 0.25):.0f}` / `{quantile(notice_vals, 0.5):.0f}` / `{quantile(notice_vals, 0.75):.0f}` days",
        f"- GitHub activity mean (non-negative rows): `{statistics.mean(github_vals):.1f}`",
        f"- Saved-by-recruiters p50/p90: `{quantile(saved_vals, 0.5):.0f}` / `{quantile(saved_vals, 0.9):.0f}`",
        "",
        "## Top Titles",
        "",
    ]
    lines.extend([f"- `{title}`: {count}" for title, count in title_counter.most_common(15)])
    lines.extend(["", "## Top Skills", ""])
    lines.extend([f"- `{skill}`: {count}" for skill, count in skill_counter.most_common(20)])
    lines.extend(["", "## Countries", ""])
    lines.extend([f"- `{country}`: {count}" for country, count in country_counter.most_common()])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

