import re
import csv
import sys
import json

csv.field_size_limit(sys.maxsize)

class Tokenizer:
    def __init__(self, to_lower=True):
        # If true, makes everything lowercase
        self.to_lower = to_lower

    """
    Takes in a string of song lyrics and strips formatting, extracting
    tokens by removing suffixes/capitalization, where applicable.
    """
    def tokenize_song_lyrics(self, lyric_str: str):
        if self.to_lower: 
            lyric_str = lyric_str.lower()

        # Remove labels of song sections, i.e. "[Chorus]"
        lyric_str = re.sub(r'\[.*?\]', '', lyric_str)

        # Remove punctuation like parentheses and line breaks
        lyric_str = re.sub(r'[\(\)\/,;:\.]', '', lyric_str)

        # Tokenize using NLTK
        tokens = lyric_str.split()

        return tokens

if __name__ == "__main__":
    tokenizer = Tokenizer()
    input_csv = 'filtered.csv'
    output_csv = 'tokenized_filtered.csv'
    
    # Read the filtered CSV file
    with open(input_csv, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        data = list(reader)
    
    # Tokenize the lyrics and replace the original lyrics with the tokenized lyrics
    for row in data:
        lyrics = row['lyrics']
        tokenized_lyrics = tokenizer.tokenize_song_lyrics(lyrics)
        row['lyrics'] = ' '.join(tokenized_lyrics)  # Join tokens into a single string
    
    # Write the updated data to a new CSV file
    with open(output_csv, mode='w', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

