"""
Main execution module for job priority assignment system.
"""

import pandas as pd
from datetime import datetime

from data_loader import load_jobs_data, load_capability_data
from filter import filter_jobs_by_date
from capability_checker import merge_capability_data
from priority_assignment import assign_priorities, create_priority_summary
from output_handler import prepare_output, save_to_excel, save_to_csv


def process_job_priorities(
    jobs_file_path,
    capability_file_path,
    reference_date,
    output_path='prioritized_jobs.xlsx',
    capability_sheet_name='Sheet1 (2)'
):
    """
    Main function to process job priorities.
    
    Priority Rules:
    1. Jobs that cannot be done internally: Priority -1
    2. Job type priority: HAZARD > REPAIRS > SURVEY
    3. Within same job type: Earlier due date/time = Higher priority
    4. Same priority: Only when job type, date, AND time are identical
    
    Args:
        jobs_file_path (str): Path to jobs data file
        capability_file_path (str): Path to capability Excel file
        reference_date (str or datetime): Reference date for filtering
        output_path (str): Path for output file
        capability_sheet_name (str): Sheet name in capability file
        
    Returns:
        pd.DataFrame: Processed dataframe with priorities
    """
    print("="*60)
    print("Job Priority Assignment System")
    print("="*60)
    
    # Step 1: Load data
    print("\n[1/5] Loading jobs data...")
    jobs_df = load_jobs_data(jobs_file_path)
    print(f"      Loaded {len(jobs_df)} jobs")
    
    print("\n[2/5] Loading capability data...")
    capability_df = load_capability_data(capability_file_path, capability_sheet_name)
    print(f"      Loaded {len(capability_df)} capability records")
    
    # Step 2: Filter by date
    print(f"\n[3/5] Filtering jobs by reference date: {reference_date}")
    filtered_df = filter_jobs_by_date(jobs_df, reference_date)
    print(f"      Filtered to {len(filtered_df)} jobs")
    
    # Step 3: Merge with capability data
    print("\n[4/5] Checking capability data...")
    merged_df = merge_capability_data(filtered_df, capability_df)
    
    cannot_do_count = (~merged_df['can_do_internally']).sum()
    needs_check_count = merged_df['needs_capability_check'].sum()
    print(f"      Jobs we cannot do: {cannot_do_count}")
    print(f"      Jobs needing capability check: {needs_check_count}")
    
    # Step 4: Assign priorities
    print("\n[5/5] Assigning priorities...")
    prioritized_df = assign_priorities(merged_df)
    
    # Create summary
    summary = create_priority_summary(prioritized_df)
    print("\n      Priority Summary:")
    print(summary.to_string(index=False))
    
    # Step 5: Prepare output
    print("\n[6/6] Preparing output...")
    output_df = prepare_output(prioritized_df)
    
    # Save output
    if output_path.endswith('.csv'):
        save_to_csv(output_df, output_path)
    else:
        save_to_excel(output_df, output_path)
    
    print("\n" + "="*60)
    print("Processing Complete!")
    print("="*60)
    
    return output_df


def main():
    """
    Main entry point with example usage.
    """
    # Example configuration
    JOBS_FILE = 'export.csv'  # or 'jobs_data.xlsx'
    CAPABILITY_FILE = 'RM Codes Crew Capability.xlsx'
    REFERENCE_DATE = '06/11/2025'  # Format: dd/mm/yyyy
    OUTPUT_FILE = 'prioritized_jobs_output.xlsx'
    
    try:
        result_df = process_job_priorities(
            jobs_file_path=JOBS_FILE,
            capability_file_path=CAPABILITY_FILE,
            reference_date=REFERENCE_DATE,
            output_path=OUTPUT_FILE
        )
        
        # Display top 10 priority jobs
        print("\nTop 10 Priority Jobs:")
        display_cols = ['Priority', 'JobID', 'Parent Job Type', 'Due', 
                       'Cannot_Do_Flag', 'Capability_Check_Flag']
        existing_display_cols = [col for col in display_cols if col in result_df.columns]
        print(result_df[existing_display_cols].head(10).to_string(index=False))
        
    except FileNotFoundError as e:
        print(f"\nError: File not found - {e}")
        print("Please ensure the input files exist in the current directory.")
    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise


if __name__ == "__main__":
    main()