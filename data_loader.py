"""
Data loading module for reading job and capability data.
"""

import pandas as pd
from datetime import datetime
from config import DATE_FORMAT, JOBS_FILE_COLUMNS, CAPABILITY_FILE_COLUMNS


def load_jobs_data(file_path):
    """
    Load jobs data from CSV or Excel file.
    
    Args:
        file_path (str): Path to the jobs data file
        
    Returns:
        pd.DataFrame: Jobs dataframe
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Validate required columns
    required_columns = list(JOBS_FILE_COLUMNS.values())
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return df


def load_capability_data(file_path, sheet_name='Sheet1 (2)'):
    """
    Load capability data from Excel file.
    
    Args:
        file_path (str): Path to the capability Excel file
        sheet_name (str): Name of the sheet to read
        
    Returns:
        pd.DataFrame: Capability dataframe
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Validate required columns
    required_columns = list(CAPABILITY_FILE_COLUMNS.values())
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns in capability file: {missing_columns}")
    
    return df


def parse_date(date_string):
    """
    Parse date string to datetime object.
    
    Args:
        date_string (str): Date string in format dd/mm/yyyy hh:mm:ss AM/PM
        
    Returns:
        datetime: Parsed datetime object
    """
    date_formats = [
        '%d/%m/%Y %I:%M:%S %p',  # 01/07/2024 11:26:45 AM
        '%d/%m/%Y %I:%M %p',      # 01/07/2024 11:26 AM
        '%d/%m/%y %I:%M:%S %p',  # 01/07/24 11:26:45 AM
        '%d/%m/%y %I:%M %p',      # 01/07/24 11:26 AM (your format)
        '%d/%m/%Y',               # 01/07/2024
        '%d/%m/%y',               # 01/07/24
        '%Y-%m-%d %H:%M:%S',      # 2024-07-01 11:26:45
        '%Y-%m-%d %H:%M',         # 2024-07-01 11:26
        '%Y-%m-%d',               # 2024-07-01
    ]
    
    date_string = date_string.strip()
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # If none of the formats work, raise an error with helpful message
    raise ValueError(
        f"Unable to parse date '{date_string}'. "
        f"Supported formats include: dd/mm/yyyy, dd/mm/yy, with optional time (HH:MM AM/PM)"
    )