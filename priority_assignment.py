"""
Priority assignment module for job prioritization.
"""

import pandas as pd
from config import JOB_TYPE_PRIORITY, CANNOT_DO_PRIORITY, JOBS_FILE_COLUMNS


def assign_priorities(df):
    """
    Assign priorities to jobs based on job type, due date/time, and capability.
    
    Priority rules:
    1. Jobs that cannot be done internally get priority -1
    2. HAZARD > REPAIRS > SURVEY (job type priority)
    3. Within same job type: Earlier due date/time = Higher priority
    4. Same job type + same due date/time = Same priority
    
    Args:
        df (pd.DataFrame): Dataframe with jobs and capability information
        
    Returns:
        pd.DataFrame: Dataframe with assigned priorities
    """
    df_priority = df.copy()
    
    # Initialize priority column
    df_priority['Priority'] = 0
    
    # Separate jobs that cannot be done internally
    cannot_do_mask = ~df_priority['can_do_internally']
    can_do_mask = df_priority['can_do_internally']
    
    # Assign -1 priority to jobs that cannot be done
    df_priority.loc[cannot_do_mask, 'Priority'] = CANNOT_DO_PRIORITY
    
    # For jobs that can be done, assign priorities
    if can_do_mask.sum() > 0:
        df_can_do = df_priority[can_do_mask].copy()
        
        # Get job type column
        job_type_col = JOBS_FILE_COLUMNS['parent_job_type']
        
        # Map job types to priority values
        df_can_do['job_type_priority'] = df_can_do[job_type_col].map(JOB_TYPE_PRIORITY)
        
        # Sort by job type priority FIRST, then by due datetime
        # Keep the original index to map back later
        df_can_do = df_can_do.sort_values(
            by=['job_type_priority', 'due_datetime'],
            ascending=[True, True]
        )
        
        # Assign priorities based on datetime within job type
        priority_counter = 1
        prev_job_type = None
        prev_due_datetime = None
        
        priorities = []
        
        for idx, row in df_can_do.iterrows():
            current_job_type = row['job_type_priority']
            current_due_datetime = row['due_datetime']
            
            # Same priority only if BOTH job type AND datetime match
            if (current_job_type == prev_job_type and 
                current_due_datetime == prev_due_datetime):
                priorities.append(priority_counter)
            else:
                # Different - increment priority
                if prev_job_type is not None:
                    priority_counter += 1
                priorities.append(priority_counter)
            
            prev_job_type = current_job_type
            prev_due_datetime = current_due_datetime
        
        df_can_do['Priority'] = priorities
        
        # Update the main dataframe using the original indices
        df_priority.loc[df_can_do.index, 'Priority'] = df_can_do['Priority'].values
    
    return df_priority


def create_priority_summary(df):
    """
    Create a summary of priority assignments.
    
    Args:
        df (pd.DataFrame): Dataframe with assigned priorities
        
    Returns:
        pd.DataFrame: Summary dataframe
    """
    summary = df.groupby('Priority').agg({
        JOBS_FILE_COLUMNS['job_id']: 'count',
        JOBS_FILE_COLUMNS['parent_job_type']: lambda x: ', '.join(x.unique())
    }).reset_index()
    
    summary.columns = ['Priority', 'Job Count', 'Job Types']
    
    return summary.sort_values('Priority')