import ast
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from textblob import TextBlob

"""
 - SCHEMA: Year,ISO Code 2,ISO Code 3,Countries, Economic Freedom Summary Index,Rank,Quartile,Government consumption,data,Transfers and subsidies,data,Government investment,data,Top marginal income tax rate,data,Top marginal income and payroll tax rate,data,Top marginal tax rate,State ownership of Assets,Size of Government,Area 1 Rank,Judicial independence,Impartial courts,Protection of property rights,Military interference in rule of law and politics,Integrity of the legal system,Legal enforcement of contracts,Regulatory restrictions on the sale of real property,Reliability of police,Gender Legal Rights Adjustment,Legal System & Property Rights -- Without Gender Adjustment,Legal System & Property Rights -- With Gender Adjustment,Area 2 Rank,Money growth,data,Standard deviation of inflation,data,Inflation: Most recent year,data,Freedom to own foreign currency bank accounts,Sound Money,Area 3 Rank,Revenue from trade taxes (% of trade sector),data,Mean tariff rate,data,Standard deviation of tariff rates,data,Tariffs,Non-tariff trade barriers,Compliance costs of importing and exporting,Regulatory trade barriers,Black market exchange rates,Financial openness,Capital controls,Freedom of foreigners to visit,Protection of foreign assets,Controls of the movement of capital and people,Freedom to trade internationally,Area 4 Rank,Ownership of banks,Private sector credit,Interest rate controls/negative real interest rates),Credit market regulations,Hiring regulations and minimum wage,Hiring and firing regulations,Centralized collective bargaining,Hours Regulations,Mandated cost of worker dismissal,Conscription,Foreign Labor,Labor market regulations,Regulatory Burden,Bureacracy costs,Impartial Public Administration,Tax compliance,Business regulations,Market openness,Business Permits,Distorton of the business environment,Freedom to enter markets and compete,Regulation,Area 5 Rank,World Bank Region,"World Bank Current Income Classification, 1990-Present"
 - Years this metric is relevant: 1970-2022
 - Countries include all, but for this, limit to United States (ISO Code 2 = US, ISO Code 3 = USA, Countries = United States)
 - Year (date) is a year (e.g. "2022")
"""
efotw = pd.read_csv("data/labels/efotw.csv")

"""
 - SCHEMA: X.1,% Approve
 - Years this metric is relevant: 1974-2024
 - X.1 (date) is a full month, day year (e.g. "Nov 6 2024")
"""
gallup_congress = pd.read_csv("data/labels/gallup_congress_approval.csv")

"""
 - SCHEMA: Start,End,Approve,Disapprove,Unsure
 - Years this metric is relevant: 1945-2024
 - Start (date) is a full month/day/year (e.g. "10/1/2024")
"""
gallup_pres = pd.read_csv("data/labels/gallup_pres_approval.csv")

"""
 - SCHEMA: DATE,GDP
 - Years this metric is relevant: 1947-2024
 - DATE (date) is a full month-day-year (e.g. "10-1-2024")
"""
gdp = pd.read_csv("data/labels/GDP.csv")

"""
 - SCHEMA: Year,Very Happy,Pretty Happy,Not Too Happy
 - Years this metric is relevant: 1972-2022
 - Year (date) is a year (e.g. "2022")
"""
gss_happiness = pd.read_csv("data/labels/gss_happiness.csv")

# Step 2: Clean Well-being Data
def clean_efotw_data(df):
    """
    Cleans the Economic Freedom of the World (efotw) dataset.
    
    - Filters for rows where 'ISO Code 2' is 'US' and 'ISO Code 3' is 'USA'.
    - Groups data by year and ensures only one data point per year.
    - Outputs a DataFrame with 'year' and 'Economic Freedom Summary Index'.

    Args:
        df (pd.DataFrame): Raw efotw dataset.

    Returns:
        pd.DataFrame: Cleaned dataset with 'year' and 'Economic Freedom Summary Index'.
    """
    initial_size = len(df)
    print(f"Initial efotw size: {initial_size}")
    
    # Filter for rows where ISO Code 2 is "US" and ISO Code 3 is "USA"
    df = df[(df['ISO Code 2'] == "US") & (df['ISO Code 3'] == "USA")]
    print(f"efotw after country filtering: {len(df)} rows remaining")
    
    # Select relevant columns
    df = df[['Year', 'Economic Freedom Summary Index']]
    
    # Handle missing or invalid years
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    print(f"efotw after year cleaning: {len(df)} rows remaining")
    
    # Remove duplicates and ensure one data point per year
    df = df.groupby('Year').agg({'Economic Freedom Summary Index': 'mean'}).reset_index()
    df.columns = ['year', 'value']  # Ensure consistent column names
    print(f"efotw after grouping: {len(df)} rows remaining")
    
    # Log summary
    print(f"[efotw] Dataset cleaned: {initial_size - len(df)} rows dropped, {len(df)} rows remaining.")
    return df

