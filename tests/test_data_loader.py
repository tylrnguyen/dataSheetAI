import pandas as pd

from app.data_loader import (
    normalize_column_names,
    apply_normalized_columns,
    dataframe_to_rows,
)


def test_normalize_column_names():
    cols = [" First Name ", "Age(years)", "favorite color"]
    assert normalize_column_names(cols) == ["first_name", "ageyears", "favorite_color"]


def test_apply_normalized_columns():
    df = pd.DataFrame({" First Name ": ["Ada"], "Favorite Color": ["Blue"]})
    normalized_df = apply_normalized_columns(df)

    assert list(normalized_df.columns) == ["first_name", "favorite_color"]


def test_dataframe_to_rows_normalizes_columns_and_returns_tuples():
    df = pd.DataFrame({"A Value": [1, 2], "B-Value": ["x", "y"]})
    rows = dataframe_to_rows(df)

    assert rows == [(1, "x"), (2, "y")]
    assert list(df.columns) == ["a_value", "bvalue"]
