import pandas as pd
import plotly.express as px

DATA_FILE = "data/cleaned_bird_data.csv"

def temporal_analysis(df):
    yearly = df.groupby("year").size().reset_index(name="count")
    fig = px.line(yearly, x="year", y="count", title="Observations per Year")
    fig.show()

    seasonal = df.groupby("season").size().reset_index(name="count")
    fig2 = px.bar(seasonal, x="season", y="count", title="Observations by Season")
    fig2.show()

def spatial_analysis(df):
    habitat_counts = df.groupby("habitat_type")["scientific_name"].nunique().reset_index(name="species_count")
    fig = px.bar(habitat_counts, x="habitat_type", y="species_count", title="Species Count by Habitat")
    fig.show()

    plot_counts = df.groupby("plot_name")["scientific_name"].nunique().reset_index(name="species_count")
    fig2 = px.bar(plot_counts, x="plot_name", y="species_count", title="Species Count by Plot")
    fig2.show()

def species_analysis(df):
    species_top = df["scientific_name"].value_counts().reset_index()
    species_top.columns = ["scientific_name", "count"]
    fig = px.bar(species_top.head(20), x="scientific_name", y="count", title="Top 20 Observed Species")
    fig.show()

def environmental_analysis(df):
    fig = px.scatter(df, x="temperature", y="humidity", size="distance", color="habitat_type", title="Weather Conditions")
    fig.show()

def observer_analysis(df):
    obs_counts = df["observer"].value_counts().reset_index()
    obs_counts.columns = ["observer", "count"]
    fig = px.bar(obs_counts, x="observer", y="count", title="Observations per Observer")
    fig.show()

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    temporal_analysis(df)
    spatial_analysis(df)
    species_analysis(df)
    environmental_analysis(df)
    observer_analysis(df)

df['distance_m'] = df['distance'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
df['distance_m'] = pd.to_numeric(df['distance_m'], errors='coerce')


fig = px.scatter(df, x="temperature", y="humidity", size="distance_m", color="habitat_type", title="Weather Conditions")
