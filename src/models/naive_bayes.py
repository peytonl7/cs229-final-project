from Model import Model
from src.tokenizer.tokenizer import Tokenizer

from collections import defaultdict
import numpy as np
import csv

# Number of songs an n-gram must appear in to be counted
MIN_SONG_THRESHOLD = 3

class NaiveBayes(Model):
    def __init__(self, verbose, n=2):
        super().__init__("Naive Bayes", verbose)

        # N-gram to use
        self.n = n
        # Trained "weights"
        self.n_grams = None
        self.p_label = None
        # N-gram to index dictionary
        self.n_gram_to_ind = None

    def train(self, train_path: str) -> None:
        if self.verbose:
            print(f"Training on path: {train_path}")
        lyrics, years = self.read_file(train_path)
        if self.verbose:
            print(f"Found {len(years)} songs")
        labels = self.extract_labels(years)
        if self.verbose:
            print(f"Num 'happy' years in data: {sum(labels)}\nNum 'unhappy' years in data: {len(labels) - sum(labels)}")
        self.p_label = self.extract_label_probabilities(labels)
        self.n_grams = self.extract_n_gram_probabilities(lyrics, labels)
        if self.verbose:
            print(f"Found {self.n_grams.shape[1]} unique n-grams")
            print(self.n_grams)
        
    def evaluate(self, eval_path):
        lyrics, years = self.read_file(eval_path)
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
        song_v = np.ndarray((len(self.n_gram_to_ind)))
        n_grams = self.extract_n_grams(song)
        for n_gram in n_grams.keys():
            if n_gram in self.n_gram_to_ind.keys():
                song_v[self.n_gram_to_ind[n_gram]] += n_grams[n_gram]
        # Compute probabilities
        prob_0 = np.sum(song_v * self.n_grams[0]) + self.p_label[0]
        prob_1 = np.sum(song_v * self.n_grams[1]) + self.p_label[1]
        return 1 if prob_1 > prob_0 else 0

    """
    Read the song metadata into a list of dicts.
    Returns:
        lyrics: list of lists of tokenized lyrics for songs in dataset
        years: list of release years (strings) for songs in dataset
    """
    def read_file(self, train_path: str):
        tokenizer = Tokenizer()
        lyrics = []
        years = []
        with open(train_path, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                lyrics_fn = "data/song-lyrics/" + row[-1]
                with open(lyrics_fn, 'r') as lyrics_file:
                    tokens = tokenizer.tokenize_song_lyrics(lyrics_file.read())
                    lyrics.append(tokens)
                years.append(row[-4][-4:])
        return lyrics, years

    """
    Returns an ordered list of binary(?) labels for the data
    based on some criteria.
    """
    def extract_labels(self, years: list) -> np.ndarray:
        happiness = self.get_GSS_labels()
        # Decision boundary. Set as average happiness over all available years for now
        THRESHOLD = sum(happiness.values()) / len(happiness.keys())
        labels = []
        for year in years:
            labels.append(0 if happiness[year] < THRESHOLD else 1)
        return np.array(labels)

    """
    Compute the probability of each label by simple counting 
    over the training data.
    """
    def extract_label_probabilities(self, labels) -> list:
        p_1 = sum(labels) / len(labels)
        return [1 - p_1, p_1]
    
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
    NB = NaiveBayes(verbose=True)
    NB.train("data/song-metadata/song-metadata.csv")
    print(NB.evaluate("data/song-metadata/song-metadata-eval.csv"))