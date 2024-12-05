import csv
import sys

csv.field_size_limit(sys.maxsize)

input_csv_1 = 'merged_dataa23.csv'
input_csv_2 = 'usaef.csv'
output_csv = 'merged_data_final.csv'


pres_approval = {}
with open(input_csv_2, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        year = row['YEAR']
        avg_approval = row['EF_Summary_Index']
        pres_approval[year] = avg_approval

merged_data = []
with open(input_csv_1, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['EF_Summary_Index']
    for row in reader:
        year = row['year']
        row['EF_Summary_Index'] = pres_approval.get(year, '')
        merged_data.append(row)

with open(output_csv, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)