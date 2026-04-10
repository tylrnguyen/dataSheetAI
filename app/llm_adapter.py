# takes natural language and asks llm for sql
# doesn't execute sql 

def build_schema_context(db_schema): 
    lines = []

    for table, columns in db_schema.items():
        lines.append(f"Table: {table}")
        for col, col_type in columns.items():
            lines.append(f"  - {col} ({col_type})")
    return "\n".join(lines)

def build_prompt(natural_language_query, db_schema):
    schema_context = build_schema_context(db_schema)
    prompt = f"""
You are an assistant that translates natural language queries into SQL queries.

Database schema:
{schema_context}

Rules: 
- Only generate SELECT queries.
- Use table and column names exactly as they appear in the schema.
- Do not modify the database 
- Return only the SQL query 

User question: 
{natural_language_query}
"""
    return prompt.strip()

def generate_sql(user_question, db_schema): 
    prompt = user_question.lower()

    if "all" in question or "everything" in question: 
        return "SELECT * FROM people"
    
    if "name" in question and "age" in question: 
        return "SELECT name, age FROM people"
    
    if "color" in question: 
        return "SELECT favorite_color FROM people"
    
    # fallback 
    return "SELECT * FROM people" 