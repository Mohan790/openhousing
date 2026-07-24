import pandas as pd
import os


PROCESSED_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "processed_housing.csv"
)


def load_data(df: pd.DataFrame) -> None:
    # Create the data folder if it does not exist
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    # Save the transformed data
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"[load] {len(df)} rows saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    from extract import extract_raw_data
    from transform import transform_data

    raw_data = extract_raw_data()
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)