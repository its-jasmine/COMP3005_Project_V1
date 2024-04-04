import json
import os

columns_names = keys = [
    "event_id",
    "match_id",
    "index",
    "period",
    "timestamp",
    "minute",
    "second",
    "type",
    "possession",
    "possession_team_id",
    "play_pattern",
    "team_id",
    "duration",
    "location",
    "under_pressure",
    "off_camera",
    "out",
    "related_events"
]


def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS matches \n" \
           "(event_id            VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "match_id             INTEGER NOT NULL,  \n" \
           "index                INTEGER NOT NULL, \n" \
           "period               INTEGER NOT NULL, \n" \
           "timestamp            TIME NOT NULL, \n" \
           "minute               INTEGER NOT NULL, \n" \
           "second               INTEGER NOT NULL, \n" \
           "type                 VARCHAR(255) NOT NULL, \n" \
           "possession            INTEGER NOT NULL, \n" \
           "possession_team_id    INTEGER NOT NULL, \n" \
           "play_pattern         VARCHAR(255) NOT NULL, \n" \
           "team_id              INTEGER, \n" \
           "duration             FLOAT, \n" \
           "location             INTEGER, \n" \
           "under_pressure       INTEGER, \n" \
           "off_camera           INTEGER, \n" \
           "out                  INTEGER, \n" \
           "related_events       INTEGER);"

# match_id = name of file
# I'm confused
def generate_insert_statement(table_name, data, match_id):
    statements = []
    values = []
    values.append(data["id"])
    values.append(match_id)
    values.append(data["index"])
    values.append(data["period"])
    values.append(data["timestamp"])
    values.append(data["minute"])
    values.append(data["second"])
    values.append(data["type"]["name"])
    values.append(data["possession"])
    values.append(data["possession_team"]["id"]) 
    values.append(data["play_pattern"]["name"])
    values.append(data["team"]["id"]) 
    try:
        values.append(data["duration"])
    except KeyError:
        pass

    try:
        values.append(data["location"])
    except KeyError:
        pass

    try:
        values.append(data["under_pressure"])
    except KeyError:
        pass

    try:
        values.append(data["off_camera"])
    except KeyError:
        pass

    try:
        values.append(data["out"])
    except KeyError:
        pass

    try:
        values.append(data["related_events"])
    except KeyError:
        pass

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;") # TODO add IF NOT EXISTS
    return statements


def convert_json_to_sql(file_path):
    with open(f"../statsbomb_data/events/{file_path}", 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    statements = []
    for data in json_data:
        statements += (generate_insert_statement("events", data, os.path.splitext(file_path)[0])) # Replace 'YourTableName' with your actual table name
    
    return statements


sql_statements = []
sql_statements.append(generate_create_statement())
directory = "../statsbomb_data/events/"
files = os.listdir(directory)

# for file in files:
#     sql_statements += convert_json_to_sql(file)

sql_statements += convert_json_to_sql(files[0]) #just to test 

sql_statements = set(sql_statements) # deduplicate
for statement in sql_statements:
    statement = statement.replace("None", "NULL")
    # execute_query(statement)
    print(statement)