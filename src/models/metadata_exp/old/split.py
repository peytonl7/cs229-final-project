import csv
import sys

csv.field_size_limit(sys.maxsize)

input_csv = 'cleaned_tags.csv'
train_csv = 'train.csv'
val_csv = 'val.csv'
test_csv = 'test.csv'

with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

def split_string(s):
    length = len(s)
    train_end = int(0.8 * length)
    val_end = int(0.9 * length)
    return s[:train_end], s[train_end:val_end], s[val_end:]

train_data = []
val_data = []
test_data = []

for row in data:
    train_row = row.copy()
    val_row = row.copy()
    test_row = row.copy()

    train_lyrics, val_lyrics, test_lyrics = split_string(row['lyrics'])
    train_tags, val_tags, test_tags = split_string(row['tags'])

    train_row['lyrics'] = train_lyrics
    val_row['lyrics'] = val_lyrics
    test_row['lyrics'] = test_lyrics

    train_row['tags'] = train_tags
    val_row['tags'] = val_tags
    test_row['tags'] = test_tags

    train_data.append(train_row)
    val_data.append(val_row)
    test_data.append(test_row)

with open(train_csv, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(train_data)

with open(val_csv, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(val_data)

with open(test_csv, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(test_data)