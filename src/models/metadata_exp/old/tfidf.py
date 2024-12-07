from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re

data = pd.read_csv('tokenized_filtered.csv')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.strip()
    return text

data['cleaned_lyrics'] = data['lyrics'].apply(clean_text)
data['cleaned_tags'] = data['tags'].apply(clean_text)

data['text'] = data['cleaned_lyrics'] + " " + data['cleaned_tags']

vectorizer = TfidfVectorizer(max_features=300)  # Limit to 300 features
X = vectorizer.fit_transform(data['text']).toarray()

# Check the shape of the feature matrix
print(f"TF-IDF Feature Matrix Shape: {X.shape}")
