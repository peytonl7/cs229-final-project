import re

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

        # Remove line breaks
        lyric_str = re.sub(r'/', '', lyric_str)

        # Remove labels of song sections, i.e. "[Chorus]"
        lyric_str = re.sub(r'\[.*\]', '', lyric_str)

        # Remove punctuation like parentheses
        lyric_str = re.sub(r'[\(\)]', '', lyric_str)

        # Tokenize using NLTK
        tokens = lyric_str.split()

        return tokens

if __name__ == "__main__":
    tokenizer = Tokenizer()
    with open('example.txt', 'r') as file:
        data = file.read()
        print(tokenizer.tokenize_song_lyrics(data))


