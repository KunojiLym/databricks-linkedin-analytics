import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from excel_ingestion_app.utils.excel_validator import validate_excel_sheets

def test_validate_excel_sheets_success():
    mock_file = MagicMock()
    with patch('pandas.ExcelFile') as mock_excel:
        mock_instance = mock_excel.return_value
        mock_instance.sheet_names = ["DISCOVERY", "ENGAGEMENT", "FOLLOWERS", "TOP POSTS", "OTHER"]
        
        is_valid, error = validate_excel_sheets(mock_file, ["DISCOVERY", "ENGAGEMENT", "FOLLOWERS", "TOP POSTS"])
        
        assert is_valid is True
        assert error is None

def test_validate_excel_sheets_missing():
    mock_file = MagicMock()
    with patch('pandas.ExcelFile') as mock_excel:
        mock_instance = mock_excel.return_value
        mock_instance.sheet_names = ["DISCOVERY", "ENGAGEMENT"]
        
        is_valid, error = validate_excel_sheets(mock_file, ["DISCOVERY", "ENGAGEMENT", "FOLLOWERS", "TOP POSTS"])
        
        assert is_valid is False
        assert "Missing required sheets: FOLLOWERS, TOP POSTS" in error

def test_validate_excel_sheets_error():
    mock_file = MagicMock()
    with patch('pandas.ExcelFile', side_effect=Exception("Corrupt file")):
        is_valid, error = validate_excel_sheets(mock_file, ["DISCOVERY"])
        
        assert is_valid is False
        assert "Error reading file: Corrupt file" in error
