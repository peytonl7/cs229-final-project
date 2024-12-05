import csv
from collections import defaultdict

input_csv = 'GDP.csv'
output_csv = 'avg_gdp_by_year.csv'

with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

yearly_gdp = defaultdict(list)

for row in data:
    date = row['DATE']
    year = date.split('-')[0]
    gdp = float(row['GDP'])
    
    yearly_gdp[year].append(gdp)

average_gdp_by_year = {year: sum(gdps) / len(gdps) for year, gdps in yearly_gdp.items()}

with open(output_csv, mode='w', newline='') as outfile:
    fieldnames = ['YEAR', 'AVERAGE_GDP']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for year, avg_gdp in sorted(average_gdp_by_year.items()):
        writer.writerow({'YEAR': year, 'AVERAGE_GDP': avg_gdp})