"""
Output module for exporting prioritized jobs data.
"""

import pandas as pd
from config import JOBS_FILE_COLUMNS


def prepare_output(df):
    """
    Prepare final output dataframe with relevant columns.
    
    Args:
        df (pd.DataFrame): Processed dataframe
        
    Returns:
        pd.DataFrame: Clean output dataframe
    """
    output_cols = [
        'Priority',
        JOBS_FILE_COLUMNS['job_id'],
        JOBS_FILE_COLUMNS['parent_job_type'],
        JOBS_FILE_COLUMNS['standard_job'],
        JOBS_FILE_COLUMNS['location'],
        JOBS_FILE_COLUMNS['due'],
        'Area',
        'can_do_internally',
        'needs_capability_check',
        'high_speed_zone',
        'LGA'
    ]
    
    # Filter to only existing columns
    existing_cols = [col for col in output_cols if col in df.columns]
    
    output_df = df[existing_cols].copy()
    
    # Add flag columns with descriptive names
    output_df['Cannot_Do_Flag'] = ~output_df['can_do_internally']
    output_df['Capability_Check_Flag'] = output_df['needs_capability_check']
    
    # Add high speed zone flag if column exists
    if 'high_speed_zone' in output_df.columns:
        output_df['High_Speed_Zone_Flag'] = output_df['high_speed_zone']
    
    # Sort by priority (excluding -1, which goes to end)
    df_priority_minus_one = output_df[output_df['Priority'] == -1]
    df_priority_others = output_df[output_df['Priority'] != -1]
    
    df_priority_others = df_priority_others.sort_values('Priority')
    
    output_df = pd.concat([df_priority_others, df_priority_minus_one], ignore_index=True)
    
    return output_df


def save_to_excel(df, output_path, include_summary=True):
    """
    Save dataframe to Excel file.
    
    Args:
        df (pd.DataFrame): Dataframe to save
        output_path (str): Output file path
        include_summary (bool): Whether to include summary sheet
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write main data
        df.to_excel(writer, sheet_name='Prioritized Jobs', index=False)
        
        # Write summary if requested
        if include_summary:
            summary = create_summary_statistics(df)
            summary.to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"Output saved to: {output_path}")


def save_to_csv(df, output_path):
    """
    Save dataframe to CSV file.
    
    Args:
        df (pd.DataFrame): Dataframe to save
        output_path (str): Output file path
    """
    df.to_csv(output_path, index=False)
    print(f"Output saved to: {output_path}")


def create_summary_statistics(df):
    """
    Create summary statistics for the output.
    
    Args:
        df (pd.DataFrame): Processed dataframe
        
    Returns:
        pd.DataFrame: Summary statistics
    """
    metrics = [
        'Total Jobs',
        'Jobs We Can Do',
        'Jobs We Cannot Do',
        'Jobs Needing Capability Check',
        'High Speed Zone Jobs (>80)',
        'HAZARD Jobs',
        'REPAIRS Jobs',
        'SURVEY Jobs'
    ]
    
    counts = [
        len(df),
        df['can_do_internally'].sum(),
        (~df['can_do_internally']).sum(),
        df['needs_capability_check'].sum(),
        df['high_speed_zone'].sum() if 'high_speed_zone' in df.columns else 0,
        (df[JOBS_FILE_COLUMNS['parent_job_type']] == 'HAZARD').sum(),
        (df[JOBS_FILE_COLUMNS['parent_job_type']] == 'REPAIRS').sum(),
        (df[JOBS_FILE_COLUMNS['parent_job_type']] == 'SURVEY').sum()
    ]
    
    summary_data = {
        'Metric': metrics,
        'Count': counts
    }
    
    return pd.DataFrame(summary_data)