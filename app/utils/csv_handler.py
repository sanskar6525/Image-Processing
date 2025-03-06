import pandas as pd
from fastapi import HTTPException

def validate_csv(file_path: str):
    """Validate the CSV file format and required columns."""
    df = pd.read_csv(file_path)

    required_columns = {"Serial Number", "Product Name", "Input Image Urls"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="CSV file is missing required columns")

    for index, row in df.iterrows():
        if pd.isna(row["Serial Number"]) or pd.isna(row["Product Name"]) or pd.isna(row["Input Image Urls"]):
            raise HTTPException(status_code=400, detail=f"Missing data in row {index + 1}")

        image_urls = row["Input Image Urls"].split(",")
        for url in image_urls:
            if not url.strip().startswith("http"):
                raise HTTPException(status_code=400, detail=f"Invalid image URL in row {index + 1}")

    return True
