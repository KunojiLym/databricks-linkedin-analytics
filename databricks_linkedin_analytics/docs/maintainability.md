# Maintainability and code organization

Maps to: Blog Part 9 — Making a Maintainable Pipeline

## Principles
- Keep single responsibility per notebook: ingestion, transformation, modeling
- Extract reusable code into importable modules in `src/` where appropriate
- Keep configuration in `resources/variables.yml` rather than hard-coding

## Repository conventions
- Notebooks: `src/linkedin_analytics_jobs/<stage>/<notebook>.ipynb`
- SQL DDL: `src/linkedin_analytics_jobs/3. gold modelling/pipeline_gold_create/`
- Resource manifests: `databricks_linkedin_analytics/resources/*.yml`

## Versioning and changes
- When changing schema or table names, add a migration note in `docs/maintainability.md` and update `resources/schemas.yml` and `variables.yml`
- For breaking schema changes, plan a backfill run and document how to re-run the gold pipeline for affected partitions

## Testing and CI
- Use `papermill` to parameterize and run key notebooks in CI
- Add small unit tests for any Python modules using `pytest`

## Refactoring tips
- Move commonly-reused functions (parsing, date helpers) from notebooks into a `src/` Python module
- Keep notebooks lightweight and use `%run` or module imports for shared code
