# COVID-19 Data Tracker 

## Overview
This project analyzes real-world COVID-19 pandemic data using Python.
It processes country-level time-series data, calculates important health metrics, and generates visual dashboards and insights.

Dataset size: 300,000+ records across 200+ countries.


##  Project Structure

```
covid19-data-tracker/
│
├── covid19_data_tracker.py      
├── README.md           
├── requirements.txt              
│
└── outputs/
    ├── covid19_dashboard.png   
    └── covid19_processed_data.csv 
```

---
## Features
- Data cleaning and preprocessing using Pandas
- Cases per million calculation
- Death rate analysis
- Vaccination progress comparison
- Multi-country trend visualization
- Correlation analysis (vaccination vs death rate)

## Technologies Used
Python, Pandas, NumPy, Matplotlib, Seaborn
## How to Run

1) Install dependencies:
pip install -r requirements.txt

2) Download dataset:
https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv

Put the file in the same folder as covid_tracker.py

3) Run:
python covid_tracker.py

## Output
The program generates:
- covid19_dashboard.png (visual dashboard)
- processed_covid_data.csv (cleaned dataset)

## Key Insight Example
Higher vaccination does not always immediately reduce deaths due to reporting lag and demographic differences between countries.

## Dataset Source
Our World in Data COVID-19 Dataset
https://ourworldindata.org/coronavirus


##  License

This project uses publicly available data from Our World in Data.  


---


