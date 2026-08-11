"""
Basic tests to prove the ETL pipeline works — this is what CI runs
automatically on every push.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "etl"))

from extract import extract_raw_data
from transform import transform_data


def test_extract_returns_expected_shape():
    df = extract_raw_data()
    assert len(df) > 400
    assert "medv" in df.columns


def test_transform_removes_nulls():
    df = extract_raw_data()
    clean = transform_data(df)
    assert clean.isna().sum().sum() == 0


def test_transform_creates_usd_price():
    df = extract_raw_data()
    clean = transform_data(df)
    assert "price_usd" in clean.columns
    assert (clean["price_usd"] > 0).all()
