# Ingestion (Bronze layer)

Maps to the following posts in [Build Your Own LinkedIn Analytics](https://www.yzouyang.com/category/blog-series/build-your-own-linkedin-analytics/): 
- [Part 3: Creating the Data Architecture](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-3-creating-the-data-architecture/)
- [Part 4: Ingesting Data](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-4-ingesting-data/) 

## Goals of the bronze layer
- Ingest Excel files from the landing volume (assumed already downloaded from LinkedIn analytics interface)
- Capture raw data as-is with minimal transformation
- Keep ingestion idempotent and traceable (source filename, load timestamp, status)

## Notebooks and flows

**Note:** This repository covers ingestion from the landing volume into bronze. Excel files are assumed to be already downloaded from the LinkedIn analytics interface and placed in the landing volume (external process, not covered here).

- Daily ingest: `src/linkedin_analytics_jobs/1. bronze ingestion/bronze daily ingest.ipynb`
  - Steps: discover Excel files in landing volume pending folder → parse Excel → normalize columns → write Delta table → move file to processed folder
- Historical ingest: `bronze historical ingest.ipynb` — larger files and backfill patterns
- Post ingest and patching: `bronze post ingest.ipynb` and `bronze post patch ingest.ipynb`

## Design patterns
- Use Delta for ACID and upsert operations
- Include a `_metadata` or `ingestion_audit` columns to track source path and ingestion status
- For idempotency, use a dedup key (e.g., file checksum or (post_id, date))

## Execution
- Prefer running notebooks on Databricks clusters (Jobs). Use `papermill` for parameterized runs.
- For scheduled automated runs, see `resources/jobs.yml` which defines the ingest job triggers.

## Variables
- Many ingestion behaviors are driven by `resources/variables.yml` (landing volume names, pending/processed folder paths). Review and update those defaults for your environment.
- The landing volume is assumed to have `pending/` and `processed/` subdirectories for file organization.

## Landing volume setup (external to this repo)
This repository assumes Excel files are already in the landing volume. The actual download from the LinkedIn analytics interface is **external to this repository**. 

**To set up:**
1. Create a landing volume in Databricks (e.g., `/Volumes/linq_landing/`)
2. Create `pending/` and `processed/` subdirectories
3. Manually download Excel files from LinkedIn analytics interface and upload to the `pending/` folder
4. Configure `resources/variables.yml` with the landing volume path
5. Run the bronze ingestion notebooks, which will move processed files to the `processed/` folder

## Troubleshooting
- If files aren't being discovered, verify they're in the `pending/` folder of the landing volume configured in `resources/variables.yml`
- If a file fails to ingest, check the `errors` folder in the landing volume and job run logs for stack traces.
- Ensure Excel files are properly formatted and located; the job cannot download them from LinkedIn analytics interface (that's an external process)

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
