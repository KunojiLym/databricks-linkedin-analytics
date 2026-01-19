# Quickstart — Deploy to Databricks (Dev) and run notebooks

This quickstart gives exact commands and environment overview to deploy the `databricks_linkedin_analytics` bundle to a Databricks development workspace and run notebooks locally when applicable.

Related blog posts: Part 10 (Orchestrating and Automating the Pipeline)

Prerequisites
- Databricks CLI installed and configured: `databricks configure --token` (or use a named profile)
- Optional: `dbx` (Databricks CI/CD tool) installed for advanced deployments
- `papermill` or `nbconvert` if you want to execute notebooks locally

Environment variables (recommended)
- DATABRICKS_HOST — your Databricks workspace URL
- DATABRICKS_TOKEN — personal access token
- LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET — LinkedIn API credentials (store securely)
- Optional override variables referenced in `resources/variables.yml` (e.g., catalogs, schemas, volumes)

Quick deploy (Databricks Bundle)
1. Authenticate the CLI:

    databricks configure --token

2. Deploy the bundle to the `dev` target (development mode):

    databricks bundle deploy --target dev

Notes:
- The `dev` target preserves schedules in pause and prefixes deployed resources for isolation.
- To deploy to production, use `--target prod` and ensure service principals/variables are configured.

Alternative: push notebooks and resources via CLI
- Upload notebooks folder to workspace (example):

    databricks workspace import_dir "databricks_linkedin_analytics/src" "/Workspace/Users/you/LinkedInAnalytics/src" --overwrite

- Create jobs or pipelines using the CLI by converting `resources/*.yml` to the appropriate JSON or using the Databricks UI.

Running notebooks locally (lightweight)
- Notebooks expect Spark; local runs are useful for small parameterized tests using `papermill`:

    papermill "src/linkedin_analytics_jobs/1. bronze ingestion/bronze daily ingest.ipynb" output.ipynb -p LINKEDIN_PROFILE_NAME "your_profile"

- For full runs, execute notebooks on a Databricks cluster (via Jobs or interactive runs).

Variables reference
- The repository defines many deploy-time variables in `databricks_linkedin_analytics/resources/variables.yml` (catalog names, schema names, volume names, table names). Use those defaults for a development deployment and override them in production.

Troubleshooting
- If deployment fails, check `databricks bundle` output for missing variables or permissions. Ensure the Databricks host and token are valid.
- For job failures, review the job run logs in the Databricks Jobs UI.

For more details and examples, see `docs/orchestration.md` and `docs/ingestion.md`.
