import pytest
import sys
import os

# Ensure src module is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/excel_ingestion_app/utils')))

from file_validation import FilenameValidator

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
