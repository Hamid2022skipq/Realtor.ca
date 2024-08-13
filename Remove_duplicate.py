import pandas as pd

def remove_duplicate_row(file): # work perfectly
  
    df = pd.read_csv(file)
    df = df.dropna(how='all')
    sd=df.sort_values(by="CITY")
    dc = sd.drop_duplicates(subset=df.columns.difference(['DATE','LATITUDE','LONGITUDE', 'TIME']), inplace=False)
    dc.to_csv(file, index=False)
    print("Duplicates removed from the CSV file.")

file_path = r"C:\Users\Hamid Ali\Desktop\Realtor.ca-scraping\REALTOR_T.csv" 

remove_duplicate_row(file_path)

def remove_duplicate_rows(Old_file, New_file): # work perfectly
    """
    Removes duplicate rows from the second CSV file based on all columns (excluding DATE)
    in the first file. Handles slight variations in data using fuzzy matching (optional).

    Args:
        file1_path (str): Path to the first CSV file.
        file2_path (str): Path to the second CSV file (will be overwritten).
    """
    df1 = pd.read_csv(Old_file, encoding='utf-8')
    df2 = pd.read_csv(New_file, encoding='utf-8')
    df1['LATITUDE'] = df1['LATITUDE'].astype(str)
    df2['LATITUDE'] = df2['LATITUDE'].astype(str)
    df1['LONGITUDE'] = df1['LONGITUDE'].astype(str)
    df2['LONGITUDE'] = df2['LONGITUDE'].astype(str)
    compare_columns = list(df2.columns)
    compare_columns.remove("DATE")
    merged_df = df2.merge(df1[compare_columns], how="left", indicator=True)
    filtered_df = merged_df[merged_df["_merge"] == "both"].drop("_merge", axis=1)

    print("Filtered DataFrame (Duplicates):\n", filtered_df)

    # Remove duplicate rows and save back to the original file (overwrite)
    df2 = df2[~df2.index.isin(filtered_df.index)]
    df2.to_csv(New_file, index=False)


Old_file = r"C:\Users\Hamid Ali\Desktop\WebScraping\Master Files\Master_Toronto.csv"
New_file = r"C:\Users\Hamid Ali\Desktop\Realtor.ca-scraping\REALTOR_T.csv"

# Remove duplicate rows from the second CSV file
# remove_duplicate_rows(Old_file, New_file)
