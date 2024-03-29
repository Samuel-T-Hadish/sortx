"""This module contains utility functions for loading data."""
import base64
import io
import pandas as pd

def get_df_from_string_content(contents: str, filename: str) -> pd.DataFrame:

    decoded = base64.b64decode(contents.split(",")[1])

    df = pd.DataFrame()
    if "csv" in filename:
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif "xls" in filename:
        df = pd.read_excel(io.BytesIO(decoded))
    return df
