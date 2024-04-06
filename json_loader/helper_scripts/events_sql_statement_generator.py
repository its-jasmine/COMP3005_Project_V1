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
    "out"
]
columns_names_lineup = ['lineup_id', 'goalkeeper', 'right_back', 'right_center_back', 'left_center_back', 'left_back', 'right_defensive_midfield', 'left_defensive_midfield', 'right_midfield', 'left_midfield', 'right_center_forward', 'left_center_forward']

lineup_id = 0

# match_id = name of file
# I'm confused
def generate_insert_statement_events(table_name, data, match_id):
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
        values.append("NULL")

    try:
        values.append(data["location"])
    except KeyError:
        values.append("NULL")

    try:
        values.append(data["under_pressure"])
    except KeyError:
        values.append("NULL")

    try:
        values.append(data["off_camera"])
    except KeyError:
        values.append("NULL")

    try:
        values.append(data["out"])
    except KeyError:
        values.append("NULL")

    try:
        values.append(data["related_events"])
    except KeyError:
        values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;") # TODO add IF NOT EXISTS
    
    if "ball_recovery" in data.keys():
        generate_insert_statement_ball_recovery(data["ball_recovery"], data["id"])

    data_keys = data.keys()
    if "ball_recovery" in data_keys:
        generate_insert_statement_ball_recovery(data["ball_recovery"], data["id"])

    if "dribble" in data_keys:
        generate_insert_statement_dribble(data["dribble"], data["id"])

    if "shot" in data_keys:
        generate_insert_statement_shot(data["shot"], data["id"])

    if "injury_stoppage" in data_keys:
        generate_insert_statement_injury_stoppage(data["injury_stoppage"], data["id"])

    if "ball_receipt" in data_keys:
        generate_insert_statement_ball_receipt(data["ball_receipt"], data["id"])

    if "50_50" in data_keys:
        generate_insert_statement_50_50(data, data["id"])
        
    if "block" in data_keys:
        generate_insert_statement_block(data, data["id"])
        
    if "interception" in data_keys:
        generate_insert_statement_interception(data["interception"], data["id"])
        
    if "bad_behaviour" in data_keys:
        generate_insert_statement_bad_behaviour(data["bad_behaviour"], data["id"])
        
    if data["type"]["name"] == "Player Off": # TODO may remove
        generate_insert_statement_player_off(data, data["id"])
        
    if data["type"]["name"] == "Half End": # TODO may remove
        generate_insert_statement_half_end(data, data["id"])
        
    if "carry" in data_keys:
        generate_insert_statement_carry(data["carry"], data["id"])
        
    if data["type"]["name"] == "Foul Won":
        generate_insert_statement_foul_won(data, data["id"])
        
    if data["type"]["name"] == "Substitution":
        try:
            generate_insert_statement_substitution(data["substitution"], data["id"])
        except KeyError:
            generate_insert_statement_substitution(data["stta"], data["id"])

    # if data["type"]["name"] == "Starting XI":
    #     generate_insert_statement_starting_xi(data["tactics"], data["id"])

    if data["type"]["name"] == "Tactical Shift":
        generate_insert_statement_tactical_shift(data["tactics"], data["id"])

    id = data["id"]
    if data.get('type')['name'] == "Clearance":
        generate_insert_statement_clearance(data.get("clearance"), id)
    elif data.get('type')['name'] == "Goal Keeper":
        generate_insert_statement_goal_keeper(data.get("goalkeeper"), id)
    elif data.get('type')['name'] == "Foul Committed":
        generate_insert_statement_foul_committed(data.get("foul_committed"), id)
    elif data.get('type')['name'] == "Miscontrol":
        generate_insert_statement_miscontrol(data.get("miscontrol"), id)
    elif data.get('type')['name'] == "Dribbled Past":
        generate_insert_statement_dribble_past(data.get("counterpress"), id)
    elif data.get('type')['name'] == "Pressure":
        generate_insert_statement_pressure(data.get("counterpress"), id)
    elif data.get('type')['name'] == "Half Start":
        generate_insert_statement_half_start(data.get("half_start"), id)
    elif data.get('type')['name'] == "Duel":
        generate_insert_statement_duel(data.get("duel"), id)
    
    return statements

