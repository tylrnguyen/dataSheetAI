# entry point, start cli

from app.data_loader import read_csv_file, apply_normalized_columns
from app.schema_manager import (
    infer_column_types,
    build_create_table_sql,
    get_existing_tables,
    get_table_schema,
    schemas_match
)
from app.db import get_connection, execute_non_query, close_connection


def main():
    df = read_csv_file("data/sample.csv")
    df = apply_normalized_columns(df)

    csv_schema = infer_column_types(df)
    print("Inferred CSV schema:")
    print(csv_schema)

    table_name = "people"
    create_sql = build_create_table_sql(table_name, csv_schema)
    print("\nCreate table SQL:")
    print(create_sql)

    conn = get_connection("app_data.db")
    execute_non_query(conn, create_sql)

    print("\nExisting tables:")
    print(get_existing_tables(conn))

    db_schema = get_table_schema(conn, table_name)
    print("\nDatabase schema:")
    print(db_schema)

    print("\nSchemas match:")
    print(schemas_match(csv_schema, db_schema))

    close_connection(conn)


if __name__ == "__main__":
    main()