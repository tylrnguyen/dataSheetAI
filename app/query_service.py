# controls traffic, coordinates query flow
# orchestration layer

from app.sql_validator import validate_sql_query
from app.db import execute_query
from app.llm_adapter import generate_sql

def run_sql_query(conn, sql, db_schema): 
    # execute the SQL query using the provided connection and database schema
    # return the results of the query
    is_valid, error_message = validate_sql_query(sql, db_schema)

    if not is_valid: 
        return False, error_message
    
    results = execute_query(conn, sql)

    return True, results

def run_nlq(conn, nlq, db_schema): 
    # take a natural language query, generate SQL, validate it, and execute it
    sql = generate_sql(nlq, db_schema)
    return run_sql_query(conn, sql, db_schema)