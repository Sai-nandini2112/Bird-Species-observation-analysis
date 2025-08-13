import streamlit as st
import pandas as pd
import plotly.express as px

# ===== CONFIG =====
DATA_FILE = "data/cleaned_bird_data.csv"

# ===== LOAD DATA =====
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    # Ensure numeric distance
    if "distance" in df.columns:
        df["distance"] = df["distance"].astype(str).str.extract(r"(\d+\.?\d*)")[0]
        df["distance"] = pd.to_numeric(df["distance"], errors="coerce")
    return df

df = load_data()

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Bird Species Observation Dashboard", layout="wide")
st.title("🐦 Bird Species Observation Dashboard")

# ===== SIDEBAR FILTERS =====
habitats = sorted(df["habitat_type"].dropna().unique())
selected_habitats = st.sidebar.multiselect("Select Habitat Type(s)", habitats, default=habitats)

species_list = sorted(df["scientific_name"].dropna().unique())
selected_species = st.sidebar.selectbox("Select Species", ["All"] + species_list)

date_min = df["date"].min()
date_max = df["date"].max()
selected_dates = st.sidebar.date_input("Date Range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

# ===== APPLY FILTERS =====
mask = df["habitat_type"].isin(selected_habitats)
mask &= (df["date"] >= pd.to_datetime(selected_dates[0])) & (df["date"] <= pd.to_datetime(selected_dates[1]))
if selected_species != "All":
    mask &= (df["scientific_name"] == selected_species)

filtered_df = df[mask]

# ===== METRICS =====
col1, col2, col3 = st.columns(3)
col1.metric("Total Observations", len(filtered_df))
col2.metric("Unique Species", filtered_df["scientific_name"].nunique())
col3.metric("Habitats Selected", len(selected_habitats))

# ===== TOP SPECIES =====
top_species = filtered_df["scientific_name"].value_counts().reset_index()
top_species.columns = ["scientific_name", "count"]
fig_top_species = px.bar(top_species.head(20), x="scientific_name", y="count", title="Top 20 Species")
fig_top_species.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_top_species, use_container_width=True)

# ===== TEMPORAL ANALYSIS =====
temporal_counts = filtered_df.groupby(filtered_df["date"].dt.to_period("M")).size().reset_index(name="count")
temporal_counts["date"] = temporal_counts["date"].dt.to_timestamp()
fig_temporal = px.line(temporal_counts, x="date", y="count", title="Monthly Observation Trends")
st.plotly_chart(fig_temporal, use_container_width=True)


# ===== ENVIRONMENTAL ANALYSIS =====

# --- Environmental Analysis without lat/lon ---
st.subheader("Environmental Analysis")

# Clean and ensure numeric values for all relevant columns
numeric_cols = ["distance", "initial_three_min_cnt", "temperature", "humidity"]
for col in numeric_cols:
    if col in filtered_df.columns:
        filtered_df[col] = pd.to_numeric(filtered_df[col], errors="coerce")

# Drop duplicates just in case
filtered_df = filtered_df.drop_duplicates()

# -------------------- WEATHER CORRELATION --------------------
weather_vars = ["temperature", "humidity", "sky", "wind"]
if all(col in filtered_df.columns for col in weather_vars):

    # Scatter: Temperature vs Bird Count
    df_temp = filtered_df.dropna(subset=["temperature", "initial_three_min_cnt", "distance"])
    fig_temp_count = px.scatter(
        df_temp,
        x="temperature",
        y="initial_three_min_cnt",
        color="sky",
        size="distance",
        hover_data=["scientific_name", "plot_name", "observer"],
        title="Temperature vs Bird Count (Colored by Sky Condition)"
    )
    st.plotly_chart(fig_temp_count, use_container_width=True)

    # Scatter: Humidity vs Bird Count
    df_hum = filtered_df.dropna(subset=["humidity", "initial_three_min_cnt", "distance"])
    fig_humidity_count = px.scatter(
        df_hum,
        x="humidity",
        y="initial_three_min_cnt",
        color="wind",
        size="distance",
        hover_data=["scientific_name", "plot_name", "observer"],
        title="Humidity vs Bird Count (Colored by Wind Condition)"
    )
    st.plotly_chart(fig_humidity_count, use_container_width=True)

    # Boxplot: Distance by Wind Condition
    df_wind = filtered_df.dropna(subset=["wind", "distance"])
    fig_distance_wind = px.box(
        df_wind,
        x="wind",
        y="distance",
        color="wind",
        title="Observed Bird Distances by Wind Condition"
    )
    st.plotly_chart(fig_distance_wind, use_container_width=True)

else:
    st.warning("Weather data (Temperature, Humidity, Sky, Wind) is incomplete in this dataset.")

# -------------------- DISTURBANCE EFFECT --------------------
if "disturbance" in filtered_df.columns:
    df_disturbance = filtered_df.dropna(subset=["disturbance", "initial_three_min_cnt"])
    fig_disturbance = px.box(
        df_disturbance,
        x="disturbance",
        y="initial_three_min_cnt",
        color="disturbance",
        title="Effect of Disturbance on Bird Sightings"
    )
    st.plotly_chart(fig_disturbance, use_container_width=True)
else:
    st.warning("No disturbance data found.")

# -------------------- CORRELATION HEATMAP --------------------
corr_cols = ["temperature", "humidity", "distance", "initial_three_min_cnt"]
corr_cols = [col for col in corr_cols if col in filtered_df.columns]

if len(corr_cols) >= 2:
    corr_matrix = filtered_df[corr_cols].corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Between Weather Variables and Bird Metrics"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Not enough numeric data for correlation analysis.")


# ===== OBSERVER ACTIVITY =====
if "observer" in filtered_df.columns:
    obs_counts = filtered_df["observer"].value_counts().reset_index()
    obs_counts.columns = ["observer", "count"]
    fig_obs = px.bar(obs_counts.head(15), x="observer", y="count", title="Top Observers")
    st.plotly_chart(fig_obs, use_container_width=True)

# ===== CONSERVATION STATUS =====
if "pif_watchlist_status" in filtered_df.columns:
    watchlist_counts = filtered_df["pif_watchlist_status"].value_counts().reset_index()
    watchlist_counts.columns = ["status", "count"]
    fig_watchlist = px.pie(watchlist_counts, names="status", values="count", title="PIF Watchlist Status Distribution")
    st.plotly_chart(fig_watchlist, use_container_width=True)

fig_env = px.scatter(
    df,
    x="temperature",
    y="humidity",
    size=df["initial_three_min_cnt"].astype(int),  # convert True/False → 1/0
)

fig_env = px.scatter(
    df.dropna(subset=["initial_three_min_cnt"]),
    x="temperature",
    y="humidity",
    size=df["initial_three_min_cnt"].astype(int),  # convert True/False → 1/0
)

df["initial_three_min_cnt"] = df["initial_three_min_cnt"].fillna(1)  # Default bubble size

df["initial_three_min_cnt"] = pd.to_numeric(df["initial_three_min_cnt"], errors="coerce").fillna(1)



print(df.columns)


import os

# Make sure the folder exists
os.makedirs("data", exist_ok=True)

# Make sure filtered_df is not empty
if 'filtered_df' in locals() and not filtered_df.empty:
    filtered_df.to_csv("data/cleaned_bird_data.csv", index=False)
    st.success("Cleaned data saved to data/cleaned_bird_data.csv")
else:
    st.warning("No filtered data available to save.")
