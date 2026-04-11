import sqlite3

from app.query_service import run_sql_query, run_nlq


def setup_people_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, favorite_color TEXT)")
    cur.executemany(
        "INSERT INTO people (name, age, favorite_color) VALUES (?, ?, ?)",
        [("Ada", 36, "Blue"), ("Grace", 85, "Green")],
    )
    conn.commit()
    return conn


def test_run_sql_query_valid_select():
    conn = setup_people_db()
    schema = {"people": {"name": "TEXT", "age": "INTEGER", "favorite_color": "TEXT"}}
    try:
        success, result = run_sql_query(conn, "SELECT name FROM people ORDER BY name", schema)
        assert success is True
        assert result == [("Ada",), ("Grace",)]
    finally:
        conn.close()


def test_run_sql_query_invalid_non_select():
    conn = setup_people_db()
    schema = {"people": {"name": "TEXT", "age": "INTEGER", "favorite_color": "TEXT"}}
    try:
        success, result = run_sql_query(conn, "DELETE FROM people", schema)
        assert success is False
        assert "forbidden" in result.lower()
    finally:
        conn.close()


def test_run_nlq_returns_generated_sql_and_results(monkeypatch):
    conn = setup_people_db()
    schema = {"people": {"name": "TEXT", "age": "INTEGER", "favorite_color": "TEXT"}}

    monkeypatch.setattr("app.query_service.generate_sql", lambda nlq, db_schema: "SELECT name FROM people ORDER BY name")

    try:
        success, result, sql = run_nlq(conn, "show me names", schema)
        assert success is True
        assert sql == "SELECT name FROM people ORDER BY name"
        assert result == [("Ada",), ("Grace",)]
    finally:
        conn.close()


def test_run_nlq_handles_generation_errors(monkeypatch):
    conn = setup_people_db()
    schema = {"people": {"name": "TEXT", "age": "INTEGER", "favorite_color": "TEXT"}}

    def fail_generate_sql(_nlq, _db_schema):
        raise RuntimeError("adapter unavailable")

    monkeypatch.setattr("app.query_service.generate_sql", fail_generate_sql)

    try:
        success, result, sql = run_nlq(conn, "show me names", schema)
        assert success is False
        assert "failed to generate sql" in result.lower()
        assert sql is None
    finally:
        conn.close()
