# reads csv w pandas, converts to records that can be inserted manually 
# allow pands.read_csv() but not df.to_sql() or df.to_sqlite() or any other method that abstracts away the SQL writing

import pandas as pd

def read_csv_file(file_path: str): 
    df = pd.read_csv(file_path)
    return df

# take column name, make it db friendly
def normalize_column_names(col_names: list[str]) -> list[str]:
    normalized = []
    for col in col_names: 
        col = col.strip().lower().replace(' ', '_')
        col = ''.join(e for e in col if e.isalnum() or e == '_')
        normalized.append(col)
    return normalized

def apply_normalized_columns(df): 
    df.columns = normalize_column_names(df.columns)
    return df

def dataframe_to_rows(df): 
    df = apply_normalized_columns(df)
    rows = [tuple(row) for row in df.to_numpy()]
    return rows