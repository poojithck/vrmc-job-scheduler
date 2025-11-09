"""
Filtering module for date-based job filtering.
"""

import pandas as pd
from datetime import datetime
from data_loader import parse_date
from config import JOBS_FILE_COLUMNS


def filter_jobs_by_date(df, reference_date):
    """
    Filter jobs based on due date.
    
    Args:
        df (pd.DataFrame): Jobs dataframe
        reference_date (str or datetime): Reference date for filtering
        
    Returns:
        pd.DataFrame: Filtered dataframe with jobs due on or after reference date
    """
    # Parse reference date if string
    if isinstance(reference_date, str):
        reference_date = parse_date(reference_date)
    
    # Create a copy to avoid modifying original
    df_filtered = df.copy()
    
    # Parse due dates
    due_col = JOBS_FILE_COLUMNS['due']
    df_filtered['due_datetime'] = df_filtered[due_col].apply(parse_date)
    
    # Filter jobs with due date >= reference date
    df_filtered = df_filtered[df_filtered['due_datetime'] >= reference_date]
    
    return df_filtered.reset_index(drop=True)
