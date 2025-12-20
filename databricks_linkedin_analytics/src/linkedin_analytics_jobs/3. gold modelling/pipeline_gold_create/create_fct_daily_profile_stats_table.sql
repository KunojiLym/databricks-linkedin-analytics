CREATE MATERIALIZED VIEW IF NOT EXISTS ${GOLD_CATALOG}.${GOLD_SCHEMA}.${FCT_DAILY_PROFILE_STATS_TABLE} AS 

-- 1: select daily stats for individual posts
SELECT
  concat(
    i.post_publish_date, 
    ": ", 
    regexp_extract(p.link, r'.*_(.*)-activity.*')
  ) AS post_id,
  i.post_publish_date,
  p.post_publish_timestamp,
  impressions,
  coalesce(engagements, 0) as engagements,
  i.analytics_date,
  DATEDIFF(i.analytics_date, i.post_publish_date) AS days_since_post,
  coalesce(impressions - LAG(impressions, 1) OVER (
    PARTITION BY i.post_url ORDER BY i.analytics_date
  )) AS change_in_impressions,
  coalesce(engagements - LAG(engagements, 1) OVER (
    PARTITION BY i.post_url ORDER BY i.analytics_date
  )) AS change_in_engagements,
  p.title,
  p.content
FROM
  ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_IMPRESSIONS_TABLE} i
  LEFT JOIN ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_ENGAGEMENTS_TABLE} e
    ON i.post_url = e.post_url
    AND i.analytics_date = e.analytics_date
  LEFT JOIN silver.linkedin.posts p
    ON i.post_url = p.post_url
WHERE i.post_url != "others"

UNION ALL

-- 2: select daily stats for posts outside of top 50 for the day
SELECT
  "others" AS post_id,
  NULL AS post_publish_date,
  NULL AS post_publish_timestamp,
  impressions,
  coalesce(engagements, 0) AS engagements,
  i.analytics_date,
  NULL AS days_since_post,
  NULL AS change_in_impressions,
  NULL AS change_in_engagements,
  NULL AS title,
  NULL AS content  
FROM 
  (
    SELECT
      impressions,
      analytics_date
    FROM
      ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_IMPRESSIONS_TABLE}
    WHERE post_url = "others"
  ) i 
  LEFT JOIN (
    SELECT
      engagements,
      analytics_date
    FROM
      ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_ENGAGEMENTS_TABLE}
    WHERE post_url = "others"
  ) e
  ON i.analytics_date = e.analytics_date
  
UNION ALL

-- 3: select total stats
SELECT
  "total" AS post_id,
  NULL AS post_publish_date,
  NULL AS post_publish_timestamp,
  t.impressions,
  t.engagements,
  t.date AS analytics_date,
  NULL AS days_since_post,
  coalesce(
    t.impressions - prev_t.impressions
  ) AS change_in_impressions,
  coalesce(
    t.engagements - prev_t.engagements
  ) AS change_in_engagements,
  NULL AS title,
  NULL AS content
FROM
  ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_TOTALS_TABLE} t
  LEFT JOIN ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_TOTALS_TABLE} prev_t
    ON prev_t.date = DATE_SUB(t.date, 1)
;