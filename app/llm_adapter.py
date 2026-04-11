import os

def build_schema_context(db_schema):
    lines = []
    for table, columns in db_schema.items():
        lines.append(f"Table: {table}")
        for col, col_type in columns.items():
            lines.append(f"- {col} ({col_type})")
    return "\n".join(lines)


def build_prompt(user_question, schema_context):
    prompt = f"""
You are an AI assistant that converts natural language into SQLite SQL queries.

Database schema:
{schema_context}

Rules:
- Only generate a SELECT query
- Use only the tables and columns provided
- Do not modify the database
- Return only raw SQL
- Do not use markdown
- Do not use code fences
- Do not include explanations

User question:
{user_question}
"""
    return prompt.strip()


def generate_sql_stub(user_question, db_schema):
    question = user_question.lower()

    if "name and age" in question or ("name" in question and "age" in question):
        return "SELECT name, age FROM people"

    if "color" in question:
        return "SELECT favorite_color FROM people"

    return "SELECT * FROM people"


def generate_sql_gemini(user_question, db_schema):
    from openai import OpenAI

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    schema_context = build_schema_context(db_schema)
    prompt = build_prompt(user_question, schema_context)

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    return sql

def clean_sql_output(text):
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        # remove first fence line like ``` or ```sqlite
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # remove last fence line if present
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text

def generate_sql(user_question, db_schema):
    use_stub = os.getenv("USE_STUB", "true").lower() == "true"

    if use_stub:
        return generate_sql_stub(user_question, db_schema)

    return generate_sql_gemini(user_question, db_schema)