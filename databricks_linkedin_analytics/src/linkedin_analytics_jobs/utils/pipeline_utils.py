import re
from datetime import datetime
from typing import Optional, Tuple

from pyspark.sql import functions as F, DataFrame
from pyspark.sql.functions import col, sequence, explode, min as spark_min, max as spark_max

_FORBIDDEN_PATTERNS = [
    r'--', r';', r"'", r'\"', r'/\*', r'\*/', r'xp_', r'char\(', r'nchar\(', r'varchar\(',
    r'alter', r'drop', r'insert', r'delete', r'update', r'select',
    r'create', r'exec', r'union', r'or', r'and',
]


def remove_spaces(name: str) -> str:
    """Remove all spaces from profile name for legacy Content_/PostAnalytics_ filenames."""
    return name.replace(' ', '')


def ensure_spaces(name: str) -> str:
    """Ensure profile name has spaces for AggregateAnalytics_/SinglePostAnalytics_ filenames."""
    compact = remove_spaces(name.strip())
    if not compact:
        return name.strip()
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', compact)


def profile_name_variants(profile: str) -> Tuple[str, str]:
    """
    Return (spaced, compact) filename variants for a profile name.

    Accepts either 'Your Profile Name Here' or 'YourProfileNameHere' (or any equivalent spacing).
    """
    compact = remove_spaces(profile.strip())
    spaced = ensure_spaces(compact)
    return spaced, compact


def _check_forbidden_patterns(value: str, parameter_key: str) -> None:
    for pattern in _FORBIDDEN_PATTERNS:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValueError(
                f"Potentially dangerous value for {parameter_key}: {value} "
                f"(pattern matched: {pattern})"
            )


def get_valid_profile_name(value: str, parameter_key: str = "LINKEDIN_PROFILE_NAME") -> str:
    """
    Validate a LinkedIn profile display name for filename matching only (not SQL).

    Accepts either spaced or compact forms (e.g. 'Your Profile Name Here' or 'YourProfileNameHere').
    Returns the canonical spaced form used for new-format filenames.
    """
    if not value:
        raise ValueError(f"Empty value for {parameter_key}")
    if not re.fullmatch(r'[A-Za-z0-9 _.\-]+', value.strip()):
        raise ValueError(f"Invalid characters in {parameter_key}: {value}")
    _check_forbidden_patterns(value.strip(), parameter_key)
    spaced, _compact = profile_name_variants(value)
    return spaced


def _parse_iso_dates(date_start: str, date_end: str, require_same_dates: bool) -> bool:
    try:
        d1 = datetime.strptime(date_start, '%Y-%m-%d')
        d2 = datetime.strptime(date_end, '%Y-%m-%d')
    except ValueError:
        return False
    if require_same_dates and d1 != d2:
        return False
    return True


def match_content_filename(
    filename: str,
    profile: str,
    *,
    require_same_dates: bool = True,
) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    Match daily/historical content export filenames (newest format first).

    Returns (matched, date_start, date_end, format_name).
    format_name is 'aggregate_analytics' or 'content'.
    """
    spaced, compact = profile_name_variants(profile)
    spaced = re.escape(spaced)
    compact = re.escape(compact)

    aggregate_pattern = (
        rf'^AggregateAnalytics_{spaced}_(\d{{4}}-\d{{2}}-\d{{2}})_(\d{{4}}-\d{{2}}-\d{{2}})\.xlsx$'
    )
    match = re.match(aggregate_pattern, filename)
    if match:
        date_start, date_end = match.group(1), match.group(2)
        if _parse_iso_dates(date_start, date_end, require_same_dates):
            return True, date_start, date_end, 'aggregate_analytics'

    if require_same_dates:
        content_pattern = (
            rf'^Content_(\d{{4}}-\d{{2}}-\d{{2}})_\1_{compact}\.xlsx$'
        )
    else:
        content_pattern = (
            rf'^Content_(\d{{4}}-\d{{2}}-\d{{2}})_(\d{{4}}-\d{{2}}-\d{{2}})_{compact}\.xlsx$'
        )
    match = re.match(content_pattern, filename)
    if match:
        date_start = match.group(1)
        date_end = match.group(1) if require_same_dates else match.group(2)
        if _parse_iso_dates(date_start, date_end, require_same_dates):
            return True, date_start, date_end, 'content'

    return False, None, None, None


def match_post_filename(
    filename: str,
    profile: str,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Match per-post analytics filenames (newest format first).

    Returns (matched, post_id, format_name).
    format_name is 'single_post_analytics' or 'post_analytics'.
    """
    spaced, compact = profile_name_variants(profile)
    spaced = re.escape(spaced)
    compact = re.escape(compact)
    suffix = r'(?: \(\d+\))?'

    single_pattern = (
        rf'^SinglePostAnalytics_{spaced}_(\d+){suffix}\.xlsx$'
    )
    match = re.match(single_pattern, filename)
    if match:
        return True, match.group(1), 'single_post_analytics'

    legacy_pattern = rf'^PostAnalytics_{compact}_(\d+){suffix}\.xlsx$'
    match = re.match(legacy_pattern, filename)
    if match:
        return True, match.group(1), 'post_analytics'

    return False, None, None


def get_valid_parameter_value(parameter_value: str, parameter_key: str = "parameter") -> str:
    """
    Validates a parameter value to prevent SQL injection.
    Extracted from notebooks for unit testing.
    """
    if not parameter_value:
        raise ValueError(f"Empty value for {parameter_key}")

    # Parameter_value must be a string with only alphanumeric characters and underscores
    if not re.fullmatch(r'[a-zA-Z0-9_]+', parameter_value):
        raise ValueError(f"Invalid characters in {parameter_key}: {parameter_value}")
    
    _check_forbidden_patterns(parameter_value, parameter_key)
    return parameter_value

def fill_missing_dates(df: DataFrame, date_col: str, group_cols: list, value_col: str, spark=None) -> DataFrame:
    """
    Fills missing dates in a time-series DataFrame with 0 for the specified value column.
    """
    if spark is None:
        spark = df.sparkSession
    # Get min and max dates
    date_range = df.select(spark_min(date_col).alias("min_date"), spark_max(date_col).alias("max_date")).collect()[0]
    min_date, max_date = date_range.min_date, date_range.max_date

    if min_date is None or max_date is None:
        return df

    # Create full date sequence
    date_seq_df = spark.createDataFrame([(min_date, max_date)], ["start", "end"]) \
        .select(explode(sequence(col("start"), col("end"))).alias(date_col))

    # Cross join with unique group keys
    unique_keys_df = df.select(*group_cols).distinct()
    full_grid_df = unique_keys_df.crossJoin(date_seq_df)

    # Left join to original df
    filled_df = full_grid_df.join(
        df,
        on=group_cols + [date_col],
        how="left"
    ).fillna({value_col: 0})

    return filled_df
