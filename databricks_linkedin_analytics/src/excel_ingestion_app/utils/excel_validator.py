import pandas as pd
from typing import List, Tuple, Optional

def validate_excel_sheets(uploaded_file, required_sheets: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validates that the uploaded Excel file contains all required sheets.
    Returns (is_valid, error_message).
    """
    try:
        xl = pd.ExcelFile(uploaded_file)
        missing_sheets = [s for s in required_sheets if s not in xl.sheet_names]
        if missing_sheets:
            return False, f"Missing required sheets: {', '.join(missing_sheets)}"
        return True, None
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
