import re
from datetime import datetime

class FilenameValidator:
    def __init__(self, filename: str):
        self.filename = filename

    def is_valid_format(self) -> bool:
        # Expected format: Content_YYYY-MM-DD_YYYY-MM-DD_ProfileName.xlsx
        # Using a slightly relaxed regex to allow for profile names with more characters
        pattern = r'^Content_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_[a-zA-Z0-9_]+\.xlsx$' # Added underscore to allowed chars
        match = re.match(pattern, self.filename)
        if not match:
            return False
            
        # Verify dates are valid
        try:
            date1 = datetime.strptime(match.group(1), '%Y-%m-%d')
            date2 = datetime.strptime(match.group(2), '%Y-%m-%d')
            return date1 == date2 # For now assuming dates must match as per existing ingestion logic
        except ValueError:
            return False
