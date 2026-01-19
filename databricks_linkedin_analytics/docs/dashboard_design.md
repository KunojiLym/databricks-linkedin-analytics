# Dashboard design and data product

Maps to the following post in [Build Your Own LinkedIn Analytics](https://www.yzouyang.com/category/blog-series/build-your-own-linkedin-analytics/): 
- [Part 7: Dashboard Design for Insights and Impact](https://www.yzouyang.com/build-your-own-linkedin-analytics-part-7-dashboard-design-for-insights-and-impact/) 

## Artifacts
- `src/linkedin_analytics_jobs/4. data product/LinkedIn Statistics.lvdash.json` — dashboard definition exported from the visualization tool
- `resources/dashboards.yml` — dashboard resource configuration for bundle deployment

## Design goals
- Surface trends (impressions, engagement rate) over time
- Provide post-level detail with filters for date range, post type, and engagements
- Include KPIs for follower growth and content performance

## How-to
- Import the `.lvdash.json` file into your Databricks dashboard or visualization tool
- Ensure the gold tables exist and permissions allow the dashboard's query engine to read them

## Examples
- Use `fct_daily_post_statistics` for per-post metrics and `fct_daily_profile_statistics` for profile-level KPIs
- Add pre-aggregated tiles for rolling 7-day averages to improve dashboard responsiveness

## Operational notes
- Dashboard refresh is in the job pipeline (`resources/jobs.yml`) after the gold pipeline completes.
