# STARVEX — Copilot Instructions

- Read `AI_COMMAND_CENTER.md` and `AI_TEAM_RUNBOOK.md` before making changes.
- Work only on the requested scope and on a feature branch.
- Do not modify production settings, deployment configuration, or secrets unless explicitly requested.
- Never expose, copy, or commit credentials, tokens, private keys, or customer data.
- Prefer small, focused changes and add meaningful behavioral tests.
- Do not claim tests passed unless you ran them and can report the exact command and result.
- Do not use source-text checks as a substitute for runtime behavior tests.
- For Telegram order/payment flows, verify failure handling, admin notification behavior, and privacy.
- Do not merge or deploy. Open a PR with a concise summary, tests, evidence, and limitations.
