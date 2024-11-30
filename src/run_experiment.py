import argparse
from src.models import naive_bayes

MODELS = {
    "NB": naive_bayes.NaiveBayes
}

def run_experiment(model_name, train_path, eval_path, verbose, labels):
    if model_name in MODELS:
        model = MODELS[model_name](verbose=verbose, labels=labels)
        model.train(train_path)
        model.evaluate(eval_path)

def main():
    parser = argparse.ArgumentParser(prog="run_experiment",
                                     description="Runs an experiment using given data and models.")
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-t', '--train', default="data/processed-hot-100-with-lyrics-metadata.csv")
    parser.add_argument('-e', '--eval', default="data/processed-hot-100-with-lyrics-metadata.csv")
    parser.add_argument('-v', '--verbose', default=True)
    parser.add_argument('-l', '--labels', default="hap")
    
    args = parser.parse_args()
    run_experiment(args.model, args.train, args.eval, args.verbose, args.labels)
    

if __name__ == "__main__":
    main()