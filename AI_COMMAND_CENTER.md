# STARVEX AI Command Center

## Purpose

Provide one controlled intake point for STARVEX development tasks and a repeatable hand-off between the owner, ChatGPT, Claude Code, GitHub Copilot, and GitHub Actions.

This bootstrap is intentionally **human-approved**. It does not claim that three AI products can currently invoke one another automatically.

## Current verified capabilities

- ChatGPT can inspect this repository through the connected GitHub integration and can prepare/review changes when the required repository tools are available.
- Claude Code's GitHub App was previously observed as installed. Its ability to act on a particular issue or pull request must be confirmed in GitHub before relying on it.
- GitHub Copilot Free provides Copilot Chat and code assistance. Copilot cloud Agent Sessions were previously shown as requiring an upgrade, so unattended Copilot implementation/review is not assumed.
- GitHub Actions can run repository checks and report their results. The existing CI workflow is the source of truth for automated test status.

## Target operating flow

1. Owner submits one task using the **STARVEX AI Command** issue form.
2. ChatGPT acts as coordinator: checks the current default branch, open PRs, scope, risks, and acceptance criteria.
3. Claude Code may implement the approved task on a dedicated branch and open a PR, if its GitHub App is enabled for the repository and responds to the task.
4. Copilot may provide an independent review when the repository's Copilot features allow it. If unattended Agent/review is unavailable on the current plan, use Copilot Chat as a manual reviewer; do not mark this stage complete without evidence.
5. GitHub Actions runs the checks on the PR.
6. ChatGPT reviews the diff, tests, and agent feedback, then reports the result to the owner.
7. The owner explicitly approves any merge or production deployment.

## Command format

A task should state:
- **Goal:** the desired outcome.
- **Scope:** files/features allowed to change.
- **Acceptance criteria:** observable conditions that define completion.
- **Constraints:** things that must not change.
- **Risk level:** low / medium / high.

The issue form collects these fields. A short command can be used as the task title, with the details in the form.

## Mandatory safety and quality gates

- Never commit secrets, tokens, passwords, private keys, or customer credentials.
- Use GitHub Actions Secrets or the host's secret manager for credentials. Never paste secret values into issues, PRs, or ChatGPT.
- Work on a feature branch. Never push AI-generated changes directly to `main`.
- Do not merge automatically.
- Do not deploy automatically.
- Require passing CI and a human review before merge.
- For customer-facing order/payment flows, verify failure handling and privacy before release.
- An agent's claim that a test passed is not proof; inspect the actual GitHub Actions run and logs.
- Do not treat a green source-text assertion as proof of runtime behavior.

## What is not automated yet

The following are explicit prerequisites for the full "one instruction in ChatGPT, finished result returned in ChatGPT" experience:

1. A supported, authorized way to invoke Claude Code from a GitHub issue/PR or workflow.
2. A supported Copilot agent/review capability available to this repository and account. Copilot Free Chat alone does not provide an unattended agent worker.
3. A callback/reporting path that lets ChatGPT retrieve the completed task, PR, checks, and review results. The GitHub connector can retrieve these when asked, but it does not autonomously push a notification into this chat.
4. Owner-approved configuration of any required app permissions and secrets.

Until those prerequisites are verified, the issue form is a controlled task intake and the agents' hand-offs may still require a manual trigger. Do not describe the system as fully autonomous.

## Initial rollout

- Keep this bootstrap on its own branch and review it as a draft PR.
- Verify Claude's issue/PR mention behavior in a non-production task.
- Verify whether Copilot Agent or automated PR review is available; if not, retain Copilot Chat as a manual review stage.
- Only then add an orchestrator workflow that calls confirmed, supported integrations.
