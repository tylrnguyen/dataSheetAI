from app.db import (
    get_connection,
    execute_non_query,
    execute_query,
    build_insert_sql,
    insert_rows,
    close_connection,
)


def test_build_insert_sql():
    sql = build_insert_sql("people", ["name", "age"])
    assert sql == "INSERT INTO people (name, age) VALUES (?, ?);"


def test_execute_and_insert_rows_roundtrip():
    conn = get_connection(":memory:")
    try:
        execute_non_query(conn, "CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);")
        insert_rows(conn, "people", ["name", "age"], [("Ada", 36), ("Linus", 30)])

        results = execute_query(conn, "SELECT name, age FROM people ORDER BY id")
        assert results == [("Ada", 36), ("Linus", 30)]
    finally:
        close_connection(conn)
