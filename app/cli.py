# handles input() and print() 
# should never write SQL itself, doesn't talk to SQLite directly

from app.db import get_connection, execute_non_query, insert_rows, close_connection
from app.data_loader import read_csv_file, apply_normalized_columns, dataframe_to_rows
from app.schema_manager import (
    infer_column_types,
    build_create_table_sql,
    get_existing_tables,
    get_table_schema
)
from app.query_service import run_sql_query


def build_db_schema(conn):
    db_schema = {}
    tables = get_existing_tables(conn)

    for table in tables:
        db_schema[table] = get_table_schema(conn, table)

    return db_schema


def load_csv_into_db(conn):
    file_path = input("Enter CSV file path: ").strip()
    table_name = input("Enter table name: ").strip()

    try:
        df = read_csv_file(file_path)
        df = apply_normalized_columns(df)

        csv_schema = infer_column_types(df)
        create_sql = build_create_table_sql(table_name, csv_schema)
        execute_non_query(conn, create_sql)

        rows = dataframe_to_rows(df)
        insert_rows(conn, table_name, list(df.columns), rows)

        print(f"Loaded {len(rows)} rows into table '{table_name}'.")
    except Exception as e:
        print("Error loading CSV:", e)


def handle_sql_query(conn):
    sql = input("Enter SQL query: ").strip()
    db_schema = build_db_schema(conn)

    success, result = run_sql_query(conn, sql, db_schema)

    if success:
        print("Query results:")
        for row in result:
            print(row)
    else:
        print("Query failed:", result)


def run_cli():
    conn = get_connection("app_data.db")

    while True:
        print("\n--- Menu ---")
        print("1. Load CSV into database")
        print("2. Run SQL query")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            load_csv_into_db(conn)
        elif choice == "2":
            handle_sql_query(conn)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    close_connection(conn)