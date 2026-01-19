# Orchestration — Jobs and Pipelines

Maps to: Blog Part 8 — Orchestrating and Automating the Pipeline

## Overview
- Orchestration is implemented using Databricks jobs and the Pipelines feature. The `databricks.yml` bundle wires resources in `resources/*.yml` into the workspace.

## Key resources
- `resources/jobs.yml` — composite job that runs silver transformations, triggers the gold pipeline, and refreshes dashboards
- `resources/pipelines.yml` — gold pipeline configuration and library inclusions
- `databricks_linkedin_analytics/databricks.yml` — bundle metadata and targets

## Typical flow
1. Ingest files to landing volume (file arrival trigger or scheduled job)
2. Bronze ingestion job runs and writes staging tables
3. Silver transformation notebook tasks run (see `resources/jobs.yml` tasks)
4. Gold pipeline `gold_create` runs to produce dimensional/fact tables
5. Dashboard refresh task runs using the freshly built gold tables

## Failure handling
- Jobs may be configured with retries (see `resources/jobs.yml` for `max_retries` and retry intervals)
- For manual backfills, run the ingest notebooks with historical date parameters or call SQL to rebuild gold partitions

## Operational commands
- Use `databricks bundle deploy` to push the job/pipeline definitions
- Use the Jobs UI to manually trigger or re-run failed tasks

For a breakdown of scheduled triggers and file-arrival triggers, see `resources/jobs.yml`.
