# Source-bounded Claims

Public, receipt-backed eval for Marvin. This repository defines the contract before claiming a result.

## Status

- Protocol: v0.1
- Latest run: not run
- Evidence status: scaffold only
- Public claim: none yet

Do not replace “not run” with a number. A synthetic fixture can prove the runner works; it cannot prove Marvin meets the standard.

## Standard

Every factual claim traces to supplied or retrieved evidence; unknowns remain unknown.

## Test

Extract claims from outputs, map each to evidence, and mark unsupported or over-broad claims as failures.

## Reported metric

`unsupported_claim_rate` — unsupported factual claims divided by all scored factual claims.

## Claim boundary

Passing a source fixture does not establish truth beyond the cited source set.

## Files

- `eval/index.json` — versioned contract and claim boundary.
- `validate.py` — dependency-free schema/contract check.

## Run

```sh
python3 validate.py
```

The first real report will include the fixture version, case count, model/prompt identifiers where applicable, pass/fail outcomes, failures, and an independent receipt.
