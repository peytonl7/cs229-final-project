import csv
import json
from collections import defaultdict

# Input and output file paths
input_file = '../../data/hot-100.csv'
output_file = '../../data/processed-hot-100.csv'

# Dictionary to store data by song and performer
data = defaultdict(lambda: {
    "chart_instances": [],
    "time_on_chart": 0,
    "peak_position": float('inf'),
    "worst_position": float('-inf')
})

# Read the original CSV
with open(input_file, mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        song = row['song']
        performer = row['performer']
        
        # Update data for this song
        key = (song, performer)
        data[key]["chart_instances"].append({
            "chart_position": int(row['chart_position']),
            "chart_date": row['chart_date']
        })
        
        data[key]["time_on_chart"] += 1
        position = int(row['chart_position'])
        data[key]["peak_position"] = min(data[key]["peak_position"], position)
        data[key]["worst_position"] = max(data[key]["worst_position"], position)

# Write to the new CSV in the desired format
with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["song", "performer", "chart_instances", "time_on_chart", "peak_position", "worst_position"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for (song, performer), info in data.items():
        writer.writerow({
            "song": song,
            "performer": performer,
            "chart_instances": json.dumps(info["chart_instances"]),  # Use JSON format to store list of dictionaries
            "time_on_chart": info["time_on_chart"],
            "peak_position": info["peak_position"],
            "worst_position": info["worst_position"]
        })

print(f"Processed data has been saved to {output_file}")