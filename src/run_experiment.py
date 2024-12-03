import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.models import naive_bayes

MODELS = {
    "NB": naive_bayes.NaiveBayes
}

def run_experiment(model_name, data_path, verbose, labels):
    # np.random.seed(229)
    data = None
    for i in range(1, 4):
        path = f'{data_path}-part-{i}.csv'
        if data is None:
            data = pd.read_csv(path)
        else:
            pd.concat([data, pd.read_csv(path)])
    train_data, eval_data = train_test_split(data, test_size=0.2)

    if model_name in MODELS:
        model = MODELS[model_name](verbose=verbose, labels=labels)
        model.train(train_data)
        model.evaluate(eval_data)

def main():
    parser = argparse.ArgumentParser(prog="run_experiment",
                                     description="Runs an experiment using given data and models.")
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-d', '--data', default="data/processed-hot-100-with-lyrics-metadata")
    parser.add_argument('-v', '--verbose', default=True)
    parser.add_argument('-l', '--labels', default="gdp")
    
    args = parser.parse_args()
    run_experiment(args.model, args.data, args.verbose, args.labels)
    

if __name__ == "__main__":
    main()