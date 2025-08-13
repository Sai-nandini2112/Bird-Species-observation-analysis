import pandas as pd
import numpy as np
from pathlib import Path

# File paths
FOREST_FILE = Path("data/Bird_Monitoring_Data_FOREST.XLSX")
GRASS_FILE = Path("data/Bird_Monitoring_Data_GRASSLAND.XLSX")
OUT_FILE = Path("data/cleaned_bird_data.csv")

def load_and_tag(path, habitat):
    df = pd.read_excel(path, engine="openpyxl")
    df["habitat_type"] = habitat
    return df

def standardize_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )
    return df

def handle_missing(df):
    # Fill common missing values or drop if critical
    df = df.dropna(subset=["scientific_name", "date"])
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    return df

def parse_dates(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    if "start_time" in df.columns and "end_time" in df.columns:
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce").dt.time
        df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce").dt.time
    return df

def main():
    forest_df = load_and_tag(FOREST_FILE, "Forest")
    grass_df = load_and_tag(GRASS_FILE, "Grassland")
    df = pd.concat([forest_df, grass_df], ignore_index=True)

    df = standardize_columns(df)
    df = handle_missing(df)
    df = parse_dates(df)

    # Save cleaned CSV
    df.to_csv(OUT_FILE, index=False)
    print(f"Cleaned dataset saved to {OUT_FILE} with {len(df)} records.")

if __name__ == "__main__":
    main()
