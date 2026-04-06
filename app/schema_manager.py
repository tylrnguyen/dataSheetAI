# figures out column names/types
# checks existing tables, compares schemas
# decides append vs create 

from app.db import execute_query

# looks at each dataframe column, decide which sqlite type it should map to
def infer_column_types(df):
    type_mapping = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'object': 'TEXT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP'
    }
    # inspect df.dtypes, map to sqlite types, store in dict
    column_types = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        column_types[col] = type_mapping.get(dtype, 'TEXT')
    return column_types

# build CREATE TABLE statement based on column names and types
def build_create_table_sql(table_name, columns):
    column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

    for col, col_type in columns.items():
        column_defs.append(f"{col} {col_type}")

    cols_sql = ", ".join(column_defs)
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_sql});"
    return create_sql  

def get_existing_tables(conn):
    sql = """
    SELECT name FROM sqlite_master
    WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """
    tables = execute_query(conn, sql)
    return [t[0] for t in tables]

def get_table_schema(conn, table_name):
    sql = f"PRAGMA table_info({table_name});"
    schema_info = execute_query(conn, sql)
    # schema_info is list of tuples: (cid, name, type, notnull, dflt_value, pk)
    # convert to dict of column name -> type
    schema = {col[1]: col[2] for col in schema_info if col[1] != "id"}    
    return schema

def schemas_match(csv_schema, db_schema):
    # check if all columns in csv_schema are in db_schema with same type
    for col, col_type in csv_schema.items():
        if col not in db_schema or db_schema[col] != col_type:
            return False
    return True