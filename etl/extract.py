import pandas as pd
import urllib.request
import os


SOURCE_URL = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"

RAW_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "raw_housing.csv"
)


def extract_raw_data() -> pd.DataFrame:
    # Create the data folder if it does not exist
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

    # Download the dataset
    urllib.request.urlretrieve(SOURCE_URL, RAW_PATH)

    # Read the downloaded CSV
    df = pd.read_csv(RAW_PATH)

    print(f"[extract] {len(df)} rows downloaded and saved to {RAW_PATH}")

    return df


if __name__ == "__main__":
    extract_raw_data()