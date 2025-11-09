"""
Example usage script demonstrating different ways to use the priority assignment system.
"""

from main import process_job_priorities
from data_loader import load_jobs_data
from config import JOBS_FILE_COLUMNS


def example_basic_usage():
    """
    Example 1: Basic usage with default settings.
    """
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    result_df = process_job_priorities(
        jobs_file_path='jobs_data.csv',
        capability_file_path='RM Codes Crew Capability.xlsx',
        reference_date='10/10/2024',
        output_path='output_basic.xlsx'
    )
    
    return result_df


def example_csv_output():
    """
    Example 2: Output to CSV instead of Excel.
    """
    print("\n" + "="*60)
    print("Example 2: CSV Output")
    print("="*60)
    
    result_df = process_job_priorities(
        jobs_file_path='jobs_data.xlsx',
        capability_file_path='RM Codes Crew Capability.xlsx',
        reference_date='15/11/2024',
        output_path='output_results.csv'
    )
    
    return result_df


def example_filter_by_priority():
    """
    Example 3: Get only high-priority jobs (priority 1-10).
    """
    print("\n" + "="*60)
    print("Example 3: Filter High Priority Jobs")
    print("="*60)
    
    result_df = process_job_priorities(
        jobs_file_path='jobs_data.csv',
        capability_file_path='RM Codes Crew Capability.xlsx',
        reference_date='10/10/2024',
        output_path='high_priority_jobs.xlsx'
    )
    
    # Filter to only high priority jobs
    high_priority = result_df[
        (result_df['Priority'] > 0) & 
        (result_df['Priority'] <= 10)
    ]
    
    print(f"\nFound {len(high_priority)} high-priority jobs")
    print(high_priority[['Priority', 'JobID', 'Parent Job Type', 'Due']].to_string(index=False))
    
    return high_priority


def example_jobs_by_type():
    """
    Example 4: Analyze jobs by type.
    """
    print("\n" + "="*60)
    print("Example 4: Jobs by Type Analysis")
    print("="*60)
    
    result_df = process_job_priorities(
        jobs_file_path='jobs_data.csv',
        capability_file_path='RM Codes Crew Capability.xlsx',
        reference_date='10/10/2024',
        output_path='output_analysis.xlsx'
    )
    
    # Analyze by job type
    job_type_col = JOBS_FILE_COLUMNS['parent_job_type']
    
    for job_type in ['HAZARD', 'REPAIRS', 'SURVEY']:
        type_jobs = result_df[result_df[job_type_col] == job_type]
        can_do = type_jobs['can_do_internally'].sum()
        print(f"\n{job_type}:")
        print(f"  Total: {len(type_jobs)}")
        print(f"  Can Do: {can_do}")
        print(f"  Cannot Do: {len(type_jobs) - can_do}")
        print(f"  Need Check: {type_jobs['needs_capability_check'].sum()}")


def example_flagged_jobs():
    """
    Example 5: Extract jobs requiring attention.
    """
    print("\n" + "="*60)
    print("Example 5: Jobs Requiring Attention")
    print("="*60)
    
    result_df = process_job_priorities(
        jobs_file_path='jobs_data.csv',
        capability_file_path='RM Codes Crew Capability.xlsx',
        reference_date='10/10/2024',
        output_path='output_flagged.xlsx'
    )
    
    # Jobs we cannot do
    cannot_do = result_df[result_df['Cannot_Do_Flag'] == True]
    print(f"\nJobs we cannot do internally: {len(cannot_do)}")
    if len(cannot_do) > 0:
        print(cannot_do[['JobID', 'Standard Job', 'Parent Job Type']].head().to_string(index=False))
    
    # Jobs needing capability check
    needs_check = result_df[result_df['Capability_Check_Flag'] == True]
    print(f"\nJobs needing capability check: {len(needs_check)}")
    if len(needs_check) > 0:
        print(needs_check[['JobID', 'Standard Job', 'Parent Job Type']].head().to_string(index=False))


def main():
    """
    Run examples based on available data.
    """
    print("\nJob Priority Assignment System - Examples")
    print("="*60)
    print("\nNote: Modify file paths in each example function to match your data.")
    print("\nAvailable examples:")
    print("1. Basic usage")
    print("2. CSV output")
    print("3. Filter high-priority jobs")
    print("4. Analyze jobs by type")
    print("5. Extract flagged jobs")
    print("\nUncomment the desired example in the main() function to run it.")
    
    # Uncomment the example you want to run:
    # example_basic_usage()
    # example_csv_output()
    # example_filter_by_priority()
    # example_jobs_by_type()
    # example_flagged_jobs()


if __name__ == "__main__":
    main()
