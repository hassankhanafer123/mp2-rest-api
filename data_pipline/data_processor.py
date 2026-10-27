import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    df_nodup = df.drop_duplicates()
    logger.debug("before removing duplicates: %d rows, after: %d rows, removed: %d rows",
                 len(df), len(df_nodup), len(df) - len(df_nodup))
    return df_nodup


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        df_clean = df.dropna(axis=0)
        logger.debug("before handling missing values: %d rows, after: %d rows, removed: %d rows",
                     len(df), len(df_clean), len(df) - len(df_clean))
    elif axis == "columns":
        df_clean = df.dropna(axis=1)
        logger.debug("before handling missing values: %d columns, after: %d columns, removed: %d columns",
                     df.shape[1], df_clean.shape[1], df.shape[1] - df_clean.shape[1])
    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")

    return df_clean


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["zscore", "iqr"]:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column '%s' not found, skipping", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column '%s' is not numeric, skipping", col)
            continue
        rows_before = len(df)  
        if method == "zscore":
            mean = df[col].mean()
            std = df[col].std()
            if std != 0:
                df = df[(df[col] - mean).abs() <= threshold * std]
        elif method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[col] >= Q1 - threshold * IQR) & (df[col] <= Q3 + threshold * IQR)]
        rows_after = len(df)
        logger.debug("Column '%s' (method=%s, threshold=%s): removed %d rows",
                     col, method, threshold, rows_before - rows_after)
    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]
    if processing["remove_duplicates"]:
        df = remove_duplicates(df)
    missing = processing["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])
    outliers = processing["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(df,
                             outliers["columns"],
                             outliers["method"],
                             outliers["threshold"])

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before":     len(df_before),
        "rows_after":      len(df_after),
        "rows_removed":    len(df_before) - len(df_after),
        "columns_before":  df_before.shape[1],
        "columns_after":   df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }