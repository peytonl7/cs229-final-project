import csv
from collections import defaultdict

# Years for data of certain types of label
YEAR_RANGES = {
    "hap": [1972, 2022],
    "ef": [1970, 2022],
    "ca": [1974, 2024],
    "pa": [1945, 2024],
    "gdp": [1947, 2024]
}

class Model:
    def __init__(self, name, verbose, labels):
        self.name = name
        self.verbose = verbose
        if labels == "hap":
            self.labels_by_year = self.get_HAP_labels()
        if labels == "ef":
            self.labels_by_year = self.get_EF_labels()
        if labels == "ca":
            self.labels_by_year = self.get_CA_labels()
        if labels == "pa":
            self.labels_by_year = self.get_PA_labels()
        if labels == "gdp":
            self.labels_by_year = self.get_GDP_labels()
        self.year_range = YEAR_RANGES[labels]

    def train(self, train_path):
        raise NotImplementedError
    
    def predict(self, x):
        raise NotImplementedError
    
    def evaluate(self, eval_path):
        raise NotImplementedError
    
    def get_HAP_labels(self):
        """
        Returns dict of {year: happiness index} based on GSS data.
        Responses are between 1-6 thousand per year, each indicating
        'Very Happy', 'Pretty Happy', or 'Not Very Happy'.
        Years not covered computed by linear interpolation.
        Goes to 1972.
        """
        VERY_HAPPY_W = 3
        PRETTY_HAPPY_W = 1
        NOT_VERY_HAPPY_W = -3
        happiness = {}
        with open('data/labels/gss_happiness.csv', newline='') as file:
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
        prev_year = None
        for year in sorted(happiness.keys()):
            if prev_year:
                steps = int(year) - int(prev_year) - 1
                step = happiness[str(year)] - happiness[str(prev_year)]
                for i in range(1, steps + 1):
                    happiness[str(int(prev_year) + i)] = happiness[year] + step * i
            prev_year = year
        return happiness
            
    
    def get_EF_labels(self, country="USA"):
        """
        Returns dict of {year: economic freedom index} based on EFOTW data.
        Years not covered computed by linear interpolation.
        Goes to 1970.

        Params:
            country: str of ISO Code 3 for the desired country. Default is USA
        """
        economic_freedom = {}
        with open('data/labels/efotw.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "Year" or row[2] != country: continue   # Skip header and non-country rows
                economic_freedom[row[0]] = float(row[4])
        
        prev_year = None
        for year in sorted(economic_freedom.keys()):
            if prev_year:
                steps = int(year) - int(prev_year) - 1
                step = economic_freedom[str(year)] - economic_freedom[str(prev_year)]
                for i in range(1, steps + 1):
                    economic_freedom[str(int(prev_year) + i)] = economic_freedom[year] + step * i
            prev_year = year
        
        return economic_freedom
    
    def get_CA_labels(self):
        """
        Returns dict of {year: congressional approval} based on Gallup poll data.
        Approval by year computed as average of all polls that year.
        Years not covered computed by linear interpolation.
        Goes to 1974.
        """
        ca = defaultdict(list)
        with open('data/labels/gallup_congress_approval.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "\ufeffX.1": continue   # Skip header
                ca[row[0][-4:]].append(int(row[1]))

        congressional_approval = {}
        for year in ca.keys():
            congressional_approval[year] = sum(ca[year]) / len(ca[year])

        prev_year = None
        for year in sorted(congressional_approval.keys()):
            if prev_year:
                steps = int(year) - int(prev_year) - 1
                step = congressional_approval[str(year)] - congressional_approval[str(prev_year)]
                for i in range(1, steps + 1):
                    congressional_approval[str(int(prev_year) + i)] = congressional_approval[year] + step * i
            prev_year = year

        return congressional_approval
    
    def get_PA_labels(self):
        """
        Returns dict of {year: presidential approval} based on Gallup poll data.
        Approval by year computed as average of all polls that year.
        Goes to 1945.
        """
        pa = defaultdict(list)
        with open('data/labels/gallup_pres_approval.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "Start": continue   # Skip header
                pa[row[0][-4:]].append(int(row[2]))
            
        pres_approval = {}
        for year in pa.keys():
            pres_approval[year] = sum(pa[year]) / len(pa[year])

        return pres_approval
    
    def get_GDP_labels(self):
        """
        Returns dict of {year: GDP} based on Federal Reserve data.
        GDP by year computed as average of all points that year.
        Goes to 1947.
        """
        gdp = defaultdict(list)
        with open('data/labels/GDP.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "DATE": continue   # Skip header
                gdp[row[0][:4]].append(float(row[1]))

        gross_dom_prod = {}
        for year in gdp.keys():
            gross_dom_prod[year] = sum(gdp[year]) / len(gdp[year])

        return gross_dom_prod