# Clean the efotw dataset
efotw_cleaned = clean_efotw_data(efotw)

# Save cleaned efotw data to file
efotw_cleaned.to_csv("src/models/cleaned_data/efotw_cleaned.csv", index=False)

def clean_gallup_congress_data(df):
    """
    Cleans the Gallup Congress Approval ratings dataset.
    
    - Converts the date column to a datetime object and extracts the year.
    - Groups data by year and calculates the average approval percentage for each year.
    - Outputs a DataFrame with 'year' and 'average approval percentage'.

    Args:
        df (pd.DataFrame): Raw Gallup Congress Approval dataset.

    Returns:
        pd.DataFrame: Cleaned dataset with 'year' and 'average approval percentage'.
    """
    initial_size = len(df)
    print(f"Initial Gallup Congress data size: {initial_size}")
    
    # Convert 'X.1' column to datetime to extract the year
    df['Year'] = pd.to_datetime(df['X.1'], errors='coerce').dt.year
    print(f"Gallup Congress after date conversion: {df['Year'].isna().sum()} invalid date entries")
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    
    # Remove rows with missing approval ratings
    print(f"Gallup Congress before value cleaning: {df['% Approve'].isna().sum()} missing approval values")
    df = df.dropna(subset=['% Approve'])
    
    # Ensure the approval column is numeric
    df['% Approve'] = pd.to_numeric(df['% Approve'], errors='coerce')
    df = df.dropna(subset=['% Approve'])
    
    # Group by year and calculate the average approval percentage
    df = df.groupby('Year').agg({'% Approve': 'median'}).reset_index()
    df.columns = ['year', 'value']  # Ensure consistent column names
    print(f"Gallup Congress after grouping: {len(df)} rows remaining")
    
    # Log summary
    final_size = len(df)
    print(f"[Gallup Congress] Data cleaned: {initial_size - final_size} rows dropped, {final_size} rows remaining.")
    return df

# Clean the Gallup Congress Approval data
gallup_congress_cleaned = clean_gallup_congress_data(gallup_congress)

# Save cleaned Gallup Congress data to file
gallup_congress_cleaned.to_csv("src/models/cleaned_data/gallup_congress_cleaned.csv", index=False)


def clean_gallup_pres_data(df):
    """
    Cleans the presidential approval ratings dataset.
    
    - Extracts the year from the 'Start' date column.
    - Groups data by year and calculates the median approval percentage for each year.
    - Outputs a DataFrame with 'year' and 'median_approval_percentage'.

    Args:
        df (pd.DataFrame): Raw presidential approval dataset.

    Returns:
        pd.DataFrame: Cleaned dataset with 'year' and 'median_approval_percentage'.
    """
    initial_size = len(df)
    print(f"Initial Presidential Approval data size: {initial_size}")
    
    # Convert the 'Start' column to datetime to extract the year
    df['Year'] = pd.to_datetime(df['Start'], errors='coerce').dt.year
    print(f"Presidential Approval after date conversion: {df['Year'].isna().sum()} invalid date entries")
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    
    # Remove rows with missing approval ratings
    print(f"Presidential Approval before value cleaning: {df['Approve'].isna().sum()} missing approval values")
    df = df.dropna(subset=['Approve'])
    
    # Ensure the 'Approve' column is numeric
    df['Approve'] = pd.to_numeric(df['Approve'], errors='coerce')
    df = df.dropna(subset=['Approve'])
    
    # Group by year and calculate the median approval percentage
    df = df.groupby('Year').agg({'Approve': 'median'}).reset_index()
    df.columns = ['year', 'value']  # Ensure consistent column names
    print(f"Presidential Approval after grouping: {len(df)} rows remaining")
    
    # Log summary
    final_size = len(df)
    print(f"[Presidential Approval] Data cleaned: {initial_size - final_size} rows dropped, {final_size} rows remaining.")
    return df


