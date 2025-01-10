import pandas as pd
import numpy as np

def perform_search(df: pd.DataFrame, search_terms: str) -> pd.DataFrame:
    """
    Perform multi-keyword search on DataFrame.
    
    Args:
        df: Input DataFrame
        search_terms: Space-separated search terms
    
    Returns:
        Filtered DataFrame containing rows with all search terms
    """
    if not search_terms.strip():
        return df
    
    # Split search terms and convert to lowercase
    terms = [term.lower().strip() for term in search_terms.split()]
    
    # Create a mask that will be True for rows containing all search terms
    mask = pd.Series([True] * len(df), index=df.index)
    
    for term in terms:
        term_mask = pd.Series([False] * len(df), index=df.index)
        # Search through all columns
        for column in df.columns:
            term_mask |= df[column].astype(str).str.lower().str.contains(term, na=False)
        mask &= term_mask
    
    return df[mask]

def get_data_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate statistics for the DataFrame.
    
    Args:
        df: Input DataFrame
    
    Returns:
        DataFrame containing statistics for each column
    """
    stats = []
    
    for column in df.columns:
        column_stats = {
            "Column": column,
            "Type": str(df[column].dtype),
            "Unique Values": df[column].nunique(),
            "Missing Values": df[column].isna().sum()
        }
        
        # Additional statistics for numeric columns
        if np.issubdtype(df[column].dtype, np.number):
            column_stats.update({
                "Mean": df[column].mean(),
                "Median": df[column].median(),
                "Std Dev": df[column].std(),
                "Min": df[column].min(),
                "Max": df[column].max()
            })
        
        stats.append(column_stats)
    
    stats_df = pd.DataFrame(stats)
    return stats_df.set_index("Column")
