import csv
import sys
from collections import defaultdict

csv.field_size_limit(sys.maxsize)

input_csv = 'tokenized_filtered.csv'
output_csv = 'yearly_aggregated.csv'

with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

yearly_data = defaultdict(lambda: {'lyrics': [], 'tags': set()})

for row in data:
    date = row['date']
    year = date.split('-')[0]
    lyrics = row['lyrics']
    tags = row['tags'].split(', ')

    yearly_data[year]['lyrics'].append(lyrics)
    yearly_data[year]['tags'].update(tags)

sorted_years = sorted(yearly_data.keys())

with open(output_csv, mode='w', newline='') as outfile:
    fieldnames = ['year', 'lyrics', 'tags']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for year in sorted_years:
        content = yearly_data[year]
        writer.writerow({
            'year': year,
            'lyrics': ' '.join(content['lyrics']),
            'tags': ', '.join(content['tags'])
        })