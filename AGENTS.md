# AI Coding Assistants

This project officially supports the following AI coding assistants to help with development, documentation, and code improvement:

- **GitHub Copilot** — GitHub's AI pair programmer for VS Code and JetBrains
- **Cursor** (with `.cursorrules` support) — AI-first code editor with context awareness
- **Claude Code** — Anthropic's Claude integration for code generation and analysis
- **Codex** — GitHub's generative AI model for code completion (via GitHub Copilot)
- **JetBrains AI Chat** — JetBrains' native AI assistant for IntelliJ, PyCharm, etc.

## Quick Start

**For all tools:** See [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) for:
- Project architecture context to feed to AI
- Tool-specific setup and configuration
- Prompting patterns for notebooks, SQL, YAML, and markdown
- Best practices and troubleshooting

**For Cursor:** Review [.cursorrules](.cursorrules) — automatically loaded by Cursor with project guidelines.

**For GitHub Copilot:** Review [.copilotignore](.copilotignore) — defines scope and excludes sensitive files.

## Configuration Files

| Tool | Config File | Purpose |
|------|------------|---------|
| Cursor | [`.cursorrules`](.cursorrules) | Project rules, code style, focus areas |
| GitHub Copilot | [`.copilotignore`](.copilotignore) | File/path exclusions, scope limits |
| Claude Code | [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) | Context prompts in detailed guide |
| Codex | [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) | Uses GitHub context automatically |
| JetBrains AI Chat | [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md) | Manual setup in local IDE settings |

## Project Structure for AI Context

This is a **Databricks medallion architecture** analytics pipeline:

```
Bronze Layer (1. bronze ingestion/):    Excel file ingestion (LinkedIn Company Page API-ready)
Silver Layer (2. silver transformation/): Consolidation, deduplication, enrichment
Gold Layer (3. gold modelling/):         Dimensional & fact tables for analytics
Data Products (4. data product/):        Dashboards and downstream consumption
```

All code lives in **Jupyter notebooks** (`.ipynb`), **SQL DDL** (`.sql`), and **configuration YAML** (`resources/`). 

**Note:** Currently ingests from Excel files already in the landing volume (manually downloaded from LinkedIn analytics interface). Infrastructure supports LinkedIn Company Page API where available (not yet implemented). The actual download process is external to this repository.

## AI Guidelines Summary

✅ **Good prompts for this project:**
- "Explain the medallion pattern in this pipeline and suggest optimizations"
- "Generate a SQL transformation for the silver layer that deduplicates engagement records"
- "Improve this notebook cell for performance and readability"
- "Document this configuration YAML file"

❌ **Avoid asking AI to:**
- Access real LinkedIn Company Page API credentials or API keys
- Generate or suggest debugging of authentication failures
- Commit changes directly; always review AI suggestions first

For detailed setup, prompting patterns, and tool-specific guidance, **see [docs/AGENTS.md](databricks_linkedin_analytics/docs/AGENTS.md)**.
