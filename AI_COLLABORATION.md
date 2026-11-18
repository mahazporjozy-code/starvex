# STARVEX AI Collaboration

## Purpose
This repository is the shared workspace for collaboration on the public STARVEX website.

## Roles
- **Gemini — analyst:** inspect the project where its supported GitHub access allows; identify bugs, UX gaps, risks, missing features, and propose acceptance criteria. Gemini must not implement or commit code.
- **ChatGPT — engineer and reviewer:** read Gemini's findings from GitHub, verify them against the actual repository, decide the safest implementation, make code changes on a separate branch, run checks, and open a pull request.
- **Project owner — decision-maker:** set priorities and approve or reject pull requests and deployments.

## Shared handoff workflow
1. Ask Gemini to analyze a specific area or task, not to edit code.
2. Gemini prepares a structured analysis using the report format below.
3. Put the report in a GitHub Issue or as a comment on the relevant issue. If Gemini's available GitHub integration cannot publish issues/comments, the report must be pasted into GitHub by the project owner; do not give Gemini write access just for this workflow.
4. ChatGPT reads the GitHub issue/comment, checks each claim against the current source code, and marks unsupported or duplicate findings.
5. ChatGPT implements only verified and prioritized changes on a dedicated branch, then opens a pull request.
6. The project owner reviews and approves the pull request before merge or deployment.

## Gemini analysis report format
- **Title / area reviewed:**
- **Summary:**
- **Observed issue:** include file path and line/function when known.
- **Why it matters:**
- **Suggested behavior or solution:** describe the outcome, not code edits.
- **Priority:** critical / high / medium / low.
- **Acceptance criteria:** clear, testable bullets.
- **Risks / dependencies:**
- **Open questions:**
- **Confidence:** high / medium / low.

## Branch and review rules
- Do not commit directly to `main`.
- Make each implementation task on a separate, clearly named branch.
- Keep changes focused and explain the purpose of each change.
- Open a pull request targeting `main` for review.
- Run relevant checks and report their results in the pull request.
- The project owner makes the final decision and approves merging and deployment.

## Security and privacy
- Never commit bot tokens, API keys, Supabase secrets, passwords, private keys, customer information, order data, or other confidential information.
- Use environment variables or the hosting platform's secret manager for credentials.
- Do not copy private STARVEX NEXUS panel code, configuration, or data into this public repository.
- Treat the separate private NEXUS repository as an independent project with its own access controls.

## Important limitation
GitHub is a shared handoff workspace, not a live direct chat or automatic agent-to-agent connection. A model can only read or publish to GitHub if its own product integration and permissions support that action. A read-only Gemini connection is sufficient for analysis; if Gemini cannot create an issue/comment, the report needs to be posted by the project owner. ChatGPT can then retrieve it and implement approved work.

## Scope
This repository is for the public STARVEX website. Private panel development remains outside this repository.
