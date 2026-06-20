import re
from datetime import datetime
from typing import Optional


def _parse_same_dates(date_start: str, date_end: str) -> bool:
    try:
        d1 = datetime.strptime(date_start, '%Y-%m-%d')
        d2 = datetime.strptime(date_end, '%Y-%m-%d')
        return d1 == d2
    except ValueError:
        return False


class FilenameValidator:
    """Validates LinkedIn daily content export filenames (legacy and current formats)."""

    def __init__(self, filename: str):
        self.filename = filename
        self.detected_format: Optional[str] = None

    def is_valid_format(self) -> bool:
        # Current: AggregateAnalytics_{Profile With Spaces}_{date}_{date}.xlsx
        aggregate_pattern = (
            r'^AggregateAnalytics_(.+)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})\.xlsx$'
        )
        match = re.match(aggregate_pattern, self.filename)
        if match:
            date_start, date_end = match.group(2), match.group(3)
            if _parse_same_dates(date_start, date_end):
                self.detected_format = 'aggregate_analytics'
                return True

        # Legacy: Content_{date}_{date}_{ProfileNoSpaces}.xlsx
        content_pattern = (
            r'^Content_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_[a-zA-Z0-9_]+\.xlsx$'
        )
        match = re.match(content_pattern, self.filename)
        if match:
            date_start, date_end = match.group(1), match.group(2)
            if _parse_same_dates(date_start, date_end):
                self.detected_format = 'content'
                return True

        self.detected_format = None
        return False
