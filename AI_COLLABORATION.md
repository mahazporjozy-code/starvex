# STARVEX AI Collaboration

## Purpose
This repository is the shared workspace for collaboration on the public STARVEX website.

## Source of truth
GitHub is the shared source of truth. ChatGPT and Gemini may independently inspect, propose, implement, and review changes through repository branches and pull requests. GitHub does not create a live direct chat between the models.

## Branch and review rules
- Do not commit directly to `main`.
- Make each task on a separate, clearly named branch.
- Keep changes focused and explain the purpose of each change.
- Open a pull request targeting `main` for review.
- Run relevant checks and report their results in the pull request.
- The project owner makes the final decision and approves merging and deployment.

## Security and privacy
- Never commit bot tokens, API keys, Supabase secrets, passwords, private keys, customer information, order data, or other confidential information.
- Use environment variables or the hosting platform's secret manager for credentials.
- Do not copy private STARVEX NEXUS panel code, configuration, or data into this public repository.
- Treat the separate private NEXUS repository as an independent project with its own access controls.

## Collaboration handoff
When handing work to another assistant:
1. State the task and expected outcome.
2. Identify the branch and files changed.
3. Summarize implementation decisions and outstanding questions.
4. Include checks performed and any known limitations.
5. Ask for review before merging.

## Scope
This repository is for the public STARVEX website. Private panel development remains outside this repository.
