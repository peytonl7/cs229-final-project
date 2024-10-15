import argparse
import models.naive_bayes

MODELS = {
    "NB": models.naive_bayes.NaiveBayes
}

def run_experiment(model_name, train_path, eval_path, verbose):
    if model_name in MODELS:
        model = MODELS[model_name](verbose=verbose)
        model.train(train_path)
        print(model.evaluate(eval_path))

def main():
    parser = argparse.ArgumentParser(prog="run_experiment",
                                     description="Runs an experiment using given data and models.")
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-t', '--train', required=True)
    parser.add_argument('-e', '--eval', required=True)
    parser.add_argument('-v', '--verbose', default=True)
    
    args = parser.parse_args()
    run_experiment(args.model, args.train, args.eval, args.verbose)
    

if __name__ == "__main__":
    main()