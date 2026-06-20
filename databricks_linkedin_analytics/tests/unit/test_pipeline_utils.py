import pytest
import sys
import os
from pyspark.sql import SparkSession
from datetime import date

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from linkedin_analytics_jobs.utils.pipeline_utils import (
    get_valid_parameter_value,
    fill_missing_dates,
    remove_spaces,
    ensure_spaces,
    get_valid_profile_name,
    match_content_filename,
    match_post_filename,
    profile_name_variants,
)

from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_spark():
    return MagicMock()

def test_get_valid_parameter_value_success():
    assert get_valid_parameter_value("valid_table_name") == "valid_table_name"
    assert get_valid_parameter_value("gold") == "gold"

def test_get_valid_parameter_value_forbidden_patterns():
    # The character check happens FIRST, so these must have valid characters [a-zA-Z0-9_]
    # to trigger the forbidden keyword check.
    with pytest.raises(ValueError, match="Potentially dangerous value"):
        get_valid_parameter_value("drop_table") # 'drop' is forbidden
    
    with pytest.raises(ValueError, match="Potentially dangerous value"):
        get_valid_parameter_value("select_all") # 'select' is forbidden

def test_get_valid_parameter_value_invalid_chars():
    with pytest.raises(ValueError, match="Invalid characters"):
        get_valid_parameter_value("table; drop") # semicolon and space are invalid
    
    with pytest.raises(ValueError, match="Invalid characters"):
        get_valid_parameter_value("table-name") # hyphen not allowed

def test_fill_missing_dates(mock_spark):
    mock_df = MagicMock()
    # Mock date_range collect
    mock_date_range = MagicMock()
    mock_date_range.min_date = date(2023, 1, 1)
    mock_date_range.max_date = date(2023, 1, 3)
    mock_df.select.return_value.collect.return_value = [mock_date_range]
    
    # Mock sequence/explode part
    mock_date_seq_df = MagicMock()
    mock_spark.createDataFrame.return_value.select.return_value = mock_date_seq_df
    
    # Mock unique keys
    mock_unique_keys_df = MagicMock()
    mock_df.select.return_value.distinct.return_value = mock_unique_keys_df
    
    # Mock join/fillna
    mock_filled_df = MagicMock()
    mock_unique_keys_df.crossJoin.return_value.join.return_value.fillna.return_value = mock_filled_df
    
    from linkedin_analytics_jobs.utils.pipeline_utils import fill_missing_dates
    result = fill_missing_dates(mock_df, "analytics_date", ["post_url"], "impressions", spark=mock_spark)
    
    assert result == mock_filled_df
    mock_unique_keys_df.crossJoin.assert_called_once_with(mock_date_seq_df)
    mock_unique_keys_df.crossJoin.return_value.join.assert_called()

def test_remove_spaces():
    assert remove_spaces("Your Profile Name Here") == "YourProfileNameHere"

def test_ensure_spaces():
    assert ensure_spaces("YourProfileNameHere") == "Your Profile Name Here"
    assert ensure_spaces("Your Profile Name Here") == "Your Profile Name Here"

def test_get_valid_profile_name_accepts_spaces():
    assert get_valid_profile_name("Your Profile Name Here") == "Your Profile Name Here"

def test_get_valid_profile_name_accepts_compact():
    assert get_valid_profile_name("YourProfileNameHere") == "Your Profile Name Here"

def test_profile_name_variants_equivalent():
    spaced, compact = profile_name_variants("Your Profile Name Here")
    assert spaced == "Your Profile Name Here"
    assert compact == "YourProfileNameHere"
    assert profile_name_variants("YourProfileNameHere") == (spaced, compact)

def test_get_valid_profile_name_rejects_semicolon():
    with pytest.raises(ValueError, match="Invalid characters"):
        get_valid_profile_name("bad;name")

def test_match_content_filename_daily_aggregate():
    matched, d1, d2, fmt = match_content_filename(
        "AggregateAnalytics_Your Profile Name Here_2026-06-18_2026-06-18.xlsx",
        "Your Profile Name Here",
        require_same_dates=True,
    )
    assert matched is True
    assert d1 == "2026-06-18"
    assert d2 == "2026-06-18"
    assert fmt == "aggregate_analytics"

def test_match_content_filename_daily_legacy():
    matched, d1, d2, fmt = match_content_filename(
        "Content_2025-08-01_2025-08-01_YourProfileNameHere.xlsx",
        "Your Profile Name Here",
        require_same_dates=True,
    )
    assert matched is True
    assert fmt == "content"

def test_match_content_filename_historical_different_dates():
    matched, d1, d2, fmt = match_content_filename(
        "Content_2024-08-17_2025-08-16_YourProfileNameHere.xlsx",
        "Your Profile Name Here",
        require_same_dates=False,
    )
    assert matched is True
    assert d1 == "2024-08-17"
    assert d2 == "2025-08-16"

def test_match_post_filename_single_post():
    matched, post_id, fmt = match_post_filename(
        "SinglePostAnalytics_Your Profile Name Here_7472468010083958784.xlsx",
        "Your Profile Name Here",
    )
    assert matched is True
    assert post_id == "7472468010083958784"
    assert fmt == "single_post_analytics"

def test_match_content_filename_daily_aggregate_compact_profile():
    matched, d1, d2, fmt = match_content_filename(
        "AggregateAnalytics_Your Profile Name Here_2026-06-18_2026-06-18.xlsx",
        "YourProfileNameHere",
        require_same_dates=True,
    )
    assert matched is True
    assert fmt == "aggregate_analytics"

def test_match_content_filename_daily_legacy_compact_profile():
    matched, _, _, fmt = match_content_filename(
        "Content_2025-08-01_2025-08-01_YourProfileNameHere.xlsx",
        "YourProfileNameHere",
        require_same_dates=True,
    )
    assert matched is True
    assert fmt == "content"

def test_match_post_filename_single_post_compact_profile():
    matched, post_id, fmt = match_post_filename(
        "SinglePostAnalytics_Your Profile Name Here_7472468010083958784.xlsx",
        "YourProfileNameHere",
    )
    assert matched is True
    assert post_id == "7472468010083958784"
    assert fmt == "single_post_analytics"

def test_match_post_filename_legacy_with_suffix():
    matched, post_id, fmt = match_post_filename(
        "PostAnalytics_YourProfileNameHere_7372453867575283712 (1).xlsx",
        "Your Profile Name Here",
    )
    assert matched is True
    assert post_id == "7372453867575283712"
    assert fmt == "post_analytics"
