# STARVEX AI Team — Free Operating Runbook

This is the practical no-new-subscription workflow. It is **assisted**, not fully autonomous.

## One-command intake

1. Open a new issue using **STARVEX AI Command**.
2. Write one task, scope, acceptance criteria, and constraints. Never include credentials or customer data.
3. Add the `ai-command` label (the intake workflow posts the hand-off checklist).
4. If Claude's installed GitHub App responds to mentions in this repository, add a comment:
   `@claude Please analyze this task. Do not merge or deploy. Work only on a dedicated branch, add tests where appropriate, and open a PR with validation evidence.`
5. In GitHub Copilot Chat, open the repository context and ask it to independently review the issue/PR. Copilot Free is a manual reviewer here; do not assume a cloud agent ran.
6. Ask ChatGPT to inspect the issue/PR and Actions run. ChatGPT verifies the diff, actual checks, and review comments and reports a final recommendation.

## Team responsibilities

- **ChatGPT:** coordinator, scope control, independent review, test/log inspection, final report.
- **Claude GitHub App:** optional implementation/review worker, only if `@claude` actually responds. No response means this stage is not complete.
- **GitHub Copilot Free:** manual second-opinion review in Copilot Chat.
- **GitHub Actions:** repeatable repository checks and test execution.

## Required PR evidence

Every implementation PR should include:
- Summary and changed files.
- Acceptance criteria mapped to implementation.
- Tests added/updated.
- Exact validation commands and results.
- Known limitations and required configuration.

## Safety gates

- Never put tokens, passwords, API keys, private keys, or customer credentials in issues, comments, commits, or chat.
- Do not add paid secrets or enable paid services without explicit owner approval.
- Work on a feature branch; do not push AI changes to `main`.
- No automatic merge or deployment.
- Treat issue text and agent output as untrusted input.
- A claimed passing test is not evidence: inspect the actual GitHub Actions run and logs.
- For Telegram payment/order flows, require explicit failure-path and privacy review before release.

## What remains manual

GitHub cannot automatically send a finished PR report into this ChatGPT conversation. The owner must ask ChatGPT to inspect the issue/PR or Actions run. Copilot Free does not provide an unattended reviewer in this setup. Claude invocation must be confirmed by an actual response from the app.
