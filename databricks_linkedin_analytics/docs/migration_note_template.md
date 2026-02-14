# Migration Note Template

Use this template when a change requires data migration, schema updates, or backfills. Save the filled template under `docs/migrations/` or link to it from the PR description.

---

Title: Short summary of the migration (one line)

Date: YYYY-MM-DD

Summary
- Briefly describe the change and why it is needed.

Affected artifacts
- Files: list notebooks, SQL files, and YAML resource files changed (paths)
- Tables: list impacted catalog.schema.table names and partitions

Configuration changes
- Resources: list any `resources/*.yml` or `databricks.yml` updates that affect deployment
- Jobs/pipelines: list job or pipeline IDs that change behavior

Variables affected
- List variable keys from `resources/variables.yml` that were added, removed, or modified
- Note any default value changes or new required variables

Impact
- Describe who and what will be impacted (dashboards, downstream queries, CI)

Migration steps
1. Pre-checks: SQL queries or checks to run before migrating (e.g., verify current row counts)
2. Run: exact commands or job names to execute the migration/backfill
3. Post-checks: queries to validate the migration (row counts, checksum comparisons)

Backfill plan (if applicable)
- Partition ranges and expected runtime per partition
- Resource recommendations (cluster size)

Rollback plan
- Steps to revert in case of failure (restore snapshot, re-run previous pipeline)

Change log entry
- Provide the one-line `CHANGELOG.md` entry to add under the latest dated section.

Tests
- Describe tests to validate the migration (unit tests, notebook smoke runs, SQL validations)

Reference
- Link to relevant docs, notebooks, SQL files, and resource configs

Owner
- Name and contact for the team/entity responsible for the migration

Notes
- Any extra notes or links to additional documentation or monitoring dashboards.
