import csv
import sys
csv.field_size_limit(sys.maxsize)

input_csv = 'merged_data_final.csv'
output_csv_with_year_lyrics = 'year_lyrics.csv'
output_csv_without_year_lyrics = 'without_year_lyrics.csv'


with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames


    columns_to_remove = ['year', 'lyrics']
    remaining_columns = [col for col in fieldnames if col not in columns_to_remove]


    with open(output_csv_with_year_lyrics, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=columns_to_remove)
        writer.writeheader()
        for row in reader:
            writer.writerow({col: row[col] for col in columns_to_remove})


    infile.seek(0)
    reader = csv.DictReader(infile)

    with open(output_csv_without_year_lyrics, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=remaining_columns)
        writer.writeheader()
        for row in reader:
            writer.writerow({col: row[col] for col in remaining_columns})