# Architecture — Reference overview

Maps to: Blog Part 2 — Choosing the Data Source / Architecture overview

## Purpose
This page describes the medallion architecture used in this project (Landing → Bronze → Silver → Gold), the orchestration components, and where artifacts live in the repository.

## Repo references
- `databricks_linkedin_analytics/databricks.yml` — bundle targets and deployment settings
- `databricks_linkedin_analytics/resources/*.yml` — pipelines, jobs, dashboards, variables
- `databricks_linkedin_analytics/src/` — ingestion, transformation notebooks and SQL for modeling

## Components
- Databricks Workspace: notebooks and jobs are deployed via the bundle
- Landing (raw files): Excel/CSV files stored in a landing catalog/volume
- Bronze: raw ingestion Delta tables (one table per logical source)
- Silver: cleaned and consolidated tables (impressions, engagements, posts, profiles)
- Gold: dimensional and fact tables for consumption by dashboards
- Orchestration: Databricks jobs and pipelines configured in `resources/jobs.yml` and `resources/pipelines.yml`

## Where to find code
- Bronze ingestion notebooks: `src/linkedin_analytics_jobs/1. bronze ingestion/`
- Silver transformation notebooks: `src/linkedin_analytics_jobs/2. silver transformation/`
- Gold modeling SQL: `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/`
- Dashboards: `src/linkedin_analytics_jobs/4. data product/LinkedIn Statistics.lvdash.json`

## Diagrams
- Recommended: add `docs/images/architecture.svg` for a visual overview. For quick diagrams you can use Mermaid diagrams inline.

## Deployment model
- The repository is deployed as a Databricks asset bundle. Use `databricks bundle deploy --target dev` to create a development copy. See `docs/quickstart.md` for exact commands.

This page should be used as the high-level starting point for new contributors and operators.
