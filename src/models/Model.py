import csv

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
    
    def get_GSS_labels(self):
        """
        Returns dict of {year: happiness index} based on GSS data.
        Responses are between 1-6 thousand per year, each indicating
        'Very Happy', 'Pretty Happy', or 'Not Very Happy'
        Years not covered found by nearest neighbor.
        """
        VERY_HAPPY_W = 3
        PRETTY_HAPPY_W = 1
        NOT_VERY_HAPPY_W = -3
        happiness = {}
        with open('./../../data/gss_happiness.csv', newline='') as file:
            reader = csv.reader(file)
            year_min, year_max = 2050, 1900
            for row in reader:
                if row[0] == "Year": continue
                year, vals = row[0], [int(row[1]), int(row[2]), int(row[3])]
                num_responses = sum(vals)
                # Compute index as weighted average of responses. Weights defined above
                happiness[year] = (VERY_HAPPY_W * vals[0] + PRETTY_HAPPY_W * vals[1] + NOT_VERY_HAPPY_W * vals[2]) / num_responses
                year_min, year_max = min(year_min, int(year)), max(year_max, int(year))
        # Interpolate years not covered by taking from last year with available data
        for year in range(year_min, year_max):
            if str(year) not in happiness.keys():
                happiness[str(year)] = happiness[str(year - 1)]
        return happiness
            