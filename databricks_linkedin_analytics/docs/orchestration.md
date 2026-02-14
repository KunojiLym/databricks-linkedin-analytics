# Orchestration - Jobs and Pipelines

Maps to the following post in [Build Your Own LinkedIn Analytics](https://www.yzouyang.com/category/blog-series/build-your-own-linkedin-analytics/): 
- [Part 8: Orchestrating and Automating the Pipeline](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-8-orchestrating-and-automating-the-pipeline/)

## Overview
- Orchestration is implemented using Databricks jobs and the Pipelines feature. The `databricks.yml` bundle wires resources in `resources/*.yml` into the workspace.

## Key resources
- `resources/jobs.yml` - composite job that runs silver transformations, triggers the gold pipeline, and refreshes dashboards
- `resources/pipelines.yml` - gold pipeline configuration and library inclusions
- `databricks_linkedin_analytics/databricks.yml` - bundle metadata and targets

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

## Configuration
- Jobs: `resources/jobs.yml`
- Pipelines: `resources/pipelines.yml`
- Bundle targets: `databricks_linkedin_analytics/databricks.yml`

## Variables
- `pipeline_runner`: service principal used to deploy/run pipelines.
- `warehouse_id`: SQL warehouse used by dashboard refresh tasks.
- `dashboard_subscriber`: dashboard subscription target.
- `support_email`: failure notification recipient.

## Reference
- Job tasks and triggers: `resources/jobs.yml`
- Pipeline definitions: `resources/pipelines.yml`

For a breakdown of scheduled triggers and file-arrival triggers, see `resources/jobs.yml`.
