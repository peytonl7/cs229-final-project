import ast
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from textblob import TextBlob

# Initialize error logging
error_log_path = "data/dropped_points_log.txt"
with open(error_log_path, "w") as f:
    f.write("Dropped Data Points Log:\n\n")

def log_dropped_data(song, performer, reason):
    with open(error_log_path, "a") as f:
        f.write(f"{song}, {performer} - {reason}\n")

# Step 0: Load data
"""
 - SCHEMA: song,performer,chart_instances,time_on_chart,peak_position,worst_position,lyrics,metadata
 - Here, lyrics are a single string, with line breaks being denoted by "/".
 - Here, metadata is a dictionary with keys of 'Producer', 'Writers' (list), 'Release Date', and 'Tags' (list).
"""
lyrics_metadata = pd.read_csv("data/processed-hot-100-with-lyrics-metadata.csv")

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

# Step 1: Metadata Extraction + Cleaning
def parse_metadata(metadata_str):
    try:
        return ast.literal_eval(metadata_str) if isinstance(metadata_str, str) else {}
    except Exception as e:
        return {}

# Apply metadata parsing and extract relevant fields
lyrics_metadata['metadata'] = lyrics_metadata['metadata'].apply(parse_metadata)
lyrics_metadata['release_date'] = lyrics_metadata['metadata'].apply(lambda x: x.get('Release Date'))
lyrics_metadata['genre'] = lyrics_metadata['metadata'].apply(lambda x: x.get('Tags', [None])[0])

# Calculate sentiment scores
lyrics_metadata['sentiment'] = lyrics_metadata['lyrics'].apply(
    lambda x: TextBlob(str(x)).sentiment.polarity
)

# Drop invalid data points and log them
initial_size = len(lyrics_metadata)
for index, row in lyrics_metadata.iterrows():
    reasons = []
    if pd.isna(row['lyrics']) or pd.isna(row['release_date']) or pd.isna(row['metadata']):
        reasons.append("Missing required fields")
    if isinstance(row['genre'], str) and "Non-Music" in row['genre']:
        reasons.append("Non-Music genre")
    if len(str(row['lyrics']).split()) > 1000:
        reasons.append("Lyrics exceed word limit")
    if reasons:
        log_dropped_data(row['song'], row['performer'], "; ".join(reasons))
        lyrics_metadata.drop(index, inplace=True)

final_size = len(lyrics_metadata)
print(f"Lyrics metadata cleaned: {initial_size - final_size} data points dropped, {final_size} remaining.")

# Step 2: Clean Well-being Data
def clean_wellbeing_data(df, year_column, value_column, start_year, end_year, df_name):
    initial_size = len(df)
    print(f"Initial {df_name} size: {initial_size}")

    # Convert year_column to numeric
    df[year_column] = pd.to_datetime(df[year_column], errors='coerce').dt.year
    print(f"{df_name} after year conversion: {df[year_column].isna().sum()} invalid year entries")

    # Handle missing values for value_column
    print(f"{df_name} before value imputation: {df[value_column].isna().sum()} missing values")
    df[value_column] = df[value_column].interpolate(method='linear', limit_direction='both')
    print(f"{df_name} after value imputation: {df[value_column].isna().sum()} missing values")

    # Filter rows based on the year range
    df = df[(df[year_column] >= start_year) & (df[year_column] <= end_year)]
    print(f"{df_name} after year range filtering: {len(df)} remaining rows")

    # If no rows remain, return an empty DataFrame with consistent columns
    if df.empty:
        print(f"Warning: {df_name} is empty after year filtering.")
        return pd.DataFrame(columns=['year', 'value'])

    # Group and aggregate
    df = df.groupby(year_column).agg({value_column: 'mean'}).reset_index()
    df.columns = ['year', 'value']  # Ensure consistent column names
    print(f"{df_name} after grouping: {len(df)} remaining rows")

    # Log summary
    final_size = len(df)
    print(f"[{df_name}] Well-being data cleaned: {initial_size - final_size} data points dropped, {final_size} remaining.")
    return df


# Clean each dataset
efotw_cleaned = clean_wellbeing_data(efotw, 'Year', 'Economic Freedom Summary Index', 1970, 2022, 'efotw')
gallup_congress_cleaned = clean_wellbeing_data(gallup_congress, 'X.1', '% Approve', 1974, 2024, 'gallup_congress')
gallup_pres_cleaned = clean_wellbeing_data(gallup_pres, 'Start', 'Approve', 1945, 2024, 'gallup_pres')
gdp_cleaned = clean_wellbeing_data(gdp, 'DATE', 'GDP', 1947, 2024, 'gdp')
gss_happiness_cleaned = clean_wellbeing_data(gss_happiness, 'Year', 'Very Happy', 1972, 2022, 'gss_happiness')


# Step 3: Predictive Modeling
def train_predictive_model(lyrics_df, wellbeing_df, target_metric, use_metadata):
    lyrics_df['release_year'] = pd.to_datetime(lyrics_df['release_date'], errors='coerce').dt.year
    combined = pd.merge(lyrics_df, wellbeing_df, left_on='release_year', right_on='year', how='inner')
    
    if use_metadata:
        features = combined[['sentiment', 'genre', 'chart_instances', 'peak_position', 'time_on_chart']]
        features = pd.get_dummies(features, drop_first=True)
    else:
        features = combined[['sentiment']]
    
    target = combined['value']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    print(f"Model Performance for {target_metric} {'with metadata' if use_metadata else 'without metadata'}:")
    print("MSE:", mean_squared_error(y_test, predictions))
    print("R2 Score:", r2_score(y_test, predictions))
    return model

# Train models for each well-being metric with and without metadata
metrics = [
    (efotw_cleaned, "Economic Freedom Index"),
    (gallup_congress_cleaned, "Congress Approval"),
    (gallup_pres_cleaned, "Presidential Approval"),
    (gdp_cleaned, "GDP"),
    (gss_happiness_cleaned, "Happiness")
]
for metric, name in metrics:
    train_predictive_model(lyrics_metadata, metric, name, use_metadata=False)
    train_predictive_model(lyrics_metadata, metric, name, use_metadata=True)


# Step 4: Sentiment-Well-being Trends
def analyze_sentiment_trends(lyrics_df, wellbeing_df, target_metric):
    lyrics_df['release_year'] = pd.to_datetime(lyrics_df['release_date'], errors='coerce').dt.year
    combined = pd.merge(lyrics_df[['release_year', 'sentiment']], wellbeing_df, 
                        left_on='release_year', right_on='year', how='inner')
    plt.figure(figsize=(10, 6))
    plt.plot(combined['year'], combined['sentiment'], label='Sentiment')
    plt.plot(combined['year'], combined['value'], label=target_metric)
    plt.legend()
    plt.title(f"Sentiment vs. {target_metric}")
    plt.xlabel("Year")
    plt.ylabel("Values")
    plt.show()

# Analyze sentiment trends for each well-being metric
for metric, name in metrics:
    analyze_sentiment_trends(lyrics_metadata, metric, name)