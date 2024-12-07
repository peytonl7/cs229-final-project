import csv
from collections import defaultdict

input_1 = 'efotw.csv'
output_1 = 'usaef.csv'

input_2 = 'gallup_congress_approval.csv'
output_2 = 'congress.csv'

input_3 = 'gallup_pres_approval.csv'
output_3 = 'average_pres_approval_by_year.csv'

# EFOTW -> USA

with open(input_1, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

filtered_data = [row for row in data if row['Countries'] == 'United States']

with open(output_1, mode='w', newline='') as outfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(filtered_data)

# Congress Approval

with open(input_2, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    print(reader.fieldnames)
    data = list(reader)

yearly_approval = defaultdict(list)

for row in data:
    date = row["\ufeffX.1"]
    year = date.split()[-1]
    approval = float(row['% Approve'])
    
    yearly_approval[year].append(approval)

average_approval_by_year = {year: sum(approvals) / len(approvals) for year, approvals in yearly_approval.items()}

with open(output_2, mode='w', newline='') as outfile:
    fieldnames = ['YEAR', 'AVERAGE_APPROVAL']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for year, avg_approval in sorted(average_approval_by_year.items()):
        writer.writerow({'YEAR': year, 'AVERAGE_APPROVAL': avg_approval})

# Presidential Approval

with open(input_3, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    data = list(reader)

yearly_approval = defaultdict(list)

for row in data:
    start_date = row['Start']
    end_date = row['End']
    start_year = start_date.split('/')[-1]
    end_year = end_date.split('/')[-1]
    approval = float(row['Approve'])
    
    yearly_approval[start_year].append(approval)
    if start_year != end_year:
        yearly_approval[end_year].append(approval)

average_approval_by_year = {year: sum(approvals) / len(approvals) for year, approvals in yearly_approval.items()}

with open(output_3, mode='w', newline='') as outfile:
    fieldnames = ['YEAR', 'AVERAGE_APPROVAL']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for year, avg_approval in sorted(average_approval_by_year.items()):
        writer.writerow({'YEAR': year, 'AVERAGE_APPROVAL': avg_approval})