# Modeling (Gold layer)

Maps to: Blog Part 6 — Modelling the Data

## Overview
- The gold layer contains dimensional and fact tables optimized for analytics and dashboards. The repository includes SQL DDL used by the gold pipeline.

## Relevant files
- `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/create_dim_date_table.sql`
- `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/create_dim_timestamp_table.sql`
- `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/create_fct_daily_post_stats_table.sql`
- `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/create_fct_daily_profile_stats_table.sql`

## Table design
- Dimension tables: date, timestamp (standardized keys and formats)
- Fact tables: daily aggregates for posts and profiles, partitioned by date for performance

## Performance guidance
- Partition fact tables by date (e.g., `event_date`) for common time-range queries
- Cache or materialize hot aggregations used by dashboards

## Deployment
- The gold pipeline is defined in `resources/pipelines.yml` and executed as a Databricks pipeline job. See `docs/orchestration.md` for how the pipeline is wired.

## Consumption
- Dashboards and SQL queries should reference the gold catalog/schema configured in `resources/variables.yml`.
