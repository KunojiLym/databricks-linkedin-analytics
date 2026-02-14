# Documentation Hygiene - Guidelines

## Purpose
- Keep documentation concise, high-level, and stable. The code (notebooks, SQL, YAML) is the authoritative source of truth for implementation details.

## When to update docs
- Add or update docs only when the change affects how users operate or deploy the project, or when it clarifies intent (not implementation details).
- For code or transform changes, reference the updated file(s) in the docs rather than copying code.

## Principles
- Short and navigable: limit pages to intent, navigation, and pointers to code.
- Link-first: prefer links to notebooks/SQL/YAML using relative paths (for example: `src/linkedin_analytics_jobs/2. silver transformation/silver metrics consolidation.ipynb`).
- No duplication: avoid pasting large code blocks into docs. If a short example is helpful, include at most 5 lines and point to the source.
- Single source of truth: annotate the code (notebooks/SQL) with in-file comments; docs should summarize and link.

## Changelog and traceability
- If a doc change affects behavior (e.g., configuration names, required variables), add a one-line entry under `Unreleased` in `CHANGELOG.md`.
- For schema or breaking changes, use the migration template: `docs/migration_note_template.md` and add a linked changelog entry.

## Doc checklist (for PRs)
- [ ] Is the page short and focused on intent or navigation?
- [ ] Does the doc link directly to the authoritative file(s)? (notebook, SQL, or YAML)
- [ ] If a code example is included, is it <= 5 lines and clearly labeled as excerpt?
- [ ] If the change affects behavior/config, was `CHANGELOG.md` updated under `Unreleased`?

## Examples
- **Good:** "See `src/.../silver impressions consolidation.ipynb` for the exact transformation logic." (link)
- **Bad:** pasting the entire transformation function into the docs.

## Maintenance notes
- Keep the `docs/` index (`docs/README.md`) up-to-date with links to files and the `docs/TODO.md`.
- When renaming files, update any doc links and add a changelog entry.

## Secrets and local overrides
- If you maintain a local `.databricks/bundle/<target>/variable-overrides.json`, ensure it does not contain secrets or long-lived tokens. Prefer using Databricks Secrets or CI secrets for sensitive values.
- Add `.databricks/bundle/*/variable-overrides.json` to your personal or repository `.gitignore` if you keep local overrides for development convenience.

## Configuration
- Bundle and resource configuration is defined in `databricks_linkedin_analytics/databricks.yml` and `databricks_linkedin_analytics/resources/*.yml`.

## Variables
- Variable defaults are defined in `databricks_linkedin_analytics/resources/variables.yml` and may be overridden per target.

## Reference
- Doc index: `docs/README.md`
- Changelog: `CHANGELOG.md`
- Migration template: `docs/migration_note_template.md`
