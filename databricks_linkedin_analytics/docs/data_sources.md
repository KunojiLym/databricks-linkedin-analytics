# Data sources and contracts

Maps to: Blog Part 3 — Creating the Data Architecture / Data Sources

## Overview
This project ingests LinkedIn profile and content metrics exported as Excel/CSV files and optionally via LinkedIn APIs where available. The repository includes example notebooks and configuration for both daily and historical ingestion.

## Relevant files
- Ingestion POC: `src/linkedin_analytics_jobs/0. poc and utility/linkedin_pipeline_poc.ipynb`
- Landing schema and volumes: `resources/schemas.yml`
- Variable defaults: `resources/variables.yml`

## Data contracts
- Landing files are expected in the `content_daily`, `historical_daily`, `posts`, and `patch` volumes (see `variables.yml` defaults)
- Bronze tables are named via variables in `resources/variables.yml` (e.g., `bronze_profile_metrics_table`, `bronze_post_metrics_table`)

## Sample shapes and notes
- Profile daily totals: expected numeric columns for impressions, engagements, followers
- Per-post metrics: post id, timestamp, impressions, likes, comments, shares

## Where to find ingestion examples
- `src/linkedin_analytics_jobs/1. bronze ingestion/bronze daily ingest.ipynb` — daily Excel ingestion
- `src/linkedin_analytics_jobs/1. bronze ingestion/bronze historical ingest.ipynb` — historical batch ingest
- `src/linkedin_analytics_jobs/1. bronze ingestion/bronze post ingest.ipynb` — post-level ingest

## If you extend sources
- Document expected file layout and column names in this doc and add a notebook under `src/` showing how to ingest it.
