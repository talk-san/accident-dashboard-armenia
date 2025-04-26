# Armenia Accident Risk & Cost Dashboard

A prototype interactive dashboard for exploring car-accident trends, high-risk areas, and cost distributions in Armenia.

## Project Structure

```
DataVizProject/
├── .venv/                   
├── data/
│   ├── raw/                 
│   └── processed/           
├── notebooks/               
├── src/                     
└── reports/                 
```

## Getting Started

1. **Clone this repository**  
2. **Create and activate your virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Run exploratory analysis**  
   ```bash
   jupyter lab notebooks/01_data_overview.ipynb
   ```
5. **Launch the dashboard**  
   ```bash
   streamlit run src/dashboard_app.py
   ```
