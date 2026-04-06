# entry point, start cli

from app.data_loader import (
    read_csv_file,
    apply_normalized_columns,
    dataframe_to_rows
)


def main():
    # 1. Read the CSV file
    df = read_csv_file("data/sample.csv")

    # 2. Show original columns
    print("Original columns:")
    print(list(df.columns))

    # 3. Normalize columns
    df = apply_normalized_columns(df)

    # 4. Show normalized columns
    print("\nNormalized columns:")
    print(list(df.columns))

    # 5. Convert DataFrame to row tuples
    rows = dataframe_to_rows(df)

    # 6. Print rows
    print("\nRows:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()