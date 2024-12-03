from src.models.Model import Model
from src.tokenizer.tokenizer import Tokenizer

from collections import defaultdict
import numpy as np
import math
import pandas as pd

# Number of songs an n-gram must appear in to be counted
MIN_SONG_THRESHOLD = 5

# Max number of words for a song to be included
MAX_WORD_THRESHOLD = 1600

class NaiveBayes(Model):
    def __init__(self, verbose, n=2, labels="hap"):
        super().__init__("Naive Bayes", verbose, labels)

        # N-gram to use
        self.n = n
        # Trained "weights"
        self.n_grams = None
        self.p_label = None
        # N-gram to index dictionary
        self.n_gram_to_ind = None

    def train(self, train_data: str) -> None:
        """
        Train a Naive Bayes classifier by computing conditional probabilities 
        of n-grams based on lyrics data.
        """
        # TODO: Filter data for long lyrics and wrong years
        lyrics, years = self.filter(train_data[["lyrics", "chart_instances"]])
        # Train on three parts of input data
        if self.verbose:
            print(f"Found {len(years)} valid songs")
        labels = self.extract_labels(years)
        if self.verbose:
            print(f"Num 'high' years in data: {sum(labels)}\nNum 'low' years in data: {len(labels) - sum(labels)}")
        self.p_label = self.extract_label_probabilities(labels)
        self.n_grams = self.extract_n_gram_probabilities(lyrics, labels)
        if self.verbose:
            print(f"Found {self.n_grams.shape[1]} unique n-grams\n")
        
    def evaluate(self, eval_data):
        """
        Predict from a dataset and print the results.
        """
        lyrics, years = self.filter(eval_data[["lyrics", "chart_instances"]])
        if self.verbose:
            print(f"Found {len(years)} valid songs")
        labels = self.extract_labels(years)
        predictions = []
        for example in lyrics:
            predictions.append(self.predict(example))
        correct = 0
        for i in range(len(predictions)):
            correct += 1 if predictions[i] == labels[i] else 0
        if self.verbose:
            print(f"Accuracy on eval data: {correct / len(predictions)}")
        return predictions
        
    """
    Given the song lyrics for a year, compute the 
    Naive Bayes approximation of p(y|x) for each class in [0,1].
    Return the prediction for this example.
    """
    def predict(self, song) -> int:
        # Generate matrix of n-gram counts from song
        song_v = np.zeros((len(self.n_gram_to_ind)))
        n_grams = self.extract_n_grams(song)
        for n_gram in n_grams.keys():
            if n_gram in self.n_gram_to_ind.keys():
                song_v[self.n_gram_to_ind[n_gram]] += n_grams[n_gram]
        # Compute probabilities
        prob_0 = np.sum(song_v * self.n_grams[0]) + self.p_label[0]
        prob_1 = np.sum(song_v * self.n_grams[1]) + self.p_label[1]
        return 1 if prob_1 > prob_0 else 0

    """
    Filter the song data by relevant year (to label) and length of lyrics.
    Returns:
        lyrics: list of lists of tokenized lyrics for songs in dataset
        years: list of release years (strings) for songs in dataset
    """
    def filter(self, df: pd.DataFrame):
        tokenizer = Tokenizer()
        df = df.loc[df["lyrics"] != "Error"]
        df["lyrics"] = df["lyrics"].apply(tokenizer.tokenize_song_lyrics)
        df["lyrics_len"] = df["lyrics"].apply(len)
        df["years"] = df["chart_instances"].str.extract(r'(\d\d\d\d)', expand=False).astype(int)
        df = df[(df["lyrics_len"] <= MAX_WORD_THRESHOLD) & (df["years"] >= self.year_range[0]) & (df["years"] <= self.year_range[1])]
        return list(df["lyrics"]), list(df["years"].astype(str))

    """
    Returns an ordered list of binary(?) labels for the data
    based on some criteria.
    """
    def extract_labels(self, years: list) -> np.ndarray:
        # Decision boundary. Set as average over all available years for now
        THRESHOLD = sum(self.labels_by_year.values()) / len(self.labels_by_year.keys())
        labels = []
        for year in years:
            labels.append(0 if self.labels_by_year[year] < THRESHOLD else 1)
        return np.array(labels)

    """
    Compute the probability of each label by simple counting 
    over the training data.
    """
    def extract_label_probabilities(self, labels) -> list:
        p_1 = sum(labels) / len(labels)
        return [math.log(1 - p_1), math.log(p_1)]
    
    """
    Given a list of tokens, find n-gram counts and return as a dictionary.
    """
    def extract_n_grams(self, song):
        n_grams = defaultdict(int)
        for i in range(len(song) + 1 - self.n):
            n_gram = " ".join(song[i:i+self.n])
            n_grams[n_gram] += 1
        return n_grams

    """
    Parse data into tokens and build a dict of n-grams to their
    conditional log probabilities, given the binary label.
    e.g. ret[0]["love me"] = log(p("love me" | y=0))
    """
    def extract_n_gram_probabilities(self, songs, labels) -> np.ndarray:
        # Generate n_gram_to_ind
        counts = defaultdict(int)
        n_grams_dict = defaultdict(dict)
        for i in range(len(songs)):
            n_grams = self.extract_n_grams(songs[i])
            n_grams_dict[i] = n_grams
            for n_gram in n_grams:
                counts[n_gram] += 1
        
        self.n_gram_to_ind = {}
        i = 0
        for n_gram in counts.keys():
            if counts[n_gram] >= MIN_SONG_THRESHOLD:
                self.n_gram_to_ind[n_gram] = i
                i += 1

        # Generate matrix of counts of n-grams
        arr = np.ndarray((len(songs), len(self.n_gram_to_ind)))
        for i in range(len(songs)):
            for n_gram in n_grams_dict[i].keys():
                if n_gram in self.n_gram_to_ind.keys():
                    arr[i, self.n_gram_to_ind[n_gram]] += n_grams_dict[i][n_gram]

        # Compute log probabilities
        log_prob_n_grams = np.zeros((2, arr.shape[1]))
        for class_label in [0, 1]:
            class_counts = arr[np.where(np.array(labels) == class_label)[0], :]
            log_prob_n_grams[class_label] = np.log((1 + np.sum(class_counts, axis=0)) / (arr.shape[1] + np.sum(class_counts)))
        return log_prob_n_grams
        

if __name__ == "__main__":
    NB = NaiveBayes(verbose=True, labels="hap")
    NB.train("data/processed-hot-100-with-lyrics-metadata.csv")