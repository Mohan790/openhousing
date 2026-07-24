import pandas as pd
import numpy as np


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Create a copy so the original data is not modified
    df = df.copy()

    # 1. Handle missing numeric values
    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    # 2. Remove invalid house prices
    df = df[df["medv"] > 0]

    # 3. Convert house price from thousands of dollars to USD
    df["price_usd"] = df["medv"] * 1000

    # 4. Create a new engineered feature
    df["rooms_per_dis"] = df["rm"] / df["dis"]

    print(f"[transform] {len(df)} rows after cleaning")

    return df


if __name__ == "__main__":
    from extract import extract_raw_data

    raw = extract_raw_data()

    clean = transform_data(raw)

    print(clean.head())