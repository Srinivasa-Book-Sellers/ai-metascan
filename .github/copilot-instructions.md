# Copilot instructions for ai-metascan

## Working style: small, reviewed steps

- Make changes gradually. Do only the step the user asked for; do not build ahead or implement the full end-to-end workflow unless explicitly asked.
- Keep each change small and easy to review. Prefer the simplest code that does the requested step; avoid extra validation, abstractions, or tests beyond what the step needs unless asked.
- Before larger code changes, briefly describe the plan and wait for the user to confirm.
- Pause after each step so the user can review it before continuing.
- Do not create logs, changelogs, notes, or other extra files automatically.
- Do not commit, push, or open pull requests unless the user asks.

## Data

- Inventory images, generated Excel files, and runtime data stay outside the repository and must not be committed. The only exceptions are the approved, compressed sample test case in `tests/sample` and the sample labels in `resources/labels`.
- The Vyapaar import template is `resources/Import Items Template.xlsx`; keep its headers unchanged.
