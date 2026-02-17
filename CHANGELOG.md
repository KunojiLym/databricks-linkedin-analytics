# Changelog

All notable changes to this repository will be documented in this file.

Format follows a simple dated "YYYY-MM-DD" style. Add a dated section when changes are merged; use `Unreleased` only if you later adopt a formal release workflow.

## [2026-02-18]

### Added
- AI coding assistants support documentation and configuration files: [AGENTS.md](AGENTS.md) for quick reference and [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) for comprehensive setup guide
- Tool-specific configuration files: `.copilotignore` (GitHub Copilot scope) and `.cursorrules` (Cursor AI rules)
- Support for 5 AI coding assistants: GitHub Copilot, Cursor, Claude Code, Codex, and JetBrains AI Chat
- Setup instructions in [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) covering project context, tool-specific configurations, prompting patterns for notebooks/SQL/YAML/markdown, and best practices
- Clarified ingestion documentation: Bronze layer ingests from landing volume (Excel files manually uploaded); actual download from LinkedIn analytics interface is external to this repository
- Enhanced [docs/ingestion.md](databricks_linkedin_analytics/docs/ingestion.md) with landing volume setup guide and clarified scope boundaries

---

## [2026-02-14]

### Added
- Monitoring resources, email notification configuration, and related pipeline/job variables.
- Additional .gitignore rules.

### Fixed
- Default support email now uses the workspace user email to ensure notification delivery.

---

## [2026-01-19] - Initial docs consolidation

### Added
- Initial set of high-level docs and changelog file.

---

How to use this file
- For small documentation or code changes, add an entry under the latest dated section with a concise description.
- If you later adopt a release workflow, use an `Unreleased` section and move items into a dated section when you tag a release.

Example entry
- `### Fixed\n- Corrected variable name in resources/variables.yml`