def generate_insert_statement_ball_recovery(data, event_id):
    columns_names = ["event_id", "offensive", "recovery_failure"]
    values = []
    
    values.append(event_id)
    for name in columns_names[1:]:
        try:
            values.append(data[name])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO ball_recovery ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/ball_recovery.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_dribble(data, event_id):
    columns_names = ["event_id", "overrun", "nutmeg", "outcome", "no_touch"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            if name == "outcome":
                values.append(data["outcome"]["name"])
            else:
                values.append(data[name])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO dribble ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/dribble.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_shot(data, event_id):
    columns_names = ["event_id", "key_pass_id", "end_location", "aerial_won", "follows_dribble", "first_time", "open_goal", "statsbomb_xg", "deflected", "technique", "body_part", "type", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            if name in ["technique", "body_part", "type", "outcome"]:
                values.append(data[name]["name"])
            else:
                values.append(data[name])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO shot ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/shot.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_injury_stoppage(data, event_id):
    columns_names = ["event_id", "in_chain"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO injury_stoppage ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/injury_stoppage.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_ball_receipt(data, event_id):
    columns_names = ["event_id", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name]["name"])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO ball_receipt ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/ball_receipt.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_substitution(data, event_id):
    columns_names = ["event_id", "replacement", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name]["name"])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO substitution ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/substitution.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_starting_xi(data, event_id):
    #statement for lineup
    global lineup_id
    lineup_values = []
    lineup_values.append(lineup_id)
    for player in data["lineup"]:
        lineup_values.append(player["player"]["id"])

    columns = ', '.join(columns_names_lineup) 
    values = ', '.join(map(repr, lineup_values))
    statement = f"INSERT INTO lineups ({columns}) VALUES ({values})"  + " ON CONFLICT (lineup_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/lineup.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")


    #statement for starting xi
    columns_names = ["event_id", "formation", "lineup_id"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    values.append(lineup_id)
    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO starting_xi ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/starting_xi.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")
    lineup_id += 1
    
    

def generate_insert_statement_tactical_shift(data, event_id):
    #statement for lineup
    global lineup_id
    lineup_values = []
    lineup_values.append(lineup_id)
    for player in data["lineup"]:
        lineup_values.append(player["player"]["id"])

    columns = ', '.join(columns_names_lineup) 
    values = ', '.join(map(repr, lineup_values))
    statement = f"INSERT INTO lineups ({columns}) VALUES ({values})"  + " ON CONFLICT (lineup_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/lineup.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")


    columns_names = ["event_id", "formation", "lineup_id"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    values.append(lineup_id)
    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO tactical_shift ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/tactical_shift.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")
    
    lineup_id += 1

def generate_insert_statement_50_50(data, event_id):
    columns_names = ["event_id", "outcome", "counterpress"]
    values = []
    values.append(event_id)
    values.append(data["50_50"]["outcome"]["name"]) # just including name rather than id

    try:
        values.append(data["counterpress"]) #TODO docs mention this, but most objects don't seem to have it? setting as NULL for now
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO fifty_fifty ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;" # table name can't start with numbers, writing as words
    statement = statement.replace("None", "NULL")
    print(statement)
    with open("../insert_statements/fifty_fifty.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_block(data, event_id):
    columns_names = ["event_id", "deflection", "offensive", "save_block",  "counterpress"]
    values = []
    values.append(event_id)

    for name in columns_names[1:4]:
        try:
            values.append(data["block"][name])
        except KeyError:
            values.append(None)
    try:
        values.append(data["counterpress"])  # TODO docs mention this, but most objects don't seem to have it? setting as NULL for now
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO block ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    print(statement)
    with open("../insert_statements/block.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")


def generate_insert_statement_interception(data, event_id):
    columns_names = ["event_id", "outcome"]
    values = []
    values.append(event_id)

    values.append(data["outcome"]["name"])
    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO interception ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    print(statement)
    with open("../insert_statements/interception.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_bad_behaviour(data, event_id):
    columns_names = ["event_id", "card"]
    values = []
    values.append(event_id)

    values.append(data["card"]["name"])
    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO bad_behaviour ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    print(statement)
    with open("../insert_statements/bad_behaviour.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_player_off(data, event_id): # TODO maybe remove? additional attribute is not found on event level, and theres never a key with additional attributes
    columns_names = ["event_id", "permanent"]
    values = []
    values.append(event_id)

    try:
        values.append(data["permanent"])
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO player_off ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    print(statement)
    with open("../insert_statements/player_off.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_half_end(data, event_id): # TODO maybe remove? additional attribute is not found on event level, and theres never a key with additional attributes
    columns_names = ["event_id", "early_video_end", "match_suspended"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data["half_end"][name])
        except KeyError:
            values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO half_end ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    print(statement)
    with open("../insert_statements/half_end.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_carry(data, event_id):
    columns_names = ["event_id", "end_location_x", "end_location_y"]
    values = []
    values.append(event_id)

    values.append(data["end_location"][0])
    values.append(data["end_location"][1])
    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO carry ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    print(statement)
    with open("../insert_statements/carry.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")


def generate_insert_statement_foul_won(data, event_id):
    columns_names = ["event_id", "defensive", "advantage", "penalty"]
    values = []
    values.append(event_id)
    try:
        data = data["foul_won"]
        for name in columns_names[1:]:
            try:
                values.append(data[name])
            except KeyError:
                values.append(None)
    except KeyError: # TODO maybe make booleans FALSE instead of NULL when they are not there, consider for other boools too
        values.append(None) # defensive
        values.append(None) # advantage
        values.append(None) # penalty

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO foul_won ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    print(statement)
    with open("../insert_statements/foul_won.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_clearance(data, id):
    column_names = ["aerial_won", "body_part"]
    new_values = {}
    new_values["event_id"] = id

    for i in column_names:
        try:
            if i == "aerial_won":
                new_values[i] = data[i]
            else:
                new_values[i] = data[i]
        except:
            new_values[i] = None

    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO clearance ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/clearance.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_goal_keeper(data, id):
    column_names = ["position", "end_location_x", "end_location_y", "technique", "body_part", "type", "outcome"]
    new_values = {}
    new_values["event_id"] = id

    for i in column_names:
        try:
            if i == "end_location_x":
                new_values[i] = data["end_location"][0]
            elif i == "end_location_y":
                new_values[i] = data["end_location"][1]
            else:
                new_values[i] = data[i]["name"]
        except:
            new_values[i] = None

    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO goal_keeper ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/goal_keeper.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_foul_committed(data, id):
    column_names = ["counterpress","offensive", "type", "advantage", "penalty", "card"]
    new_values = {}
    new_values["event_id"] = id

    for i in column_names:
        try:
            if i in ["type", "card"]:
                new_values[i] = data[i]["name"]
            else:
                new_values[i] = data[i]
        except:
            new_values[i] = None

    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO comitted ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/foul_comimitted.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_miscontrol(data, id):
    new_values = {}
    new_values["event_id"] = id
    try:
        new_values["counterpress"] = data["aerial_won"]
    except: 
        new_values["counterpress"] = None
    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO miscontrol ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/miscontrol.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_dribble_past(data, id):
    new_values = {}
    new_values["event_id"] = id
    try:
        new_values["counterpress"] = data
    except: 
        new_values["counterpress"] = None
    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO dribble_past ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/dribble_past.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_pressure(data, id):
    new_values = {}
    new_values["event_id"] = id
    try:
        new_values["counterpress"] = data
    except: 
        new_values["counterpress"] = None
    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO pressure ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/statement_pressure.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_half_start(data, id):
    new_values = {}
    new_values["event_id"] = id
    try:
        new_values["late_video_start"] = data["late_video_start"]
    except: 
        new_values["late_video_start"] = None
    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO half_start ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/half_start.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_duel(data, id):
    column_names = ["type", "outcome"]
    new_values = {}
    new_values["event_id"] = id

    for i in column_names:
        try:
            new_values[i] = data[i]["name"]
        except:
            new_values[i] = None

    columns = ', '.join(new_values.keys()) 
    values = ', '.join(map(repr, new_values.values()))
    statement = f"INSERT INTO duel ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/duel.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def convert_json_to_sql_events(file_path):
    with open(f"../statsbomb_data/events/{file_path}", 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    statements = []
    for data in json_data:
        statements += (generate_insert_statement_events("events", data, os.path.splitext(file_path)[0])) # Replace 'YourTableName' with your actual table name
    
    return statements


sql_statements = []
sql_statements.append(generate_create_statement())
directory = "../statsbomb_data/events/"
files = os.listdir(directory)

#for file in files:
#    sql_statements += convert_json_to_sql_events(file)

#sql_statements += convert_json_to_sql_events("303473.json") #just to test

sql_statements = set(sql_statements) # deduplicate

"""
with open("../insert_statements/events.sql", "a", encoding='utf-8') as file:
    for statement in sql_statements:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")
"""