# Clean the Presidential Approval data
gallup_pres_cleaned = clean_gallup_pres_data(gallup_pres)

# Save cleaned Presidential Approval data to file
gallup_pres_cleaned.to_csv("src/models/cleaned_data/gallup_pres_cleaned.csv", index=False)


def clean_gdp_data(df):
    """
    Cleans and aggregates the GDP dataset.
    
    - Extracts the year from the 'DATE' column.
    - Groups data by year and calculates the median GDP for each year.
    - Outputs a DataFrame with 'year' and 'median_gdp'.

    Args:
        df (pd.DataFrame): Raw GDP dataset.

    Returns:
        pd.DataFrame: Cleaned dataset with 'year' and 'median_gdp'.
    """
    initial_size = len(df)
    print(f"Initial GDP data size: {initial_size}")
    
    # Convert the 'DATE' column to datetime to extract the year
    df['Year'] = pd.to_datetime(df['DATE'], errors='coerce').dt.year
    print(f"GDP data after date conversion: {df['Year'].isna().sum()} invalid date entries")
    df = df.dropna(subset=['Year'])  # Drop rows with invalid dates
    df['Year'] = df['Year'].astype(int)
    
    # Remove rows with missing GDP values
    print(f"GDP data before value cleaning: {df['GDP'].isna().sum()} missing GDP values")
    df = df.dropna(subset=['GDP'])
    
    # Ensure the 'GDP' column is numeric
    df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
    df = df.dropna(subset=['GDP'])
    
    # Group by year and calculate the median GDP
    df = df.groupby('Year').agg({'GDP': 'median'}).reset_index()
    df.columns = ['year', 'value']  # Ensure consistent column names
    print(f"GDP data after grouping: {len(df)} rows remaining")
    
    # Log summary
    final_size = len(df)
    print(f"[GDP Data] Data cleaned: {initial_size - final_size} rows dropped, {final_size} rows remaining.")
    return df

# Clean the GDP data
gdp_cleaned = clean_gdp_data(gdp)

# Save cleaned GDP data to file
gdp_cleaned.to_csv("src/models/cleaned_data/gdp_cleaned.csv", index=False)


def clean_happiness_data(df):
    """
    Cleans and processes the GSS happiness dataset.
    
    - Calculates the percentage of "Very Happy" responses for each year.
    - Outputs a DataFrame with 'year' and 'percent_very_happy'.

    Args:
        df (pd.DataFrame): Raw GSS happiness dataset.

    Returns:
        pd.DataFrame: Cleaned dataset with 'year' and 'percent_very_happy'.
    """
    initial_size = len(df)
    print(f"Initial happiness data size: {initial_size}")
    
    # Drop rows with missing values
    df = df.dropna()
    print(f"Happiness data after dropping missing values: {len(df)} rows remaining")

    # Ensure the columns are numeric
    df[['Year', 'Very Happy', 'Pretty Happy', 'Not Too Happy']] = df[
        ['Year', 'Very Happy', 'Pretty Happy', 'Not Too Happy']
    ].apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with any invalid data
    df = df.dropna()
    
    # Calculate the total number of respondents per year
    df['Total Responses'] = df['Very Happy'] + df['Pretty Happy'] + df['Not Too Happy']
    
    # Calculate the percentage of "Very Happy" responses
    df['percent_very_happy'] = (df['Very Happy'] / df['Total Responses']) * 100
    
    # Select only relevant columns
    df = df[['Year', 'percent_very_happy']]

    df.columns = ['year', 'value']  # Ensure consistent column names

    print(f"[Happiness Data] Processed: {len(df)} rows remaining, {initial_size - len(df)} rows dropped.")
    return df

# Clean the happiness data
happiness_cleaned = clean_happiness_data(gss_happiness)

# Save cleaned happiness data to file
happiness_cleaned.to_csv("src/models/cleaned_data/gss_happiness_cleaned.csv", index=False)