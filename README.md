# Armenia Accident Risk & Cost Dashboard

A prototype interactive dashboard for exploring car‐accident trends, high‐risk areas, and cost distributions in Armenia.

---

## Project Structure

```
DataVizProject/
├── .venv/                   
├── data/
│   ├── raw/         # Original Excel data
│   └── processed/   # Cleaned Parquet data
├── notebooks/       # Exploratory analyses
│   ├── 01_data_overview.ipynb
│   ├── 02_temporal_analysis.ipynb
│   ├── 03_demographic_analysis.ipynb
│   ├── 04_weather_analysis.ipynb
│   └── 05_vehicle_cost_analysis.ipynb
├── reports/
│   └── figures/     # Exported static charts
├── src/             # Streamlit interactive dashboard
│   ├── data_processing.py   # Load & clean pipeline
│   ├── visualization.py     # Plotly chart functions
│   └── dashboard_app.py     # Streamlit app entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

1. **Clone this repository**  
   ```bash
   git clone https://github.com/<your-username>/accident-dashboard-armenia.git
   cd accident-dashboard-armenia
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run exploratory notebooks**  
   ```bash
   jupyter lab notebooks/01_data_overview.ipynb
   ```

5. **Launch the interactive dashboard**  
   ```bash
   streamlit run src/dashboard_app.py
   ```
---

## Analysis Notebooks

1. **Data Overview** (`01_data_overview.ipynb`)
   - Initial data inspection and quality assessment
   - Basic statistics and missing value analysis

2. **Temporal Analysis** (`02_temporal_analysis.ipynb`)
   - Time series decomposition of accident patterns
   - Seasonal trends
   - Peak hour identification

3. **Demographic Analysis** (`03_demographic_analysis.ipynb`)
   - Age and gender distribution of drivers
   - Driver experience correlations

4. **Weather Analysis** (`04_weather_analysis.ipynb`)
   - Weather conditions impact on accidents
   - Precipitation effects

5. **Vehicle Cost Analysis** (`05_vehicle_cost_analysis.ipynb`)
   - Repair cost distributions by car brand
   - Age of vehicle vs repair costs

---

## Dashboard Features

- **Date range picker**: zoom in on any period between 2018–2020  
- **Region & Car Brand**: “Select all” / “Clear” buttons + multi‐select  
- **Hour slider**: filter by time of day (0–23)  
- **Gender selector**  
- **Three main charts** (stacked vertically):  
  1. **Accidents over time** (weekly by default)  
  2. **Accidents by hour of day** histogram  
  3. **Repair cost distribution** (box‐plot of top 10 brands)  

Use the sidebar controls to explore how accident counts and costs vary by geography, time, vehicle type, and driver demographics.

---

*Tariel Hakobyan & Norayr Sukiasyan, Spring 2025 – American University of Armenia*  
