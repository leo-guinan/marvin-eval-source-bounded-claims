#!/usr/bin/env python3
import json
from pathlib import Path

manifest = json.loads((Path(__file__).parent / "eval" / "index.json").read_text())
required = ["id", "name", "version", "status", "standard", "test", "metric", "claim_boundary", "latest_run", "provenance"]
missing = [key for key in required if key not in manifest]
if missing:
    raise SystemExit("missing manifest keys: " + ", ".join(missing))
if manifest["status"] != "scaffold":
    raise SystemExit("initial validator expects scaffold status")
if manifest["latest_run"] is not None:
    raise SystemExit("latest_run must remain null until a real run exists")
if not manifest["provenance"]["synthetic_results_must_not_be_presented_as_real"]:
    raise SystemExit("claim-boundary guard is disabled")
print(manifest["id"], "manifest valid; no evaluation result claimed")
