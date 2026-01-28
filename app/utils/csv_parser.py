# app/utils/csv_parser.py

import csv
import pandas as pd
from typing import List


def read_values(file_path: str) -> List[str]:
    """
    Reads CSV or Excel (.xlsx) file and returns list of values
    """
    values = []

    if file_path.endswith(".csv"):
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip():
                    values.append(row[0].strip())

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path, header=None)
        for val in df.iloc[:, 0]:
            if isinstance(val, str):
                values.append(val.strip())

    else:
        raise ValueError("Unsupported file format")

    return values
