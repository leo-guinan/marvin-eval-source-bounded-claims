#!/usr/bin/env python3
"""Score claim-level source-bounded outputs against a human-labeled fixture."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


def score(cases, candidate):
    by_case = {row["case_id"]: row for row in candidate.get("cases", [])}
    rows = []
    for case in cases["cases"]:
        actual = {row["claim_id"]: row for row in by_case.get(case["id"], {}).get("claims", [])}
        for expected in case["expected_claims"]:
            got = actual.get(expected["id"], {})
            predicted = got.get("label", "missing")
            source_ids = got.get("source_ids", [])
            rows.append({
                "case_id": case["id"], "claim_id": expected["id"],
                "expected": expected["label"], "predicted": predicted,
                "source_ids": source_ids,
                "pass": predicted == expected["label"] and (predicted == "supported" and bool(source_ids) or predicted != "supported" and not source_ids),
            })
    total = len(rows)
    passes = sum(row["pass"] for row in rows)
    factual = [row for row in rows if row["expected"] in ("supported", "unsupported")]
    unsupported_predicted = sum(row["predicted"] == "supported" and row["expected"] != "supported" for row in factual)
    return {
        "receipt_version": "1.0.0", "eval_id": "marvin.source-bounded-claims",
        "fixture_id": cases["fixture_id"], "fixture_status": cases["status"],
        "candidate_id": candidate.get("candidate_id", "MISSING"),
        "candidate_provenance": candidate.get("provenance", "MISSING"),
        "scored_claims": total, "passing_claims": passes,
        "claim_accuracy": round(passes / total, 4) if total else None,
        "unsupported_claim_rate": round(unsupported_predicted / len(factual), 4) if factual else None,
        "rows": rows, "claim_boundary": cases["claim_boundary"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = score(load("fixtures/cases.json"), load(args.candidate))
    Path(args.receipt).write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ("eval_id", "candidate_id", "scored_claims", "passing_claims", "claim_accuracy", "unsupported_claim_rate")}))

if __name__ == "__main__":
    main()
