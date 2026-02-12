import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# VERY IMPORTANT: show python working folder
print("Python is reading files from this folder:")
print(os.getcwd())
print("Make sure owid-covid-data.csv is inside this folder\n")


class COVID19DataTracker:

    def __init__(self):
        self.df = None
        self.processed_df = None

    # ---------------- LOAD DATA ----------------
    def load_data(self):

        file_path = "owid-covid-data.csv"

        if not os.path.exists(file_path):
            print("ERROR: Dataset not found.")
            print("Place 'owid-covid-data.csv' in the folder shown above.")
            return False

        print("Loading dataset...")
        self.df = pd.read_csv(file_path)

        print("Loaded successfully!")
        print("Rows:", self.df.shape[0])
        print("Countries:", self.df['location'].nunique())
        return True

    # ---------------- CLEAN DATA ----------------
    def clean_data(self, countries):

        df = self.df[self.df['location'].isin(countries)].copy()

        df['date'] = pd.to_datetime(df['date'])

        keep_cols = [
            'date', 'location', 'total_cases', 'new_cases',
            'total_deaths', 'new_deaths',
            'people_fully_vaccinated', 'population'
        ]

        df = df[keep_cols]

        # forward fill cumulative data
        for col in ['total_cases', 'total_deaths', 'people_fully_vaccinated']:
            df[col] = df.groupby('location')[col].fillna(method='ffill')

        df['new_cases'] = df['new_cases'].fillna(0)
        df['new_deaths'] = df['new_deaths'].fillna(0)

        self.processed_df = df
        print("Data cleaned")

    # ---------------- METRICS ----------------
    def calculate_metrics(self):

        df = self.processed_df

        df['cases_per_million'] = (df['total_cases'] / df['population']) * 1_000_000

        # safe death rate
        df['death_rate'] = df['total_deaths'] / df['total_cases']
        df['death_rate'] = df['death_rate'].replace([np.inf, -np.inf], np.nan)
        df['death_rate'] = df['death_rate'].fillna(0) * 100

        df['vaccination_progress'] = (df['people_fully_vaccinated'] / df['population']) * 100

        self.processed_df = df
        print("Metrics calculated")

    # ---------------- VISUALIZATION ----------------
    def create_visualizations(self):

        os.makedirs("outputs", exist_ok=True)

        df = self.processed_df
        latest = df.groupby('location').last().reset_index()

        plt.figure(figsize=(16,10))

        # Cases over time
        plt.subplot(2,2,1)
        for country in df['location'].unique():
            temp = df[df['location'] == country]
            plt.plot(temp['date'], temp['total_cases'], label=country)
        plt.title("Total Cases Over Time")
        plt.xticks(rotation=45)
        plt.legend(fontsize=7)

        # Top countries
        plt.subplot(2,2,2)
        top = latest.nlargest(10,'total_cases')
        sns.barplot(y=top['location'], x=top['total_cases'])
        plt.title("Top Countries by Cases")

        # Vaccination vs death
        plt.subplot(2,2,3)
        plot = latest.dropna(subset=['vaccination_progress','death_rate'])
        sns.scatterplot(data=plot, x='vaccination_progress', y='death_rate')
        plt.title("Vaccination vs Death Rate")

        # Deaths over time
        plt.subplot(2,2,4)
        for country in df['location'].unique():
            temp = df[df['location'] == country]
            plt.plot(temp['date'], temp['total_deaths'], label=country)
        plt.title("Deaths Over Time")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig("outputs/covid19_dashboard.png", dpi=300)
        plt.show()

        print("Dashboard saved in outputs/covid19_dashboard.png")

    # ---------------- INSIGHTS ----------------
    def generate_insights(self):

        latest = self.processed_df.groupby('location').last().reset_index()

        print("\n========= KEY INSIGHTS =========")

        worst = latest.loc[latest['death_rate'].idxmax()]
        print("Highest death rate:", worst['location'], f"{worst['death_rate']:.2f}%")

        best = latest.loc[latest['vaccination_progress'].idxmax()]
        print("Highest vaccination:", best['location'], f"{best['vaccination_progress']:.2f}%")

        corr = latest['vaccination_progress'].corr(latest['death_rate'])
        print("Vaccination vs death correlation:", round(corr,2))

        if corr < 0:
            print("Interpretation: Higher vaccination associated with lower death rate.")
        else:
            print("Interpretation: Weak or unclear relation.")

    # ---------------- RUN PIPELINE ----------------
    def run(self, countries):

        if not self.load_data():
            return

        self.clean_data(countries)
        self.calculate_metrics()
        self.create_visualizations()
        self.generate_insights()

        os.makedirs("outputs", exist_ok=True)
        self.processed_df.to_csv("outputs/processed_covid_data.csv", index=False)

        print("\nProcessed CSV saved in outputs/processed_covid_data.csv")


# ================= MAIN =================

if __name__ == "__main__":

    countries = [
        'United States','India','Brazil','United Kingdom',
        'France','Germany','Italy','Spain','Canada','Japan'
    ]

    tracker = COVID19DataTracker()
    tracker.run(countries)

    print("\nPROJECT COMPLETED")
