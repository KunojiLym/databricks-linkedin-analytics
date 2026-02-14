# Ingestion (Bronze layer)

Maps to the following posts in [Build Your Own LinkedIn Analytics](https://www.yzouyang.com/category/blog-series/build-your-own-linkedin-analytics/): 
- [Part 3: Creating the Data Architecture](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-3-creating-the-data-architecture/)
- [Part 4: Ingesting Data](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-4-ingesting-data/) 

## Goals of the bronze layer
- Capture raw data as-is with minimal transformation
- Keep ingestion idempotent and traceable (source filename, load timestamp, status)

## Notebooks and flows
- Daily ingest: `src/linkedin_analytics_jobs/1. bronze ingestion/bronze daily ingest.ipynb`
  - Steps: discover files in landing volume -> parse Excel -> normalize columns -> write Delta table
- Historical ingest: `bronze historical ingest.ipynb` - larger files and backfill patterns
- Post ingest and patching: `bronze post ingest.ipynb` and `bronze post patch ingest.ipynb`

## Design patterns
- Use Delta for ACID and upsert operations
- Include a `_metadata` or `ingestion_audit` columns to track source path and ingestion status
- For idempotency, use a dedup key (e.g., file checksum or (post_id, date))

## Execution
- Prefer running notebooks on Databricks clusters (Jobs). Use `papermill` for parameterized runs.
- For scheduled automated runs, see `resources/jobs.yml` which defines the ingest job triggers.

## Troubleshooting
- If a file fails, check the `errors` folder in the landing volume and job run logs for stack traces.

## Configuration
- Ingest jobs and file-arrival triggers live in `resources/jobs.yml`.
- Landing volumes and schemas are defined in `resources/schemas.yml`.

## Variables
- `landing_catalog`, `landing_content_daily_volume`, `landing_content_historical_volume`, `landing_posts_volume`, `landing_patch_volume`: landing storage locations.
- `ingestion_folder`, `processed_folder`, `errors_folder`, `post_patch_subfolder`: input/output folders for ingest.
- `bronze_*_table`: bronze table names produced by ingestion.

## Reference
- Ingest notebooks: `src/linkedin_analytics_jobs/1. bronze ingestion/`
- Job triggers: `resources/jobs.yml`
