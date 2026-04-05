# low level SQLite connection code 
import sqlite3

# open sqlite connection, return connection object
def get_connection(db_path: str): 
    conn = sqlite3.connect(db_path)
    return conn

def execute_non_query(conn, sql: str, params: tuple = ()): 
    # cursor is "messenger" that executes SQL and returns results
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()

# sql statements that read data, mainly SELECT 
def execute_query(conn, sql: str, params: tuple = ()): 
    cursor = conn.cursor()
    cursor.execute(sql, params)
    results = cursor.fetchall()
    return results

def close_connection(conn):
    conn.close()