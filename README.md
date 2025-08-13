# Bird-Species-observation-analysis


## 📌 Project Overview
This project analyzes bird species observations across two distinct habitats: **forests** and **grasslands**.  
The goal is to uncover patterns in species diversity, temporal and spatial trends, and the influence of environmental factors such as temperature and humidity on bird activity.

Insights from this analysis can guide **biodiversity conservation**, **habitat management**, and **eco-tourism development**.

---

## 📂 Project Structure

.
├── data/
│ ├── Bird_Monitoring_Data_FOREST.XLSX # Raw forest habitat data
│ ├── Bird_Monitoring_Data_GRASSLAND.XLSX # Raw grassland habitat data
│ ├── cleaned_bird_data.csv # Cleaned and processed dataset
│ ├── bird_data.db # SQLite database containing processed data
│
├── clean_merge.py # Data cleaning and preprocessing script
├── eda_analysis.py # Exploratory Data Analysis script
├── save_sql.py # Script to save processed data to SQLite
├── streamlit_app.py # Interactive dashboard for data exploration
│
├── Bird_Species_Observation_Analysis_Report.docx # Full project report
├── Bird_Species_Observation_Analysis_Presentation.pptx # Presentation slides
└── README.md # Project documentation


---

## 🛠 Skills & Tools
- **Python** (Pandas, Matplotlib, Plotly, Streamlit, SQLAlchemy)
- **Data Cleaning & Preprocessing**
- **Exploratory Data Analysis (EDA)**
- **Data Visualization**
- **SQL & SQLite**
- **Microsoft Word & PowerPoint** for reporting

---

## 📊 Key Analyses Performed
1. **Temporal Analysis** – Observation trends by year and season.
2. **Spatial Analysis** – Species diversity comparison between forest and grassland habitats.
3. **Species Analysis** – Most frequently observed bird species.
4. **Environmental Impact** – Relationship between weather factors (temperature, humidity) and bird activity.
5. **Observer Analysis** – Identifying observer contribution patterns.

---

## 📈 Key Visualizations
- Observations per Year
- Observations by Season
- Species Count by Habitat Type
- Top 10 Observed Bird Species
- Temperature vs Humidity Scatter Plot

---

## 🚀 How to Run

1. **Clone this repository** (or download files).
2. Install required dependencies:
   ```bash
   pip install pandas matplotlib plotly streamlit sqlalchemy openpyxl python-docx python-pptx

---

##📜 Deliverables

Cleaned Dataset – Ready for analysis and visualization.

Word Report – Detailed analysis with insights and recommendations.

PowerPoint Presentation – Summary of findings for stakeholders.

Interactive Dashboard – Filterable and interactive charts via Streamlit.

---

## 🏆 Insights & Recommendations

Forest habitats have slightly higher bird diversity than grasslands.

Bird sightings peak in certain seasons, possibly due to migration or breeding.

Temperature and humidity influence bird observations.

Some species dominate sightings, indicating abundance or observation bias.

Recommend focusing conservation on high-diversity habitats and conducting more studies on less frequently observed species.

