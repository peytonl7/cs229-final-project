class Model:
    def __init__(self, name, verbose):
        self.name = name
        self.verbose = verbose

    def train(self, train_path):
        raise NotImplementedError
    
    def predict(self, x):
        raise NotImplementedError
    
    def evaluate(self, eval_path):
        raise NotImplementedError