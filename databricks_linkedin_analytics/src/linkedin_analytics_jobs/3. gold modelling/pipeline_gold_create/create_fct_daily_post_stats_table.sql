CREATE MATERIALIZED VIEW IF NOT EXISTS ${GOLD_CATALOG}.${GOLD_SCHEMA}.${FCT_DAILY_POST_STATS_TABLE} AS
SELECT
  t.date AS analytics_date,
  f.new_followers,
  t.impressions,
  t.engagements,
  coalesce(
    t.impressions - prev_t.impressions
  ) AS change_in_impressions,
  coalesce(
    t.engagements - prev_t.engagements
  ) AS change_in_engagements
FROM
  ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_TOTALS_TABLE} t
  LEFT JOIN ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_TOTALS_TABLE} prev_t
    ON prev_t.date = DATE_SUB(t.date, 1)
  LEFT JOIN ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_FOLLOWERS_TABLE} f
    ON f.date = t.date
ORDER BY t.date ASC;