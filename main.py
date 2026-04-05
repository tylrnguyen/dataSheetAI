# entry point, start cli

from app.db import (
    get_connection,
    execute_non_query,
    execute_query,
    close_connection
)


def main():
    # connect to database
    conn = get_connection("app_data.db")

    # create a test table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS test_people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER
    )
    """
    execute_non_query(conn, create_table_sql)

    # 3. Insert a sample row
    insert_sql = "INSERT INTO test_people (name, age) VALUES (?, ?)"
    execute_non_query(conn, insert_sql, ("Alice", 25))

    # 4. Query the table
    select_sql = "SELECT * FROM test_people"
    rows = execute_query(conn, select_sql)

    # 5. Print results
    print("Query Results:")
    for row in rows:
        print(row)

    # 6. Close connection
    close_connection(conn)


if __name__ == "__main__":
    main()