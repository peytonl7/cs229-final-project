import csv
import sys
csv.field_size_limit(sys.maxsize)

input_csv = 'merged_data_final.csv'
output_csv = 'cleaned_tags.csv'

with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

for row in data:
    row['tags'] = row['tags'].replace(',', '')

with open(output_csv, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(data)