# dataSheetAI

dataSheetAI is a command-line application that ingests CSV files into SQLite and lets users query data in two ways:

- Direct SQL queries
- Natural language questions translated into SQL

The project emphasizes transparency and safety:

- SQL is always validated before execution
- Only read-only SELECT queries are allowed
- Natural language queries are converted to SQL and shown to the user

## What the System Does

1. Loads CSV data into a SQLite database table.
2. Normalizes CSV column names to SQL-friendly identifiers.
3. Infers SQLite-compatible column types from pandas DataFrame dtypes.
4. Executes validated SQL queries against loaded tables.
5. Converts natural language questions into SQL using an adapter layer.

## Architecture Overview

The system is organized into modules with clear responsibilities:

- CLI and interaction layer
- Data ingestion and schema inference layer
- Query orchestration layer
- SQL validation layer
- Low-level database layer
- LLM adapter layer

### Module Responsibilities

- app/cli.py
  - Handles menu loop and user interaction.
  - Routes requests to ingestion, SQL query, or NL query flows.
  - Re-prompts on empty input.
  - Prints generated SQL for NL queries.

- app/data_loader.py
  - Reads CSV via pandas.
  - Normalizes column names.
  - Converts DataFrame rows to tuples for insert operations.

- app/schema_manager.py
  - Infers SQLite types from DataFrame dtypes.
  - Builds CREATE TABLE SQL.
  - Reads existing table names and table schema from SQLite.

- app/db.py
  - Owns low-level sqlite3 connection and query execution.
  - Provides insert SQL generation and batch row insertion.

- app/sql_validator.py
  - Validates query safety and correctness against known schema.
  - Enforces SELECT-only execution and blocks forbidden keywords.

- app/llm_adapter.py
  - Converts natural language to SQL using deterministic rules.
  - Includes prompt-building utilities for future external LLM use.

- app/query_service.py
  - Orchestrates generation, validation, and execution.
  - Returns uniform success or error results.

## Ingestion Flow

1. User selects "Load CSV into database".
2. CLI prompts for CSV path and table name (rejects empty input).
3. CSV is read into DataFrame.
4. Column names are normalized (lowercase, spaces to underscores, symbols removed).
5. Column types are inferred and CREATE TABLE SQL is built.
6. Table is created if it does not already exist.
7. Rows are converted and inserted with parameterized SQL.

## Query Flow

### Direct SQL Query Flow

1. User selects "Run SQL query".
2. CLI reads SQL input (rejects empty input).
3. Current DB schema is built from SQLite metadata.
4. SQL is validated.
5. If valid, SQL is executed and rows are printed.
6. If invalid, validator error is shown.

### Natural Language Query Flow

1. User selects "Ask a question (natural language)".
2. CLI reads question input (rejects empty input).
3. Current DB schema is built from SQLite metadata.
4. Adapter generates SQL from natural language.
5. Generated SQL is printed to the CLI.
6. Generated SQL is validated and, if valid, executed.

## How Validation Works

Validation is implemented in app/sql_validator.py and applied before every execution:

1. Empty query check.
2. Multiple statement check.
3. Forbidden keyword check (INSERT, UPDATE, DELETE, DROP, ALTER, CREATE).
4. SELECT-only check.
5. Table existence check against live schema.
6. Column existence check against allowed columns.

If any check fails, execution is blocked and a clear error is returned.

## How LLM Integration Works

The adapter supports two modes:

1. Stub mode (default)
  - Enabled when `USE_STUB=true`.
  - Uses deterministic keyword rules in `generate_sql_stub()`.

2. Gemini model mode
  - Enabled when `USE_STUB=false`.
  - Uses the `openai` Python client against Gemini's OpenAI-compatible endpoint in `generate_sql_gemini()`.
  - Requires `GEMINI_API_KEY` to be set.

This split keeps local testing reproducible while allowing model-backed NL queries when configured.

## One Limitation

Natural language quality depends on mode. Stub mode is intentionally narrow and rule-based, while model mode requires external API availability and key configuration.

## How to Run the Project

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you install packages manually, you must include `openai` for model-backed natural language queries:

```bash
pip install openai
```

### 3. Configure natural language mode

By default, the project uses stub mode (`USE_STUB=true`).

To enable model-backed natural language queries:

```bash
export USE_STUB=false
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Start the CLI

```bash
python main.py
```

You can then:

1. Load CSV into database
2. Run SQL query
3. Ask natural-language question
4. Exit

## How to Run Tests

```bash
pytest -q
```

## Evaluation Criteria

The project is evaluated using the following criteria:

1. Ingestion correctness
	- CSV columns normalize predictably.
	- Type inference maps to expected SQLite types.
	- Rows are inserted and retrievable.

2. Query safety and correctness
	- Only valid SELECT queries are executed.
	- Unknown tables and columns are rejected.
	- Forbidden operations are blocked.

3. NL query transparency
	- Generated SQL is shown to the user.
	- Generated SQL goes through the same validator path as direct SQL.

4. CLI UX resilience
	- Empty inputs are rejected and re-prompted in active flow.
	- Invalid menu choices produce explicit guidance.

5. Automated quality gate
	- Test suite runs in GitHub Actions on every push and pull request to main.

## Design Justification

1. Separation of concerns
	- Each module has a single responsibility, which improves maintainability and testability.

2. Validator-first execution
	- Both SQL and NL paths converge on the same validation gate, reducing risk and behavior drift.

3. Schema-aware checks
	- Validation uses live schema introspection, so checks match the current database state.

4. Deterministic adapter baseline
	- Rule-based NL-to-SQL provides predictable behavior while the rest of the pipeline is stabilized.

## CI Setup

GitHub Actions workflow is defined in .github/workflows/test.yml.

It runs on:

- push to main
- pull request to main

And performs:

1. Python 3.11 setup
2. Dependency installation
3. pytest execution
