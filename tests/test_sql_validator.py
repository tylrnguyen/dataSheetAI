from app.sql_validator import (
    is_select_query,
    extract_table_names,
    extract_column_names,
    validate_sql_query
)


import pytest


DB_SCHEMA = {
    "people": {
        "name": "TEXT",
        "age": "INTEGER",
        "favorite_color": "TEXT"
    }
}


def test_is_select_query():
    assert is_select_query("SELECT * FROM people") is True
    assert is_select_query("  select name from people") is True
    assert is_select_query("DELETE FROM people") is False


def test_extract_table_names():
    assert extract_table_names("SELECT * FROM people") == ["people"]
    assert extract_table_names("SELECT p.name FROM people p JOIN teams t ON p.id = t.person_id") == ["people", "teams"]


def test_extract_column_names():
    assert extract_column_names("SELECT * FROM people") == ["*"]
    assert extract_column_names("SELECT name, age FROM people") == ["name", "age"]


@pytest.mark.parametrize(
    "query, expected_valid, expected_message",
    [
        ("SELECT * FROM people", True, "Valid query"),
        ("SELECT name, age FROM people", True, "Valid query"),
        ("DELETE FROM people", False, "Query contains forbidden keywords"),
        ("SELECT salary FROM people", False, "Unknown column: salary"),
        ("SELECT name FROM employees", False, "Unknown table: employees"),
        ("", False, "Empty query is not allowed"),
    ],
)
def test_validate_sql_query(query, expected_valid, expected_message):
    is_valid, message = validate_sql_query(query, DB_SCHEMA)
    assert is_valid is expected_valid
    assert message == expected_message