# STARVEX AI Collaboration Bridge

This repository uses a GitHub-mediated, human-controlled handoff:
**Gemini = read-only analyst → GitHub Issue = shared handoff → ChatGPT = verifier and implementation agent → Pull Request = reviewable changes.**

## 1. Connect Gemini
In Gemini, use its GitHub integration/connected-app flow (if available on the account) and authorize access to only `mahazporjozy-code/starvex`. Grant read access for analysis. Do not grant write access: Gemini must not edit repository files.
If Gemini cannot create GitHub Issues, ask it to produce the report in the format in `GEMINI.md`, then create an issue manually using **Gemini Audit Report**.

## 2. Ask Gemini to analyze
Give Gemini this instruction:
> Analyze `mahazporjozy-code/starvex` for the problem I describe. Follow the repository's `GEMINI.md` exactly. You are read-only: do not edit files, commit, push, merge, or deploy. Verify findings against code, cite file paths and line numbers, distinguish facts from assumptions, and submit a GitHub Issue titled `[GEMINI AUDIT] ...` using the Gemini Audit Report format. Do not expose secrets.
Gemini posts its findings as an Issue. This is the handoff; the two models do not communicate directly or run each other in the background.

## 3. Ask ChatGPT to implement
In ChatGPT, say:
> Review Gemini audit issue #NUMBER in `mahazporjozy-code/starvex`. Fetch the current code yourself. Verify every finding independently; ignore unsupported recommendations. Implement justified fixes on a new branch, run the available tests/checks, and open a Pull Request. Do not merge or deploy without my approval.
ChatGPT can use the connected GitHub tools to inspect files, commit changes, and create a PR. The owner reviews and approves the PR.

## 4. Safety and limits
- GitHub Issues and PRs are the message bus, not a live model-to-model connection.
- Gemini does analysis only; ChatGPT owns code changes.
- ChatGPT must verify the report against the latest repository state before editing.
- Never put API keys, passwords, access tokens, private customer data, or `.env` contents in Issues.
- Do not auto-merge or auto-deploy based only on an AI report.
- This setup does not install or authorize Gemini's GitHub integration; the repository owner must complete Google's connection/authorization screen.