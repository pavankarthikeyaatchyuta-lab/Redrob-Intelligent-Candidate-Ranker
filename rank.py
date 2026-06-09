"""CLI entrypoint for the Redrob hackathon ranker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from redrob_ranker.pipeline import rank_candidates, write_explainability_report, write_submission  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank Redrob candidates for the Senior AI Engineer JD.")
    parser.add_argument("--candidates", default="candidates.jsonl", help="Path to the candidate JSONL file.")
    parser.add_argument("--out", default="ranked_candidates.csv", help="Output CSV path.")
    parser.add_argument("--explainability-report", default="explainability_report.md", help="Markdown explainability report path.")
    parser.add_argument("--top-k", type=int, default=100, help="Number of ranked candidates to emit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = (ROOT / args.candidates).resolve() if not Path(args.candidates).is_absolute() else Path(args.candidates)
    output_path = (ROOT / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    explainability_path = (ROOT / args.explainability_report).resolve() if not Path(args.explainability_report).is_absolute() else Path(args.explainability_report)

    results = rank_candidates(input_path=input_path, top_k=args.top_k)
    write_submission(results=results, output_path=output_path)
    write_explainability_report(results=results, output_path=explainability_path)
    print(f"Wrote {len(results)} ranked candidates to {output_path}")
    print(f"Wrote explainability report to {explainability_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
