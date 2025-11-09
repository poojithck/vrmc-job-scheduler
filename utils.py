"""
Utility script for quick operations and testing.
"""

import pandas as pd
from datetime import datetime
from data_loader import parse_date
from config import JOBS_FILE_COLUMNS, CAPABILITY_FILE_COLUMNS


def validate_jobs_file(file_path):
    """
    Validate jobs file format and contents.
    
    Args:
        file_path (str): Path to jobs file
    """
    print(f"\nValidating jobs file: {file_path}")
    print("-" * 60)
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        print(f"Total rows: {len(df)}")
        print(f"\nColumns found: {list(df.columns)}")
        
        # Check required columns
        required_cols = list(JOBS_FILE_COLUMNS.values())
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\nMISSING REQUIRED COLUMNS: {missing_cols}")
        else:
            print("\nAll required columns present")
        
        # Check job types
        if JOBS_FILE_COLUMNS['parent_job_type'] in df.columns:
            job_types = df[JOBS_FILE_COLUMNS['parent_job_type']].unique()
            print(f"\nJob types found: {job_types}")
        
        # Check date format
        if JOBS_FILE_COLUMNS['due'] in df.columns:
            print("\nChecking date format (first 5 entries):")
            for idx, date_val in enumerate(df[JOBS_FILE_COLUMNS['due']].head()):
                try:
                    parsed = parse_date(str(date_val))
                    print(f"  {idx+1}. {date_val} -> OK")
                except Exception as e:
                    print(f"  {idx+1}. {date_val} -> ERROR: {e}")
        
        # Check for nulls
        print("\nNull values per column:")
        null_counts = df.isnull().sum()
        for col, count in null_counts[null_counts > 0].items():
            print(f"  {col}: {count}")
        
        print("\nValidation complete")
        
    except Exception as e:
        print(f"ERROR: {e}")


def validate_capability_file(file_path, sheet_name='Sheet1 (2)'):
    """
    Validate capability file format and contents.
    
    Args:
        file_path (str): Path to capability file
        sheet_name (str): Sheet name to read
    """
    print(f"\nValidating capability file: {file_path}")
    print(f"Sheet: {sheet_name}")
    print("-" * 60)
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        print(f"Total rows: {len(df)}")
        print(f"\nColumns found: {list(df.columns)}")
        
        # Check required columns
        required_cols = list(CAPABILITY_FILE_COLUMNS.values())
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\nMISSING REQUIRED COLUMNS: {missing_cols}")
        else:
            print("\nAll required columns present")
        
        # Check capability values
        if CAPABILITY_FILE_COLUMNS['capability_internal'] in df.columns:
            cap_col = CAPABILITY_FILE_COLUMNS['capability_internal']
            
            none_count = df[cap_col].isna().sum()
            has_comparison = df[cap_col].astype(str).str.contains('<|>', na=False).sum()
            
            print(f"\nCapability analysis:")
            print(f"  None/NaN values: {none_count}")
            print(f"  Contains < or >: {has_comparison}")
            
            print(f"\nSample capability values:")
            for val in df[cap_col].dropna().head(10):
                print(f"  - {val}")
        
        print("\nValidation complete")
        
    except Exception as e:
        print(f"ERROR: {e}")


def preview_data(jobs_file, capability_file, n_rows=5):
    """
    Preview data from both files.
    
    Args:
        jobs_file (str): Path to jobs file
        capability_file (str): Path to capability file
        n_rows (int): Number of rows to preview
    """
    print("\n" + "="*60)
    print("Data Preview")
    print("="*60)
    
    # Preview jobs
    print(f"\nJobs File (first {n_rows} rows):")
    print("-" * 60)
    try:
        if jobs_file.endswith('.csv'):
            df_jobs = pd.read_csv(jobs_file)
        else:
            df_jobs = pd.read_excel(jobs_file)
        print(df_jobs.head(n_rows))
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Preview capability
    print(f"\nCapability File (first {n_rows} rows):")
    print("-" * 60)
    try:
        df_cap = pd.read_excel(capability_file, sheet_name='Sheet1 (2)')
        print(df_cap.head(n_rows))
    except Exception as e:
        print(f"ERROR: {e}")


def get_date_range_stats(jobs_file):
    """
    Get statistics about date ranges in jobs file.
    
    Args:
        jobs_file (str): Path to jobs file
    """
    print("\nDate Range Analysis")
    print("-" * 60)
    
    try:
        if jobs_file.endswith('.csv'):
            df = pd.read_csv(jobs_file)
        else:
            df = pd.read_excel(jobs_file)
        
        due_col = JOBS_FILE_COLUMNS['due']
        df['due_datetime'] = df[due_col].apply(lambda x: parse_date(str(x)))
        
        print(f"Earliest due date: {df['due_datetime'].min()}")
        print(f"Latest due date: {df['due_datetime'].max()}")
        print(f"Date range: {(df['due_datetime'].max() - df['due_datetime'].min()).days} days")
        
        # Jobs by month
        df['year_month'] = df['due_datetime'].dt.to_period('M')
        monthly_counts = df.groupby('year_month').size()
        
        print("\nJobs by month:")
        for period, count in monthly_counts.items():
            print(f"  {period}: {count} jobs")
        
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    """
    Main utility function.
    """
    print("\nJob Priority System - Utilities")
    print("="*60)
    
    # Update these paths to match your files
    JOBS_FILE = 'jobs_data.csv'
    CAPABILITY_FILE = 'RM Codes Crew Capability.xlsx'
    
    print("\nAvailable utilities:")
    print("1. Validate jobs file")
    print("2. Validate capability file")
    print("3. Preview data")
    print("4. Date range analysis")
    
    print("\nUncomment the desired utility function to run it.")
    
    # Uncomment the utility you want to run:
    # validate_jobs_file(JOBS_FILE)
    # validate_capability_file(CAPABILITY_FILE)
    # preview_data(JOBS_FILE, CAPABILITY_FILE)
    # get_date_range_stats(JOBS_FILE)


if __name__ == "__main__":
    main()
