
import json
import os


columns_names = ['goalkeeper', 'right_back', 'right_center_back', 'left_center_back', 'left_back', 'right_defensive_midfield', 'left_defensive_midfield', 'right_midfield', 'left_midfield', 'right_center_forward', 'left_center_forward']


def insert_statements_position(data, match_id):
    columns_names = ["match_id", "team_id", "player_id", "position_id", "position_name", "from_time", "to_time", "from_period", "to_period", "start_reason", "end_reason"]
    statements = []
    values = []
    values.append(match_id)
    values.append(data["team_id"])
    for player in data["lineup"]:
        values = []
        values.append(int(match_id))
        values.append(data["team_id"])
        values.append(player["player_id"])
        if len(player["positions"]) > 0:
            for position in player["positions"]:
                values += [position[key] for key in position]
                columns_str = ', '.join(columns_names) 
                values_str = ', '.join(map(repr, values))
                statement = f"INSERT INTO position ({columns_str}) VALUES ({values_str})"  + " ON CONFLICT (match_id, team_id) DO NOTHING;"
                statement = statement.replace("None", "NULL")
                statements.append(statement)
                values = values[:-8]
    return statements


def insert_statements_lineup(data, match_id):
    columns_names = ["match_id", "team_id", "player_id"]
    statements = []
    values = []
    values.append(int(match_id))
    values.append(data["team_id"])
    for player in data["lineup"]:
        values.append(player["player_id"])
        columns_str = ', '.join(columns_names) 
        values_str = ', '.join(map(repr, values))
        statement = f"INSERT INTO lineups ({columns_str}) VALUES ({values_str})"  + " ON CONFLICT (match_id, team_id) DO NOTHING;"
        statement = statement.replace("None", "NULL")
        statements.append(statement)
        values.pop()
    return statements

def convert_json_to_sql_events(file_path):
    with open(f"../statsbomb_data/lineups/{file_path}", 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        statements_lineup = []
        statements_positions = []
    for data in json_data:
        statements_lineup += (insert_statements_lineup(data, os.path.splitext(file_path)[0])) # Replace 'YourTableName' with your actual table name
        statements_positions += (insert_statements_position(data, os.path.splitext(file_path)[0]))
    return statements_lineup, statements_positions


sql_statements_lineups = []
sql_statements_positions = []
directory = "../statsbomb_data/lineups/"
files = os.listdir(directory)
for file in files:
    states = convert_json_to_sql_events(file)
    sql_statements_lineups += states[0]
    sql_statements_positions += states[1]
    
sql_statements = list(set(sql_statements_lineups)) # deduplicate

for statement in sql_statements:
    with open("../insert_statements/lineups.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

sql_statements = list(set(sql_statements_positions)) # deduplicate
for statement in sql_statements:
    with open("../insert_statements/positions.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

