CREATE MATERIALIZED VIEW IF NOT EXISTS ${GOLD_CATALOG}.${GOLD_SCHEMA}.${DIM_TIMESTAMP_TABLE} AS
SELECT
  timestamp,
  sg_timestamp,
  DATE(timestamp) AS utc_date,
  HOUR(timestamp) AS utc_hour,
  MINUTE(timestamp) AS utc_minute,
  DATE(sg_timestamp) AS sgt_date,
  HOUR(sg_timestamp) AS sgt_hour,
  MINUTE(sg_timestamp) AS sgt_minute
FROM (
  SELECT DISTINCT 
    post_publish_timestamp AS timestamp,
    from_utc_timestamp(
      post_publish_timestamp, 'Asia/Singapore'
    ) AS sg_timestamp
  FROM ${SILVER_CATALOG}.${SILVER_SCHEMA}.${SILVER_POSTS_TABLE}
  WHERE post_publish_timestamp IS NOT NULL
)
ORDER BY timestamp ASC