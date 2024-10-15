from models.Model import Model
from tqdm import tqdm

class NaiveBayes(Model):
    def __init__(self, verbose, n=2):
        super().__init__("Naive Bayes", verbose)

        # N-gram to use
        self.n = n
        # Trained "weights"
        self.n_grams = None
        self.p_label = [0.5, 0.5]

    def train(self, train_path: str) -> None:
        train_data = self.read_file(train_path)
        self.p_label = self.extract_label_probabilities(train_data)
        self.n_grams = self.extract_n_gram_probabilities(train_data)

    def evaluate(self, eval_path):
        eval_data = self.read_file(eval_path)
        predictions = []
        for example in tqdm(eval_data):
            predictions.append(self.predict(example))
        return predictions
        
    """
    Given the song lyrics for a year, compute the 
    Naive Bayes approximation of p(y|x) for each class in [0,1].
    Return the prediction for this example.
    """
    def predict(self, x) -> int:
        pass

    """
    Read the training data into some data structure. 
    Change the happiness index labels into a binary label
    for Naive Bayes prediction.
    """
    def read_file(self, train_path: str):
        pass

    """
    Compute the probability of each label by simple counting 
    over the training data.
    """
    def extract_label_probabilities(self, data) -> list:
        return [0.5, 0.5]

    """
    Parse data into tokens and build a dict of n-grams to their
    conditional log probabilities, given the binary label.
    e.g. ret[0]["love me"] = log(p("love me" | y=0))

    Use Laplace smoothing.
    """
    def extract_n_gram_probabilities(self, data) -> dict:
        ret = []
        return ret

