# Documentation - Consolidated index

This is the consolidated documentation index. The goal is to be easy to navigate without reading the original blog posts and intentionally high-level: refer to the code for details.

## How the docs are organized
- High-level pages (this index + the pages listed below) provide intent, navigation, and pointers to the code.
- Implementation details live in the notebooks (`src/.../*.ipynb`), SQL files (`src/.../*.sql`) and resource YAML files (`databricks_linkedin_analytics/resources/*.yml`).

## Navigation (one-line summaries)
<<<<<<< HEAD
- `docs/quickstart.md` — Quick start to deploy the project to Databricks (commands and env vars).
- `docs/AGENTS.md` — Setup and usage guide for AI coding assistants (GitHub Copilot, Cursor, Claude, Codex, JetBrains AI Chat).
- `docs/architecture.md` — System architecture and medallion layer overview (Landing → Bronze → Silver → Gold).
- `docs/data_sources.md` — Sources and expected file shapes; where to add new sources.
- `docs/ingestion.md` — Bronze ingestion patterns; where to find daily and historical ingest notebooks.
- `docs/transformation.md` — Silver transformation patterns; how notebooks map to silver tables.
- `docs/modeling.md` — Gold modeling and the fact/dimension tables used by dashboards.
- `docs/dashboard_design.md` — Dashboard goals and the LinkedIn Statistics data product.
- `docs/orchestration.md` — Job/pipeline wiring, triggers, and failure-retry guidance.
- `docs/maintainability.md` — How to keep the pipeline maintainable and where to edit configuration.
- `docs/observability.md` — What to monitor and quick SQL checks for pipeline health.
- `docs/TODO.md` — Actionable tasks and prioritized next steps for maintainers.
=======
- `docs/quickstart.md` - Quick start to deploy the project to Databricks (commands and env vars).
- `docs/architecture.md` - System architecture and medallion layer overview (Landing -> Bronze -> Silver -> Gold).
- `docs/data_sources.md` - Sources and expected file shapes; where to add new sources.
- `docs/ingestion.md` - Bronze ingestion patterns; where to find daily and historical ingest notebooks.
- `docs/transformation.md` - Silver transformation patterns; how notebooks map to silver tables.
- `docs/modeling.md` - Gold modeling and the fact/dimension tables used by dashboards.
- `docs/dashboard_design.md` - Dashboard goals and the LinkedIn Statistics data product.
- `docs/orchestration.md` - Job/pipeline wiring, triggers, and failure-retry guidance.
- `docs/maintainability.md` - How to keep the pipeline maintainable and where to edit configuration.
- `docs/observability.md` - What to monitor and quick SQL checks for pipeline health.
- `docs/TODO.md` - Actionable tasks and prioritized next steps for maintainers.
>>>>>>> origin/main

## Quick pointers
- **Code-first:** open notebooks and SQL files in `src/linkedin_analytics_jobs/` for concrete examples.
- **Config:** `databricks_linkedin_analytics/resources/variables.yml` controls table and volume names.
- **Dev overrides:** You can create `.databricks/bundle/dev/variable-overrides.json` for local per-target overrides - see `docs/quickstart.md` for an example and guidance about not committing secrets.
- **Deployment:** `databricks_linkedin_analytics/databricks.yml` and `resources/*.yml` define the bundle, pipelines and jobs.
- **Dashboards:** `src/linkedin_analytics_jobs/4. data product/LinkedIn Statistics.lvdash.json` and `resources/dashboards.yml`.

## Configuration
- Bundle targets and environment settings: `databricks_linkedin_analytics/databricks.yml`
- Resources (jobs, pipelines, dashboards, monitoring): `databricks_linkedin_analytics/resources/*.yml`

## Variables
- Base defaults: `databricks_linkedin_analytics/resources/variables.yml`
- Optional per-target overrides: `.databricks/bundle/<target>/variable-overrides.json`

## Reference
- Changelog: `CHANGELOG.md`
- Documentation hygiene: `docs/documentation_hygiene.md`
- Migration template: `docs/migration_note_template.md`

## Editing the docs
- Keep pages short. Prefer pointing to code sections and notebook paths rather than duplicating code.
- If you update a notebook or SQL that materially affects users, add a short line to `CHANGELOG.md` and update the relevant page in `docs/`.

## Documentation hygiene
- See `docs/documentation_hygiene.md` for short guidelines on what to document and when to add changelog entries.
- Use `docs/migration_note_template.md` when making schema or data-migration changes; place filled templates under `docs/migrations/` or link them from PRs.

## Support
- To report issues or request features, open a GitHub issue referencing the area (ingestion, transformation, modeling, orchestration).

Thank you for keeping documentation focused and code-centric.
