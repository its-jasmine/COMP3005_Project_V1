import os
import json

directory = "../statsbomb_data/events/"


files = os.listdir(directory)

event_types = {}

for file in files:
    with open(f"../statsbomb_data/events/{file}", 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            event_types[data["type"]["name"]] = list(data.keys())

    break

# for event in event_types:
#     print(f"{event}: {event_types[event]}\n" )

common_elements = set(event_types["Starting XI"])

for event in event_types:
    common_elements = common_elements.intersection(event_types[event])

print("Common elements: ", list(common_elements))

for event in event_types:
    print(f"{event}: {set(event_types[event]) - common_elements}\n" )