<!-- Use this template for pull requests. Keep the description concise and link to any related issue. -->

## Summary
<!-- One-line summary of the change -->

## Related issue
<!-- Link issue number or URL, or write 'None' -->

## What changed
- Describe the changes at a high level (no implementation details).

## Checklist
- [ ] Issue linked (if applicable)
- [ ] Description explains why the change is needed
- [ ] Tests added or updated (unit tests / notebook smoke tests)
- [ ] README or docs updated (if user-facing or configuration changed)
- [ ] Notebooks that changed are runnable (smoke-tested locally or in CI)
- [ ] No secrets or credentials committed
- [ ] YAML resources (`resources/*.yml`) validated for syntax

## Documentation hygiene checks
- [ ] Doc pages are short, high-level, and link to authoritative code (see `databricks_linkedin_analytics/docs/documentation_hygiene.md`)
- [ ] If behavior or config changed, add a short `CHANGELOG.md` entry under `Unreleased`
- [ ] If the change involves schema or backfills, attach a migration note (use `docs/migration_note_template.md`) or link to one in `docs/migrations/`

## Migration / Backfill (if applicable)
- Provide short notes and link to `docs/migration_note_template.md` if you filled a migration template.

## Reviewers / Assignees
- @owner or team

## Notes
- Any additional context for reviewers.
