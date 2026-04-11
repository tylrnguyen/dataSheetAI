import pandas as pd

from app.db import get_connection, execute_non_query, close_connection
from app.schema_manager import (
    infer_column_types,
    build_create_table_sql,
    get_existing_tables,
    get_table_schema,
    schemas_match,
)


def test_infer_column_types():
    df = pd.DataFrame(
        {
            "name": ["Ada", "Linus"],
            "age": [36, 30],
            "score": [99.5, 88.0],
            "active": [True, False],
        }
    )

    inferred = infer_column_types(df)
    assert inferred["name"] == "TEXT"
    assert inferred["age"] == "INTEGER"
    assert inferred["score"] == "REAL"
    assert inferred["active"] == "BOOLEAN"


def test_build_create_table_sql_contains_id_and_columns():
    sql = build_create_table_sql("people", {"name": "TEXT", "age": "INTEGER"})
    assert "CREATE TABLE IF NOT EXISTS people" in sql
    assert "id INTEGER PRIMARY KEY AUTOINCREMENT" in sql
    assert "name TEXT" in sql
    assert "age INTEGER" in sql


def test_get_existing_tables_and_schema():
    conn = get_connection(":memory:")
    try:
        execute_non_query(conn, "CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);")

        tables = get_existing_tables(conn)
        schema = get_table_schema(conn, "people")

        assert "people" in tables
        assert schema == {"name": "TEXT", "age": "INTEGER"}
    finally:
        close_connection(conn)


def test_schemas_match():
    csv_schema = {"name": "TEXT", "age": "INTEGER"}
    db_schema_good = {"name": "TEXT", "age": "INTEGER", "favorite_color": "TEXT"}
    db_schema_bad = {"name": "TEXT", "age": "REAL"}

    assert schemas_match(csv_schema, db_schema_good) is True
    assert schemas_match(csv_schema, db_schema_bad) is False
