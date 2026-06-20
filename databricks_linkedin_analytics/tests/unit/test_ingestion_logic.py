import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from excel_ingestion_app.utils.file_validation import FilenameValidator

def test_valid_filename():
    validator = FilenameValidator("Content_2023-10-27_2023-10-27_MyProfile.xlsx")
    assert validator.is_valid_format() == True

def test_valid_filename_with_underscore():
    validator = FilenameValidator("Content_2023-10-27_2023-10-27_My_Profile_1.xlsx")
    assert validator.is_valid_format() == True

def test_invalid_filename_format():
    validator = FilenameValidator("Invalid_Name.xlsx")
    assert validator.is_valid_format() == False

def test_invalid_date_format():
    validator = FilenameValidator("Content_2023-13-01_2023-13-01_MyProfile.xlsx")
    assert validator.is_valid_format() == False

def test_mismatched_dates():
    # Based on existing logic analysis, file usually has same from/to date
    validator = FilenameValidator("Content_2023-10-27_2023-10-28_MyProfile.xlsx")
    assert validator.is_valid_format() == False

def test_invalid_extension():
    validator = FilenameValidator("Content_2023-10-27_2023-10-27_MyProfile.csv")
    assert validator.is_valid_format() == False

def test_lowercase_prefix():
    # Regex is case sensitive: ^Content_...
    validator = FilenameValidator("content_2023-10-27_2023-10-27_MyProfile.xlsx")
    assert validator.is_valid_format() == False

def test_valid_aggregate_analytics_filename():
    validator = FilenameValidator("AggregateAnalytics_My Profile_2026-06-18_2026-06-18.xlsx")
    assert validator.is_valid_format() is True
    assert validator.detected_format == 'aggregate_analytics'

def test_aggregate_analytics_mismatched_dates():
    validator = FilenameValidator("AggregateAnalytics_My Profile_2026-06-18_2026-06-19.xlsx")
    assert validator.is_valid_format() is False

def test_unknown_prefix_invalid():
    validator = FilenameValidator("Unknown_2026-06-18_2026-06-18_MyProfile.xlsx")
    assert validator.is_valid_format() is False
