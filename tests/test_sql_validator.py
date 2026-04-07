from app.sql_validator import (
    is_select_query,
    extract_table_names,
    extract_column_names,
    validate_sql_query
)


def main():
    db_schema = {
        "people": {
            "name": "TEXT",
            "age": "INTEGER",
            "favorite_color": "TEXT"
        }
    }

    queries = [
        "SELECT * FROM people",
        "SELECT name, age FROM people",
        "SELECT favorite_color FROM people",
        "DELETE FROM people",
        "SELECT salary FROM people",
        "SELECT name FROM employees"
    ]

    for query in queries:
        print("\nQuery:", query)
        print("is_select_query:", is_select_query(query))
        print("table_names:", extract_table_names(query))
        print("column_names:", extract_column_names(query))
        print("validation:", validate_sql_query(query, db_schema))


if __name__ == "__main__":
    main()