import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data/cleaned_bird_data.csv", parse_dates=["date"])
engine = create_engine("sqlite:///data/bird_data.db")
df.to_sql("observations", engine, if_exists="replace", index=False)
print("Data saved to SQLite database.")
