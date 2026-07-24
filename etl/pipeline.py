"""
Runs the full ETL pipeline: Extract -> Transform -> Load
This is the single entry point you (or a scheduler like Airflow/cron) would call.
"""

from extract import extract_raw_data
from transform import transform_data
from load import load_data


def run_etl():
    print("=== ETL PIPELINE START ===")
    raw_df = extract_raw_data()
    clean_df = transform_data(raw_df)
    path = load_data(clean_df)
    print("=== ETL PIPELINE COMPLETE ===")
    return path


if __name__ == "__main__":
    run_etl()