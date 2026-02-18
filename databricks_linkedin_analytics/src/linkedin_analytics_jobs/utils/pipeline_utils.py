import re
from pyspark.sql import functions as F, DataFrame
from pyspark.sql.functions import col, sequence, explode, min as spark_min, max as spark_max

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
    
    # Disallow dangerous SQL keywords and patterns
    forbidden_patterns = [
        r'--', r';', r"'", r'\"', r'/\*', r'\*/', r'xp_', r'char\(', r'nchar\(', r'varchar\(', 
        r'alter', r'drop', r'insert', r'delete', r'update', r'select', 
        r'create', r'exec', r'union', r'or', r'and'
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, parameter_value, re.IGNORECASE):
            raise ValueError(f"Potentially dangerous value for {parameter_key}: {parameter_value} (pattern matched: {pattern})")
    
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
