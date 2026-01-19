# Transformation (Silver layer)

Maps to the following post in [Build Your Own LinkedIn Analytics](https://www.yzouyang.com/category/blog-series/build-your-own-linkedin-analytics/): 
- [Part 5: Cleaning and Transforming Data](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-5-cleaning-and-transforming-data/)

## Purpose
- Consolidate and standardize raw bronze tables into clean, analysis-ready silver tables: `impressions`, `engagements`, `posts`, `followers`, `totals`.

## Notebooks
- `src/linkedin_analytics_jobs/2. silver transformation/silver impressions consolidation.ipynb`
- `src/linkedin_analytics_jobs/2. silver transformation/silver engagements consolidation.ipynb`
- `src/linkedin_analytics_jobs/2. silver transformation/silver post enrichment.ipynb`
- `src/linkedin_analytics_jobs/2. silver transformation/silver metrics consolidation.ipynb`
- `src/linkedin_analytics_jobs/2. silver transformation/silver views update.ipynb`

## Key topics
- Schema enforcement and casting (dates, numeric types)
- Deduplication and late-arriving data handling
- Enrichment joins (e.g., join post metadata to metrics)
- Data quality checks: null thresholds, row count checks, value ranges

## Best practices
- Keep transformations idempotent and use transactional writes (Delta)
- Break large notebooks into smaller, testable functions or modules
- Surface DQ metrics into a monitoring table or logs

## Reference
- See `resources/schemas.yml` for canonical schema naming and `resources/variables.yml` for table names.
