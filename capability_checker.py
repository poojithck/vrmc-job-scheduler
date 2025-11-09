"""
Capability checking module for internal capability validation.
"""

import pandas as pd
import re
from config import CAPABILITY_FILE_COLUMNS, JOBS_FILE_COLUMNS


def check_capability(capability_value):
    """
    Check capability and return flags.
    
    Args:
        capability_value: Capability value from the capability file
        
    Returns:
        dict: Dictionary with capability flags
    """
    result = {
        'can_do': True,
        'needs_check': False
    }
    
    # Handle None or NaN values
    if pd.isna(capability_value) or str(capability_value).strip().upper() == 'NONE':
        result['can_do'] = False
        return result
    
    # Check for comparison operators
    capability_str = str(capability_value)
    if '<' in capability_str or '>' in capability_str:
        result['needs_check'] = True
    
    return result


def merge_capability_data(jobs_df, capability_df):
    """
    Merge jobs dataframe with capability data.
    
    Args:
        jobs_df (pd.DataFrame): Jobs dataframe
        capability_df (pd.DataFrame): Capability dataframe
        
    Returns:
        pd.DataFrame: Merged dataframe with capability information
    """
    job_col = JOBS_FILE_COLUMNS['standard_job']
    cap_job_col = CAPABILITY_FILE_COLUMNS['job_code']
    cap_internal_col = CAPABILITY_FILE_COLUMNS['capability_internal']
    
    # Merge dataframes
    merged_df = jobs_df.merge(
        capability_df[[cap_job_col, cap_internal_col]],
        left_on=job_col,
        right_on=cap_job_col,
        how='left'
    )
    
    # Apply capability checks
    capability_checks = merged_df[cap_internal_col].apply(check_capability)
    
    merged_df['can_do_internally'] = capability_checks.apply(lambda x: x['can_do'])
    merged_df['needs_capability_check'] = capability_checks.apply(lambda x: x['needs_check'])
    
    return merged_df
