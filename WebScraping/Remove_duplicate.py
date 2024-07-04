import pandas as pd

def remove_duplicate_row(file): # work perfectly
  
    df = pd.read_csv(file)
    df_deduplicated = df.drop_duplicates(subset=df.columns.difference(['DATE']), inplace=False)
    df_deduplicated.to_csv(file, index=False)
    print ("Duplicates removed from the CSV file.")

file_path = r"File path" 
remove_duplicate_row(file_path)

def remove_duplicate_rows(Old_file, New_file):
    """
    Removes duplicate rows from the second CSV file based on all columns (excluding DATE)
    in the first file. Handles slight variations in data using fuzzy matching (optional).

    Args:
        file1_path (str): Path to the first CSV file.
        file2_path (str): Path to the second CSV file (will be overwritten).
    """

    # Read CSV files into DataFrames
    df1 = pd.read_csv(Old_file, encoding='utf-8')
    df2 = pd.read_csv(New_file, encoding='utf-8')

    # Ensure both LATITUDE columns have the same data type
    df1['LATITUDE'] = df1['LATITUDE'].astype(str)
    df2['LATITUDE'] = df2['LATITUDE'].astype(str)
    df1['LONGITUDE'] = df1['LONGITUDE'].astype(str)
    df2['LONGITUDE'] = df2['LONGITUDE'].astype(str)

    # Exclude the DATE column from the list of columns to compare
    compare_columns = list(df2.columns)
    compare_columns.remove("DATE")

    # Merge on all columns except DATE (left join)
    merged_df = df2.merge(df1[compare_columns], how="left", indicator=True)

    # Print merged dataframe for debugging
    # print("Merged DataFrame:\n", merged_df)

    # Filter rows where the merge indicator is 'both' (meaning present in both files)
    filtered_df = merged_df[merged_df["_merge"] == "both"].drop("_merge", axis=1)

    # Print filtered dataframe for debugging
    print("Filtered DataFrame (Duplicates):\n", filtered_df)

    # Remove duplicate rows and save back to the original file (overwrite)
    df2 = df2[~df2.index.isin(filtered_df.index)]
    df2.to_csv(New_file, index=False)

    print(f"Duplicate rows removed from {New_file} based on all columns in {Old_file}.")

# Define file paths (assuming REALTOR.csv is the file to modify)
Old_file = r"Old file path"
New_file = r"new path"

# Remove duplicate rows from the second CSV file
# remove_duplicate_rows(Old_file, New_file)
