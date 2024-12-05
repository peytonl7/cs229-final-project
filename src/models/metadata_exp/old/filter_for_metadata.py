import csv
import sys
import json

csv.field_size_limit(sys.maxsize)

original_csv = 'processed-hot-100-with-lyrics-metadata.csv'
with open(original_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

required_columns = ['song', 'performer', 'chart_instances', 'metadata', 'lyrics']

highest_chart_data = {}
for row in data:
    if any(col not in row or not row[col] for col in required_columns):
            print(f"Skipping row with missing columns: {row}")
            continue

    song = row['song']
    performer = row['performer']
    chart_instances = json.loads(row['chart_instances'])
    lyrics = row['lyrics']
    metadata_str = row['metadata']
    if metadata_str:
        try:
            metadata = json.loads(metadata_str.replace("'", '"'))
        except json.JSONDecodeError:
            print(f"Skipping row with invalid metadata: {metadata_str}")
            continue
    else:
        metadata = {}
    
    highest_chart_position = float('inf')
    highest_chart_date = None
    
    for instance in chart_instances:
        chart_position = instance['chart_position']
        chart_date = instance['chart_date']
        
        if chart_position < highest_chart_position:
            highest_chart_position = chart_position
            highest_chart_date = chart_date
    tags = metadata.get('Tags', [])
    
    highest_chart_data[song] = {
        'song': song,
        'performer': performer,
        'chart_position': highest_chart_position,
        'date': highest_chart_date,
        'tags': ', '.join(tags),
        'lyrics': lyrics
    }

with open('filtered.csv', mode='w', newline='') as outfile:
    fieldnames = ['song', 'performer', 'chart_position', 'date', 'tags', 'lyrics']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for song_data in highest_chart_data.values():
        writer.writerow(song_data)