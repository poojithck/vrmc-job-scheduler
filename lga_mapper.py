"""
LGA mapping module for area assignment.
"""

import pandas as pd
from config import LGA_MAPPING_FILE_COLUMNS, JOBS_FILE_COLUMNS


def load_lga_mapping(file_path):
    """
    Load LGA to Area mapping from Excel file.
    
    Args:
        file_path (str): Path to the LGA mapping Excel file
        
    Returns:
        pd.DataFrame: Cleaned LGA mapping dataframe
    """
    # Load the mapping file
    df = pd.read_excel(file_path)
    
    lga_col = LGA_MAPPING_FILE_COLUMNS['lga']
    area_col = LGA_MAPPING_FILE_COLUMNS['area']
    
    # Validate required columns
    if lga_col not in df.columns or area_col not in df.columns:
        raise ValueError(f"Mapping file must contain '{lga_col}' and '{area_col}' columns")
    
    # Clean and deduplicate
    cleaned_df = clean_lga_mapping(df)
    
    return cleaned_df


def clean_lga_mapping(mapping_df):
    """
    Clean LGA mapping data by removing spaces and handling duplicates.
    
    Args:
        mapping_df (pd.DataFrame): Raw LGA mapping dataframe
        
    Returns:
        pd.DataFrame: Cleaned and deduplicated mapping dataframe
    """
    lga_col = LGA_MAPPING_FILE_COLUMNS['lga']
    area_col = LGA_MAPPING_FILE_COLUMNS['area']
    
    # Create a copy to avoid modifying original
    df = mapping_df[[lga_col, area_col]].copy()
    
    # Clean LGA column
    df['LGA_cleaned'] = clean_lga_value(df[lga_col])
    
    # Remove rows where LGA is null after cleaning
    df = df[df['LGA_cleaned'].notna()]
    
    # Handle duplicates - keep first occurrence
    df_dedup = df.drop_duplicates(subset=['LGA_cleaned'], keep='first')
    
    # Report duplicates if any
    duplicates = df[df.duplicated(subset=['LGA_cleaned'], keep=False)]
    if len(duplicates) > 0:
        print(f"\nWarning: Found {len(duplicates)} duplicate LGA entries in mapping file")
        print("Keeping first occurrence for each LGA:")
        unique_lgas = duplicates['LGA_cleaned'].unique()
        for lga in unique_lgas[:5]:  # Show first 5
            areas = duplicates[duplicates['LGA_cleaned'] == lga][area_col].tolist()
            print(f"  LGA: {lga} → Areas: {areas}")
        if len(unique_lgas) > 5:
            print(f"  ... and {len(unique_lgas) - 5} more")
    
    # Keep only necessary columns
    result = df_dedup[['LGA_cleaned', area_col]].copy()
    result.columns = ['LGA_cleaned', 'Area']
    
    return result


def clean_lga_value(lga_series):
    """
    Clean LGA values by removing spaces and standardizing format.
    
    Args:
        lga_series (pd.Series): Series of LGA values
        
    Returns:
        pd.Series: Cleaned LGA values
    """
    def clean_single_lga(lga_value):
        if pd.isna(lga_value):
            return None
        
        # Convert to string
        lga_str = str(lga_value)
        
        # Remove all whitespace (spaces, tabs, newlines)
        lga_cleaned = ''.join(lga_str.split())
        
        # Convert to uppercase for case-insensitive matching
        lga_cleaned = lga_cleaned.upper()
        
        # Return None if empty after cleaning
        if not lga_cleaned:
            return None
            
        return lga_cleaned
    
    return lga_series.apply(clean_single_lga)


def merge_area_mapping(jobs_df, mapping_df):
    """
    Merge jobs dataframe with LGA to Area mapping.
    
    Args:
        jobs_df (pd.DataFrame): Jobs dataframe
        mapping_df (pd.DataFrame): LGA mapping dataframe
        
    Returns:
        pd.DataFrame: Jobs dataframe with Area column added
    """
    lga_col = JOBS_FILE_COLUMNS.get('lga', 'LGA')
    
    # Check if LGA column exists in jobs data
    if lga_col not in jobs_df.columns:
        print(f"\nWarning: '{lga_col}' column not found in jobs data")
        print("Area mapping will be skipped. Available columns:")
        print(f"  {list(jobs_df.columns)}")
        jobs_df['Area'] = None
        return jobs_df
    
    # Create a copy
    merged_df = jobs_df.copy()
    
    # Clean LGA column in jobs data
    merged_df['LGA_cleaned'] = clean_lga_value(merged_df[lga_col])
    
    # Merge with mapping
    merged_df = merged_df.merge(
        mapping_df[['LGA_cleaned', 'Area']],
        on='LGA_cleaned',
        how='left'
    )
    
    # Report unmatched LGAs
    unmatched = merged_df[merged_df['Area'].isna()]
    if len(unmatched) > 0:
        unique_unmatched = unmatched['LGA_cleaned'].dropna().unique()
        print(f"\nWarning: {len(unmatched)} jobs have no Area mapping")
        print(f"Unique unmatched LGAs: {len(unique_unmatched)}")
        if len(unique_unmatched) > 0:
            print("Sample unmatched LGAs:")
            for lga in list(unique_unmatched)[:5]:
                count = (unmatched['LGA_cleaned'] == lga).sum()
                print(f"  {lga} ({count} jobs)")
            if len(unique_unmatched) > 5:
                print(f"  ... and {len(unique_unmatched) - 5} more")
    
    # Report successful matches
    matched = merged_df[merged_df['Area'].notna()]
    if len(matched) > 0:
        print(f"\nSuccessfully mapped {len(matched)} jobs to Areas")
        area_counts = matched['Area'].value_counts()
        print(f"Number of unique Areas: {len(area_counts)}")
        print("\nTop 5 Areas by job count:")
        for area, count in area_counts.head(5).items():
            print(f"  {area}: {count} jobs")
    
    # Drop the temporary cleaned column
    merged_df = merged_df.drop(columns=['LGA_cleaned'])
    
    return merged_df