# STARVEX Auto-Fix Intake

## What this adds
- A dedicated GitHub issue form for reproducible bugs.
- A consistent evidence/acceptance-criteria format so ChatGPT or an enabled coding agent can diagnose the exact failure.
- A strict boundary: proposed fixes go to a feature branch and PR; no automatic merge or deployment.

## Current automation boundary
GitHub Actions can run deterministic checks and collect logs. It does not contain a reasoning model and cannot safely invent arbitrary code fixes by itself. This repository currently has no verified, authorized AI model endpoint or confirmed agent callback. Therefore this intake does **not** claim that an AI repair worker is running.

## Operating procedure
1. Submit a bug with the **STARVEX Bug Fix Request** form.
2. Provide a failing Actions run or exact reproduction details; redact all secrets and customer data.
3. Ask ChatGPT to inspect the issue, source, and actual logs. ChatGPT can prepare a branch and PR through the connected GitHub integration.
4. Review the diff and successful CI before separately approving merge.

## Safety
- No model/API key is embedded in this repository.
- No third-party paid agent is invoked.
- No workflow checks out untrusted PR code with write permissions.
- No automatic merge or deployment.
