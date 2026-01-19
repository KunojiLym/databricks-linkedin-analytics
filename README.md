# Personal LinkedIn Analytics on Databricks: An Example of a Production-Ready Data Product

A compact, code-first reference implementation of a LinkedIn analytics medallion pipeline for Databricks. The documentation is intentionally high-level — the notebooks, SQL, and YAML resource files are the authoritative source of implementation details.

This repo contains a Databricks asset bundle (`databricks_linkedin_analytics/`) with notebooks for ingestion, transformation, and modeling plus resource manifests for jobs, pipelines, and dashboards.

## Quick navigation
- Docs index (recommended starting point): `databricks_linkedin_analytics/docs/README.md`
- Quickstart (deploy & run): `databricks_linkedin_analytics/docs/quickstart.md`
- Code and artifacts: `databricks_linkedin_analytics/src/` and `databricks_linkedin_analytics/resources/`
- Contributing: `databricks_linkedin_analytics/CONTRIBUTING.md`
- TODO / prioritized tasks: `databricks_linkedin_analytics/docs/TODO.md`
- Changelog: `CHANGELOG.md`

Quick example — deploy a development copy of the bundle (Databricks CLI / bundle tooling required)

```powershell
# Authenticate the CLI (if not already configured)
databricks configure --token

# Deploy the Databricks asset bundle to the 'dev' target
databricks bundle deploy --target dev
```

## Repository guidance
- Code-first: open the notebooks in `databricks_linkedin_analytics/src/` and SQL files under `src/.../3. gold modelling/` for concrete logic.
- Keep docs short: `databricks_linkedin_analytics/docs/` contains high-level guidance and pointers; follow the documentation hygiene rules in `databricks_linkedin_analytics/docs/documentation_hygiene.md`.
- When changing configuration or behavior, add a short entry under `Unreleased` in `CHANGELOG.md`.

## Support
- Open a GitHub issue for bugs or feature requests and tag the area (ingestion, transformation, modeling, orchestration).

## License
- See `LICENSE` for license details.
