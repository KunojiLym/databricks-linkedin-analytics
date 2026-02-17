# AI Coding Assistants: Detailed Setup & Prompting Guide

This guide provides comprehensive setup instructions, project context, and best practices for using AI coding assistants with the databricks-linkedin-analytics project.

## Table of Contents

1. [Project Context for AI](#project-context-for-ai)
2. [Tool-Specific Setup](#tool-specific-setup)
3. [Prompting Patterns by Artifact Type](#prompting-patterns-by-artifact-type)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)

---

## Project Context for AI

### Architecture Overview

This is a **Databricks medallion architecture** reference implementation for LinkedIn analytics:

```
Bronze Layer  → Silver Layer  → Gold Layer  → Data Products
(Raw)         (Cleansed)     (Modeled)     (Dashboards)
```

**Key Characteristics:**
- **Code format:** Jupyter notebooks (`.ipynb`) + SQL DDL (`.sql`) + YAML configs (`resources/`)
- **Python version:** 3.10–3.13
- **Code formatter:** Black (line-length: 125)
- **Data orchestration:** Databricks Asset Bundles (`databricks.yml`)
- **Testing:** pytest for unit tests
- **Source:** Excel/CSV files (infrastructure supports LinkedIn Company Page API where available)

### Project Layers

| Layer | Location | Purpose | Key Files |
|-------|----------|---------|-----------|
| **Bronze** | `src/linkedin_analytics_jobs/1. bronze ingestion/` | Raw data ingest from Excel files in landing volume (externally downloaded from LinkedIn analytics interface); infrastructure supports LinkedIn Company Page API (not yet implemented) | `bronze daily ingest.ipynb`, `bronze post ingest.ipynb` |
| **Silver** | `src/linkedin_analytics_jobs/2. silver transformation/` | Consolidation, deduplication, enrichment of metrics | `silver engagements consolidation.ipynb`, `silver impressions consolidation.ipynb` |
| **Gold** | `src/linkedin_analytics_jobs/3. gold modelling/` | SQL DDL for dimension & fact tables | `create_dim_date_table.sql`, `create_fct_daily_post_stats_table.sql` |
| **Data Products** | `src/linkedin_analytics_jobs/4. data product/` | Dashboards and downstream analytics | `LinkedIn Statistics.lvdash.json` |

### Naming Conventions

- **Schemas:** `linkedin_analytics_bronze`, `linkedin_analytics_silver`, `linkedin_analytics_gold`
- **Tables:** `bronze_*` (raw), `silver_*` (cleaned), `fct_*` / `dim_*` (modeled)
- **Notebooks:** Descriptive verb phrases (e.g., "silver engagements consolidation") with layer prefix
- **Variables:** Defined in [resources/variables.yml](../resources/variables.yml)

### Configuration Files

- **[resources/dashboards.yml](../resources/dashboards.yml)** — Databricks SQL dashboard definitions
- **[resources/jobs.yml](../resources/jobs.yml)** — Job orchestration config
- **[resources/pipelines.yml](../resources/pipelines.yml)** — Delta Live Tables pipeline definitions
- **[resources/schemas.yml](../resources/schemas.yml)** — Schema and table metadata
- **[resources/variables.yml](../resources/variables.yml)** — Shared variables and secrets references

**When prompting about configs:** Refer to specific resource files and explain what orchestration layer (Bronze, Silver, Gold) the config affects.

---

## Tool-Specific Setup

### GitHub Copilot

**Setup:**
1. Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) in VS Code or JetBrains
2. Authenticate with your GitHub account
3. Review [.copilotignore](../../.copilotignore) — defines files excluded from suggestions

**Key points:**
- Copilot will avoid suggesting code for files matching `.copilotignore` patterns
- Best used for: SQL generation, Python cell completion, YAML config suggestions
- **Avoid:** Providing real LinkedIn Company Page API keys or credentials in any prompt

**Typical use case:**
```
User: "Write a SQL query for silver_impressions that counts daily impressions by post_id"
→ Copilot generates: SELECT post_id, COUNT(*) as daily_impressions FROM silver_impressions GROUP BY post_id
```

---

### Cursor

**Setup:**
1. Install [Cursor](https://www.cursor.com/) — AI-first code editor based on VS Code
2. The [.cursorrules](.cursorrules) file is **automatically loaded** by Cursor
3. Configure your API key for Claude (if using Claude backend) in Cursor settings

**Key points:**
- `.cursorrules` was designed specifically for this purpose; commit it to your repo
- Cursor reads `.cursorrules` at project root for project-wide guidelines
- Excellent for multi-file edits and understanding project patterns
- Can use `@codebase` to reference files and `@docs` for documentation context

**Typical use case:**
```
User: "@codebase How does silver engagements consolidation join to bronze data?"
→ Cursor analyzes notebooks and explains the transformation logic
```

---

### Claude Code

**Setup:**
1. Install Claude extension or use Claude web interface with code context
2. Manually provide project summary (below) when starting new sessions
3. Use VS Code or Cursor to provide file context via `@` references

**Project summary to provide Claude:**
```
This is a Databricks medallion pipeline for LinkedIn analytics:
- Bronze (ingestion from Excel files in landing volume; supports Company Page API)
- Silver (consolidation & enrichment)
- Gold (SQL-modeled dimension/fact tables)
- Data products (dashboards)

Code is in Jupyter notebooks (.ipynb) and SQL files.
Config is in resources/ YAML files.
Naming: schema names have _bronze/_silver/_gold suffixes.
Testing with pytest. Code style: Black (125-char lines).

Note: Excel files are manually downloaded from LinkedIn analytics interface and uploaded to landing volume. Repo covers ingestion from landing to bronze, not the download itself.
```

**Key points:**
- Claude excels at refactoring complex notebook logic and SQL transformations
- Ask Claude to review notebooks cell-by-cell with suggestions
- Good for documentation and explaining medallion patterns

**Typical use case:**
```
User: "Refactor this Python cell [paste code] to improve readability and performance"
→ Claude suggests improvements with explanations
```

---

### Codex (via GitHub Copilot)

**Setup:**
- Codex is the underlying model for GitHub Copilot; no separate setup needed
- Automatically uses GitHub context from the repository

**Key points:**
- Works best when your code repo is on GitHub (public or private in your account)
- Copilot uses codebase context to improve suggestions
- Can't directly access credentials, so avoid asking about authentication

**Typical use case:**
```
User (in GitHub web): "Generate a test for this notebook"
→ Copilot suggests pytest code based on repo patterns
```

---

### JetBrains AI Chat

**Setup:**
1. In PyCharm or IntelliJ, go to **Settings → Tools → AI Assistant**
2. Configure your preferred AI backend (OpenAI, Claude, or JetBrains' built-in)
3. **Manual local configuration** — no shared config file (these are IDE settings, not repo config)

**Key points:**
- Available in context menu: right-click file/selection → "AI Actions"
- Can explain code, generate tests, and suggest refactorings
- Good for quick in-IDE explanations without leaving the editor

**Typical use case:**
```
User: Right-click on notebook cell → "Explain this code"
→ AI Chat explains the medallion transformation in the selected cell
```

---

## Prompting Patterns by Artifact Type

### Notebook Cells (Python in `.ipynb`)

**Context to provide:**
- Which layer: Bronze (ingestion from landing volume), Silver (transformation), or Gold (modeling)
- What data: e.g., "daily LinkedIn engagement metrics from Excel files in landing volume"
- Transform goal: e.g., "deduplicate by post_id and date"

**Example prompts:**

```
Good ✅:
"In the silver layer, write a PySpark transformation that consolidates engagement 
records (filtered to last 30 days) and deduplicates by post_id, keeping the 
most recent record."

Also good ✅:
"This bronze ingestion notebook reads Excel files uploaded to the landing volume from LinkedIn analytics interface. 
How can I add error handling for missing columns and data type mismatches?"

Avoid ❌:
"Write code for LinkedIn" (too vague)
"Debug the API key issue" (sensitive; don't paste credentials)
```

**What to expect:**
- AI will generate PySpark/Pandas code patterns
- Output: DataFrame operations, SQL expressions
- Good for: data transformations, performance optimizations, error handling

---

### SQL Queries (`.sql`)

**Context to provide:**
- Source tables: bronze_* or silver_* (include layer prefix)
- Dimension/fact table purpose: e.g., "daily post statistics fact table"
- Join keys and filters

**Example prompts:**

```
Good ✅:
"Create a SQL DDL for fct_daily_post_stats that joins dim_date (by date_key) 
and dim_post (by post_id) from silver layer tables, aggregating daily impressions 
and engagement counts. Include a surrogate key."

Also good ✅:
"Optimize this query for performance: [paste query]. We're joining 
silver_impressions (100M rows) to silver_posts (1M rows)."

Avoid ❌:
"Write a query" (no context)
"Fix the production query" (might expose sensitive schema details)
```

**What to expect:**
- AI will generate T-SQL/Spark SQL DDL following dimensional modeling patterns
- Output: `CREATE TABLE`, `CREATE VIEW`, aggregate functions
- Good for: dimensional design, query optimization, window functions

---

### Configuration Files (YAML in `resources/`)

**Context to provide:**
- What the config controls: jobs, pipelines, schemas, variables
- How it integrates: e.g., "this job orchestrates the silver transformation"

**Example prompts:**

```
Good ✅:
"Review this jobs.yml config for the silver transformation layer. 
Suggest improvements for error handling and retry logic. [paste YAML]"

Also good ✅:
"Generate a pipelines.yml config for a Delta Live Table that ingests 
from bronze_daily_posts and outputs to silver_posts_enriched."

Avoid ❌:
"Fix the deployment error" (too vague without YAML context)
```

**What to expect:**
- AI will generate/improve YAML structure following Databricks Asset Bundle conventions
- Output: Job task definitions, pipeline stages, schema definitions
- Good for: config validation, orchestration patterns, environment variable setup

---

### Documentation & Markdown

**Context to provide:**
- Audience: e.g., "for new contributors", "for operations team"
- Scope: e.g., "explain the silver layer transformation steps"

**Example prompts:**

```
Good ✅:
"Write a concise markdown section explaining the medallion architecture 
for the GitHub README, targeting new contributors. Include links to 
source files in src/linkedin_analytics_jobs/."

Also good ✅:
"Document this notebook's cells [paste notebook] with a markdown summary 
of inputs, transformations, and outputs."

Avoid ❌:
"Write docs" (no context)
```

**What to expect:**
- AI will generate markdown with proper formatting, links, and structure
- Output: Section headings, code blocks, relative links
- Good for: quickstart guides, architecture explanations, runbooks

---

## Best Practices

### ✅ Do

1. **Provide layer context:** Always mention Bronze/Silver/Gold when asking about transformations
2. **Include source files:** Reference specific notebooks, SQL files, or YAML configs
3. **Specify constraints:** Mention performance targets, data quality rules, or naming conventions
4. **Review suggestions:** Always review AI-generated code before running or committing
5. **Test locally:** Run AI-generated code in a dev environment first
6. **Link to code:** When documenting, link to [actual source files](../src/linkedin_analytics_jobs/)
7. **Use file context:** Provide example data schema, row counts, or transformation logic

### ❌ Don't

1. **Paste credentials:** Never share LinkedIn Company Page API keys, Databricks tokens, or secrets with AI
2. **Ask about auth failures:** Don't ask AI to debug authentication without removing credentials
3. **Use for testing only:** Don't rely solely on AI suggestions; validate with actual Databricks clusters
4. **Ignore project patterns:** Don't ask AI to break conventions (naming, layer structure, code style)
5. **Skip the docs:** Don't assume AI suggestions match [documentation_hygiene.md](./documentation_hygiene.md) standards
6. **Commit without review:** Always review AI-generated code for logic, security, and maintainability

---

## Troubleshooting

### Issue: AI Suggests Code That Doesn't Follow Project Conventions

**Solution:**
- Reference specific files in prompts: "Following the pattern in `silver engagements consolidation.ipynb`, write a similar cell for..."
- Mention naming conventions: "Use the naming pattern: bronze_*, silver_*, fct_*, dim_*"
- Link to style guides: "Follow the code style in [documentation_hygiene.md](./documentation_hygiene.md)"

### Issue: AI Suggests Code That References Undefined Tables

**Solution:**
- Provide the schema names explicitly: "Join silver_impressions to silver_posts using post_id"
- Reference [resources/schemas.yml](../resources/schemas.yml) for table definitions
- Ask: "What tables are available in the silver layer?" and let AI infer from project structure

### Issue: Copilot or Cursor Not Picking Up Project Context

**Solution:**
- Ensure [.copilotignore](../../.copilotignore) and [.cursorrules](../../.cursorrules) are committed and pushed to GitHub
- Restart the editor (VS Code, Cursor, PyCharm)
- Verify file is not in an ignored path (check `.gitignore`)

### Issue: AI Generates Overly Complex SQL

**Solution:**
- Ask AI to "simplify and optimize" the query
- Provide performance constraints: "This needs to complete in under 30 seconds on a 4-core cluster"
- Reference similar queries in existing SQL files: "Follow the pattern in `create_fct_daily_post_stats_table.sql`"

### Issue: Claude Code Session Loses Context

**Solution:**
- Reattach context at start of new session with the [project summary](#claude-code) above
- Use `@docs` (if available) to point to markdown docs
- Manually reference key files: "See [ingestion.md](./ingestion.md) for the Bronze layer design"

---

## Quick Reference: Tool Comparison

| Feature | Copilot | Cursor | Claude | Codex | JetBrains |
|---------|---------|--------|--------|-------|-----------|
| **Notebooks (.ipynb)** | ✅ Inline | ✅ Excellent | ✅ Good | ✅ Good | ✅ Good |
| **SQL (.sql)** | ✅ Good | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good |
| **YAML configs** | ✅ Good | ✅ Good | ✅ Excellent | ⚠️ Fair | ⚠️ Fair |
| **Markdown docs** | ⚠️ Fair | ✅ Good | ✅ Excellent | ⚠️ Fair | ⚠️ Fair |
| **Multi-file context** | ⚠️ Limited | ✅ Excellent | ✅ Good | ⚠️ Limited | ⚠️ Limited |
| **Local setup** | ✅ Easy | ✅ Easy | ⚠️ Varies | ✅ Easy | ✅ Easy |
| **Config file** | ✅ .copilotignore | ✅ .cursorrules | - | - | - |

---

## Additional Resources

- [architecture.md](./architecture.md) — System design and medallion pattern docs
- [ingestion.md](./ingestion.md) — Bronze layer ingestion strategy
- [transformation.md](./transformation.md) — Silver layer transformation patterns
- [modeling.md](./modeling.md) — Gold layer dimensional modeling
- [documentation_hygiene.md](./documentation_hygiene.md) — Writing standards for the project
- [../README.md](../README.md) — Project overview
- [.cursorrules](../../.cursorrules) — Cursor-specific project rules
- [.copilotignore](../../.copilotignore) — Copilot exclusions and scope
