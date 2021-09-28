import json
from collections import defaultdict

with open('problem1_day-1.json', 'r') as f:
    past_1 = json.load(f)

with open('problem1_day-2.json', 'r') as f:
    past_2 = json.load(f)

with open('problem1_day-3.json', 'r') as f:
    past_3 = json.load(f)

past_record = {}

for day in past_1:
    if int(day) not in past_record:
        past_record[int(day)] = defaultdict(int)
    for element in past_1[day]:
        past_record[int(day)][element[0]] += 1

for day in past_2:
    if int(day) not in past_record:
        past_record[int(day)] = defaultdict(int)
    for element in past_2[day]:
        past_record[int(day)][element[0]] += 1

for day in past_3:
    if int(day) not in past_record:
        past_record[int(day)] = defaultdict(int)
    for element in past_3[day]:
        past_record[int(day)][element[0]] += 1

past_record_half = {}

for minute in past_record:
    half_min = (minute//30)*30
    if half_min not in past_record_half:
        past_record_half[half_min] = defaultdict(int)
    for loc in past_record[minute]:
        past_record_half[half_min][loc] += past_record[minute][loc]

for minute in past_record_half:
    summation = sum(list(past_record_half[minute].values()))    
    for loc in past_record_half[minute]:
        past_record_half[minute][loc] = past_record_half[minute][loc]/summation        

size = 5
for minute in past_record_half:
    print("minute", minute)
    print_map = [[0]*size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            this_id = col*size+(size-1-row)
            print_map[row][col] = str(past_record_half[minute][this_id])[:4]
        
    for row in range(size):
        print(print_map[row])

with open('past_record_half.json', 'w') as f:
    json.dump(past_record_half, f)


