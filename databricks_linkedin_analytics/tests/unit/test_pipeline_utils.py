import pytest
import sys
import os
from pyspark.sql import SparkSession
from datetime import date

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from linkedin_analytics_jobs.utils.pipeline_utils import get_valid_parameter_value, fill_missing_dates

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
