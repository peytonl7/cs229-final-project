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
# Load lyrics and metadata
lyrics_metadata_parts = [
    "data/processed-hot-100-with-lyrics-metadata-part-1.csv",
    "data/processed-hot-100-with-lyrics-metadata-part-2.csv",
    "data/processed-hot-100-with-lyrics-metadata-part-3.csv"
]
lyrics_metadata = pd.concat(
    [pd.read_csv(file) for file in lyrics_metadata_parts], 
    ignore_index=True
)

# Step 1: Clean lyrics data
def parse_metadata(metadata_str):
    try:
        return ast.literal_eval(metadata_str) if isinstance(metadata_str, str) else {}
    except Exception as e:
        return {}

# Extract and clean metadata
lyrics_metadata['metadata'] = lyrics_metadata['metadata'].apply(parse_metadata)
lyrics_metadata['release_date'] = lyrics_metadata['metadata'].apply(lambda x: x.get('Release Date'))
lyrics_metadata['genre'] = lyrics_metadata['metadata'].apply(lambda x: x.get('Tags', [None])[0])

# Calculate sentiment scores
lyrics_metadata['sentiment'] = lyrics_metadata['lyrics'].apply(
    lambda x: TextBlob(str(x)).sentiment.polarity
)

"""
Uncomment this to speed up (no sentiment analysis)
lyrics_metadata['sentiment'] = 0
"""

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

# Step 2: Combine data by year
# Load cleaned well-being data
efotw_cleaned = pd.read_csv("src/models/cleaned_data/efotw_cleaned.csv")
gallup_congress_cleaned = pd.read_csv("src/models/cleaned_data/gallup_congress_cleaned.csv")
gallup_pres_cleaned = pd.read_csv("src/models/cleaned_data/gallup_pres_cleaned.csv")
gdp_cleaned = pd.read_csv("src/models/cleaned_data/gdp_cleaned.csv")
gss_happiness_cleaned = pd.read_csv("src/models/cleaned_data/gss_happiness_cleaned.csv")

def combine_data_by_year(lyrics_df, wellbeing_df):
    lyrics_df['release_year'] = pd.to_datetime(lyrics_df['release_date'], errors='coerce').dt.year
    combined = pd.merge(lyrics_df, wellbeing_df, left_on='release_year', right_on='year', how='inner')
    return combined

# Step 3: Predictive Modeling
def train_predictive_model(lyrics_df, wellbeing_df, target_metric, use_metadata):
    combined = combine_data_by_year(lyrics_df, wellbeing_df)
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
def plot_sentiment_and_wellbeing_trends(lyrics_df, metrics_data):
    # Prepare sentiment data
    lyrics_df['release_year'] = pd.to_datetime(lyrics_df['release_date'], errors='coerce').dt.year
    sentiment_by_year = lyrics_df.groupby('release_year')['sentiment'].mean().reset_index()
    sentiment_by_year.columns = ['year', 'sentiment']

    # Normalize a series
    def normalize_series(series):
        return (series - series.min()) / (series.max() - series.min())

    # Initialize a DataFrame for plotting
    trend_data = sentiment_by_year.copy()
    trend_data['sentiment'] = normalize_series(trend_data['sentiment'])

    # Ensure 'year' column has no missing values before generating the range
    valid_years = trend_data['year'].dropna().astype(int)
    all_years = pd.Series(range(max(1940, valid_years.min()), min(2024, valid_years.max()) + 1), name='year')

    # Expand trend_data to include all years within the range
    trend_data = pd.merge(all_years, trend_data, on='year', how='left')

    # Merge each well-being metric into the trend_data DataFrame and interpolate missing values
    for metric_df, metric_name in metrics_data:
        # Rename the value column for clarity
        metric_df = metric_df.rename(columns={'value': f'value_{metric_name}'})
        # Merge with trend_data on the year
        trend_data = pd.merge(trend_data, metric_df[['year', f'value_{metric_name}']], on='year', how='left')
        # Interpolate missing values for this metric
        trend_data[f'value_{metric_name}'] = trend_data[f'value_{metric_name}'].interpolate(method='linear')

    # Normalize the well-being values and filter out rows with missing data
    for _, metric_name in metrics_data:
        column_name = f'value_{metric_name}'
        trend_data[column_name] = normalize_series(trend_data[column_name])

    # Clip data to the desired year range (1940–2024)
    trend_data = trend_data[(trend_data['year'] >= 1940) & (trend_data['year'] <= 2024)]

    # Plot the trends
    plt.figure(figsize=(14, 8))
    plt.plot(trend_data['year'], trend_data['sentiment'], label='Sentiment', linewidth=2, color='blue')

    for _, metric_name in metrics_data:
        plt.plot(trend_data['year'], trend_data[f'value_{metric_name}'], label=metric_name, linewidth=2)

    plt.title("Sentiment vs Well-being Metrics Over Time (1940–2024)", fontsize=16)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Normalized Values", fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


# Define the list of metrics and their names
metrics_data = [
    (efotw_cleaned, "Economic Freedom Index"),
    (gallup_congress_cleaned, "Congress Approval"),
    (gallup_pres_cleaned, "Presidential Approval"),
    (gdp_cleaned, "GDP"),
    (gss_happiness_cleaned, "Happiness Index")
]

plot_sentiment_and_wellbeing_trends(lyrics_metadata, metrics_data)