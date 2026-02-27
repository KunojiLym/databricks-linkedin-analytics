# Changelog

All notable changes to this repository will be documented in this file.

Format follows a simple dated "YYYY-MM-DD" style. Add a dated section when changes are merged; use `Unreleased` only if you later adopt a formal release workflow.

## [2026-02-19]

### Added
- **Excel Ingestion App**: Implemented a Streamlit-based Databricks App for multi-file Excel uploads to Unity Catalog.
- **Genie Space**: Instructions for manually deploying Databricks Genie for AI-powered data analytics.
- **Modular Architecture**: 
    - Created `excel_validator.py` and `file_validation.py` for ingestion logic in App `utils` folder.
    - Centralized pipeline helpers in `pipeline_utils.py` in Jobs `utils` folder for parameter handling and time-series date filling.
- **Unit Testing Framework**: Implemented 14 tests using `pytest` and `unittest.mock` for local-first verification. Fixed argument order in `test_pipeline_utils.py` to prevent CI failures in strictly-typed environments.
- **CI/CD Integration**: Added GitHub Actions workflow for automated bundle validation and test execution. Hardened CI workflow with conditional step execution for safer OSS fork support.
- **Package Standardization**: Added `__init__.py` files across all directories for proper Python packaging.
- **Dashboards**: Created "Content Deep Dive" and "Engagement Analysis" pages.

### Refactored
- **Resource Management**: Extracted application-specific configurations into a dedicated `resources/apps.yml`.
- **Notebook Synchronization**: Patched silver transformation notebooks to use centralized utilities with robust pathing.

### Maintainability & CI/CD
- **Centralized Secrets**: Optimized GitHub Actions to use job-level environment variables for Databricks authentication.
- **Graceful CI**: Configured workflow steps to automatically skip host-dependent validation in forked repositories while maintaining 100% unit test coverage for all contributors.

### Documentation
- Significant updates to `README.md`, `quickstart.md`, and `maintainability.md` covering new testing patterns and development workflows.

---

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
