# Contributing to Personal LinkedIn Analytics on Databricks

Thanks for contributing! This file explains how to file issues, propose changes, and run basic checks.

How to file an issue
- Use GitHub Issues and include: steps to reproduce, expected vs actual behavior, environment details, and relevant logs or notebook outputs.

Branching and PR process
- Create a feature branch from `main` named `feat/<short-description>` or `fix/<short-description>`.
- Open a pull request against `main` and link any related issue.
- Use the PR template at `.github/pull_request_template.md` when opening a PR; it contains the required checklist and documentation hygiene reminders.

PR checklist (required before merging)
- [ ] Issue linked (if applicable)
- [ ] Title and description clearly explain the change
- [ ] README or relevant docs updated
- [ ] Notebooks that changed are runnable (smoke tested)
- [ ] No secrets or tokens committed
- [ ] YAML resources (`resources/*.yml`) validated for syntax
- Documentation hygiene (docs changes)
  - [ ] Doc pages are short, high-level, and link to authoritative code (see `docs/documentation_hygiene.md`)
  - [ ] If a doc change affects behavior or configuration, `CHANGELOG.md` has an `Unreleased` entry
  - [ ] Large code blocks were not copy-pasted into docs (if included, ensure they are <= 5 lines)
  - [ ] Local dev overrides (e.g., `.databricks/bundle/*/variable-overrides.json`) do not contain secrets; use Databricks secrets or CI secrets for tokens. See `docs/quickstart.md` for examples.

Testing guidance
- Unit tests: run `pytest` (if tests are added)
- Notebook smoke test: use `papermill` to run critical notebooks with small parameters
- Validate YAML files with a YAML linter or `yamllint`

Security
- Do not commit credentials. Use environment variables or secret stores when running jobs.

Style
- Keep notebooks modular. When adding code used across notebooks, add it under `src/` as a reusable module and import it from notebooks.

Thanks for contributing!
