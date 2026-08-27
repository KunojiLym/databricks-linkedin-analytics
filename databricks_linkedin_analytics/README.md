# Databricks LinkedIn Analytics bundle

This directory is the Databricks Asset Bundle for the LinkedIn analytics medallion pipeline (bronze → silver → gold → data product).

**Start here:** [docs/quickstart.md](docs/quickstart.md)

## Layout

- `src/linkedin_analytics_jobs/` — notebooks and SQL for bronze ingestion, silver transformation, gold modeling, and the dashboard
- `src/excel_ingestion_app/` — Streamlit app for Excel uploads to Unity Catalog
- `resources/jobs.yml` — job orchestration (silver tasks, gold pipeline trigger, dashboard refresh)
- `resources/pipelines.yml` — gold `gold_create` pipeline
- `databricks.yml` — bundle targets (`dev`, `prod`)

## Getting started (CLI)

Work from this directory (the one that contains `databricks.yml`). From the repository root that is `cd databricks_linkedin_analytics`.

```bash
databricks auth login --host <workspace-url>
databricks bundle deploy --target dev
```

Personal access tokens and `DATABRICKS_HOST` / `DATABRICKS_TOKEN` environment variables remain optional; see [Databricks CLI authentication](https://docs.databricks.com/aws/en/dev-tools/cli/authentication).

Deployed resources come from `resources/*.yml` — for example the `linkedin transformation` job in [`resources/jobs.yml`](resources/jobs.yml) and the `gold_create` pipeline in [`resources/pipelines.yml`](resources/pipelines.yml). This bundle does not define a template ETL pipeline or `resources/sample_job.job.yml`.

## Testing

Unit tests live in `tests/unit/` and do not need a Databricks workspace. They import application code by adding `src/` to `sys.path`.

From this directory:

```bash
uv sync
uv run pytest
```

CI (`.github/workflows/ci_cd_bundle.yml`) installs dependencies from the **repository-root** `pyproject.toml` (`uv sync`), then runs `uv run pytest tests/unit` in this directory. Both flows should work. Bundle validate/deploy jobs run only when Databricks secrets are set; unit tests always run.

## Documentation

Docs are high-level; implementation details live in notebooks, SQL, and YAML.

- Docs index: [`docs/README.md`](docs/README.md)
- Quickstart: [`docs/quickstart.md`](docs/quickstart.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)
- Orchestration: [`docs/orchestration.md`](docs/orchestration.md)
- Changelog: [`../CHANGELOG.md`](../CHANGELOG.md)

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to propose changes.
