# Observability and Monitoring

Maps to: Blog Part 10 — Observing the Pipeline

## What to monitor
- Job run status and durations (success/failure rates)
- Row counts and data freshness for critical gold tables
- Error rates and exceptions in ingestion/transformation notebooks

## Where to capture metrics
- Databricks Job run history and run logs
- A monitoring table inside the `gold` catalog (e.g., `etl_monitoring.job_runs`)

## Recommended alerts
- Alert on job failures (immediate)
- Alert on data freshness lag (e.g., if today's partition is missing)
- Alert on sudden drops or spikes in row counts for key tables

## Debugging tips
- Re-run failed notebook tasks with the same parameters to reproduce
- Inspect job logs (driver/executor logs) for stack traces
- Query intermediate bronze/silver tables to check for data anomalies

## Example SQL checks
- Missing partition check: `SELECT date FROM <gold_table> WHERE date = current_date()`
- Row-count anomaly: compare recent daily counts to historical averages

## Reference
- `resources/jobs.yml` configures retry policies for some tasks; review them when tuning failures.
