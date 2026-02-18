# TODO - Tasks, Improvements, and Next Steps

This TODO list consolidates actionable items and suggested next steps derived from the repository's "Key takeaways" and ongoing maintenance needs. Items are short and prioritized so contributors can pick small, well-scoped tasks.

How to use this file
- Add a short one-line entry for a task and link to related files or docs.
- When a PR completes a task, mark the checkbox and add a short changelog entry in `CHANGELOG.md`.

High priority
- [x] Integrate Unit Testing and Bundle Validation into CI/CD. (Implemented: `.github/workflows/ci_cd_bundle.yml`)

Medium priority
- [x] Add short unit tests for any Python modules in `src/` using `pytest` and add test runner instructions.
- [ ] Add lightweight architecture diagrams to `docs/images/` (SVG) and embed them in `docs/README.md`.
- [ ] Create `docs/diagrams.svg` or `docs/images/architecture.svg` for the medallion flow.
- [ ] Add small sample dataset files (anonymized) to `tests/fixtures/` for faster local iteration.

Architecture and modeling
- [ ] Document partitioning and performance recommendations for gold fact tables (add a short note to `docs/modeling.md`).
- [ ] Add a short note in `docs/modeling.md` linking to `src/.../pipeline_gold_create/*.sql` for schema details.

Orchestration and operations
- [ ] Add example `dbx` or `databricks` CLI commands for CI/CD in `docs/quickstart.md` (if desired and tested).
- [ ] Add minimal monitoring SQL examples in `docs/observability.md` (daily freshness checks and row-count anomaly checks).

Maintainability
- [x] Extract frequently used notebook code into `src/` Python modules and add import examples in notebooks.
- [ ] Add a short migration note template in `docs/maintainability.md` to document schema changes and backfill plans.

Documentation hygiene
- [ ] Keep docs short and high-level. If a doc change affects behavior, add a short changelog item under the latest dated section in `CHANGELOG.md`.
- [ ] Link key notebooks and SQL files from docs pages rather than embedding code snippets to reduce duplication.

Nice-to-have (lower priority)
- [ ] Add an MkDocs configuration `mkdocs.yml` and a simple theme if you want a docs site.
- [ ] Add a small dashboard health badge (if you have a monitoring endpoint) to the README.
- [ ] **[Low Priority]** Add CI smoke tests/integration tests for critical notebooks via `papermill`. *Note: Partially superseded by modular unit tests and `bundle validate`.*

How to mark progress
- When completing a task: mark the checkbox, open a PR, and add a brief `CHANGELOG.md` entry under the latest dated section (one-liner).

## Configuration
- Primary configuration lives in `databricks_linkedin_analytics/databricks.yml` and `databricks_linkedin_analytics/resources/*.yml`.

## Variables
- Default values are defined in `databricks_linkedin_analytics/resources/variables.yml` and may be overridden per target.

## Reference
- Doc index: `docs/README.md`
- Changelog: `CHANGELOG.md`
