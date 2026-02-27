# Quickstart - Deploy to Databricks (Dev) and run notebooks

This quickstart gives exact commands and environment overview to deploy the `databricks_linkedin_analytics` bundle to a Databricks development workspace and run notebooks locally when applicable.

Related blog posts: Part 10 (Orchestrating and Automating the Pipeline)

Prerequisites
- Databricks CLI installed and configured: `databricks configure --token` (or use a named profile)
- Optional: `dbx` (Databricks CI/CD tool) installed for advanced deployments
- `papermill` or `nbconvert` if you want to execute notebooks locally

Environment variables (recommended)
- DATABRICKS_HOST - your Databricks workspace URL
- DATABRICKS_TOKEN - personal access token
- LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET - LinkedIn API credentials (store securely)
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

Dev variable overrides (optional)
- During development you can provide per-target overrides for bundle variables by creating a JSON file at `.databricks/bundle/<target>/variable-overrides.json` (for example `.databricks/bundle/dev/variable-overrides.json`). This file is used by local bundle tooling to inject specific variable values when deploying to the matching target.

Example (your local dev override)
- Example file path: `.databricks/bundle/dev/variable-overrides.json`
- Example content (replace sensitive values with placeholders):

```json
{
  "linkedin_profile_name": "YourProfileNameHere",
  "warehouse_id": "your_warehouse_id_here",
  "pipeline_runner": "your_pipeline_runner_name_here"
}
```

Guidance
- Do not commit secrets or tokens into this file. If you need to store secrets for CI or shared environments, use secret stores (Databricks secrets, environment variables, or CI secrets).
- If you keep a local `variable-overrides.json` for convenience, add `.databricks/bundle/*/variable-overrides.json` to your global or repo `.gitignore` to avoid accidental commits.
- For production deployments, prefer passing variables via secure CI/CD pipelines or Databricks workspace variables instead of committing overrides in the repo.

## 4. Quality & Testing

This project includes a suite of unit tests to verify core logic and prevent regressions.

### Running tests locally
We use `pytest` and `uv` to manage the test environment. You can run tests locally without an active Databricks connection:

```bash
# Navigate to the bundle directory
cd databricks_linkedin_analytics

# Install dependencies and run tests
uv sync
uv run pytest
```

### CI/CD
A GitHub Actions workflow (`.github/workflows/ci_cd_bundle.yml`) automatically runs tests and validates bundle syntax on every pull request.

## Configuration
- Bundle targets and environment settings: `databricks_linkedin_analytics/databricks.yml`
- Resources (jobs, pipelines, dashboards, monitoring): `databricks_linkedin_analytics/resources/*.yml`

## Variables
- Base defaults: `databricks_linkedin_analytics/resources/variables.yml`
- Override file: `.databricks/bundle/<target>/variable-overrides.json`

## Reference
- Orchestration: `docs/orchestration.md`
- Ingestion: `docs/ingestion.md`

Troubleshooting
- If your deploy fails due to missing variables, check this overrides file as well as `resources/variables.yml` for required keys.

For more details and examples, see `docs/orchestration.md` and `docs/ingestion.md`.
