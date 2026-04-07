from app.data_loader import read_csv_file, apply_normalized_columns, dataframe_to_rows
from app.schema_manager import infer_column_types, build_create_table_sql
from app.db import (
    get_connection,
    execute_non_query,
    execute_query,
    insert_rows,
    close_connection
)


def main():
    table_name = "people"

    # 1. Read and prepare CSV
    df = read_csv_file("data/sample.csv")
    df = apply_normalized_columns(df)

    print("Normalized columns:")
    print(list(df.columns))

    # 2. Infer schema
    csv_schema = infer_column_types(df)
    print("\nInferred schema:")
    print(csv_schema)

    # 3. Build CREATE TABLE SQL
    create_sql = build_create_table_sql(table_name, csv_schema)
    print("\nCreate table SQL:")
    print(create_sql)

    # 4. Connect to database
    conn = get_connection("app_data.db")

    # 5. Create table
    execute_non_query(conn, create_sql)

    # 6. Convert DataFrame to rows
    rows = dataframe_to_rows(df)
    print("\nRows to insert:")
    for row in rows:
        print(row)

    # 7. Insert rows
    insert_rows(conn, table_name, list(df.columns), rows)

    # 8. Query data back out
    results = execute_query(conn, f"SELECT * FROM {table_name};")
    print("\nRows in database:")
    for result in results:
        print(result)

    # 9. Close connection
    close_connection(conn)


if __name__ == "__main__":
    main()