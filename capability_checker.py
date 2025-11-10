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
    if pd.isna(capability_value) or str(capability_value).strip().upper() == 'No Crew':
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
    speed_zone_col = JOBS_FILE_COLUMNS.get('speed_zone', 'SpeedZone')
    
    # Merge dataframes - include speed zone column
    merged_df = jobs_df.merge(
        capability_df[[cap_job_col, cap_internal_col]],
        left_on=job_col,
        right_on=cap_job_col,
        how='left'
    )
    
    # Apply capability checks
    print(f"      Columns: {list(capability_df.columns)}")
    capability_checks = merged_df[cap_internal_col].apply(check_capability)
    
    merged_df['can_do_internally'] = capability_checks.apply(lambda x: x['can_do'])
    merged_df['needs_capability_check'] = capability_checks.apply(lambda x: x['needs_check'])
    
    # Add speed zone flag
    merged_df['high_speed_zone'] = check_speed_zone(merged_df[speed_zone_col])
    
    return merged_df


def check_speed_zone(speed_zone_series):
    """
    Check if speed zone is greater than 80.
    
    Args:
        speed_zone_series (pd.Series): Series of speed zone values
        
    Returns:
        pd.Series: Boolean series indicating if speed zone > 80
    """
    def is_high_speed(speed_value):
        # Handle None or NaN values
        if pd.isna(speed_value):
            return False
        
        try:
            # Convert to float and check if > 80
            speed = float(speed_value)
            return speed > 80
        except (ValueError, TypeError):
            # If conversion fails, return False
            return False
    
    return speed_zone_series.apply(is_high_speed)