# protects database 
# only valid SELECT queries should run 

def is_select_query(sql): 
    # simple check: does it start with "SELECT" (case-insensitive)
    return sql.strip().lower().startswith("select")

def extract_table_names(sql):
    # find table names after FROM and JOIN
    import re
    pattern = r"(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    return re.findall(pattern, sql, re.IGNORECASE)

def extract_column_names(sql):
    # find column names in SELECT clause
    import re
    pattern = r"SELECT\s+(.*?)\s+FROM"
    match = re.search(pattern, sql, re.IGNORECASE)
    if match:
        columns_part = match.group(1).strip()
        if columns_part == "*":
            return ["*"]
        columns = [col.strip() for col in columns_part.split(",")]
        return columns
    return []

def validate_sql_query(sql, db_schema):
    if not is_select_query(sql):
        return False, "Only SELECT queries are allowed"

    table_names = extract_table_names(sql)
    if not table_names:
        return False, "No valid table found in query"

    for table in table_names:
        if table not in db_schema:
            return False, f"Unknown table: {table}"

    column_names = extract_column_names(sql)
    if not column_names:
        return False, "No valid columns found in query"

    if column_names == ["*"]:
        return True, "Valid query"

    allowed_columns = set()
    for table in table_names:
        allowed_columns.update(db_schema[table].keys())

    for column in column_names:
        if column not in allowed_columns:
            return False, f"Unknown column: {column}"

    return True, "Valid query"