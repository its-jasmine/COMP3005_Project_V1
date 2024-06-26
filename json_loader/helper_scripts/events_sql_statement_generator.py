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
    "location_x",
    "location_y",
    "under_pressure",
    "off_camera",
    "out",
    "player_id"
]
columns_names_lineup = ['goalkeeper', 'right_back', 'right_center_back', 'left_center_back', 'left_back', 'right_defensive_midfield', 'left_defensive_midfield', 'right_midfield', 'left_midfield', 'right_center_forward', 'left_center_forward']

lineup_id = 0

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
        values.append(None)

    try:
        values.append(data["location"][0])
    except KeyError:
        values.append(None)
    
    try:
        values.append(data["location"][1])
    except KeyError:
        values.append(None)

    try:
        values.append(data["under_pressure"])
    except KeyError:
        values.append(None)

    try:
        values.append(data["off_camera"])
    except KeyError:
        values.append(None)

    try:
        values.append(data["out"])
    except KeyError:
        values.append(None)

    try:
        values.append(data["player"]["id"])
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;")

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

    if "pass" in data_keys:
        generate_insert_statement_pass(data["pass"], data["id"])
        
    if "carry" in data_keys:
        generate_insert_statement_carry(data["carry"], data["id"])
        
    if data["type"]["name"] == "Foul Won":
        generate_insert_statement_foul_won(data, data["id"])
        
    if data["type"]["name"] == "Substitution":
        try:
            generate_insert_statement_substitution(data["substitution"], data["id"])
        except KeyError:
            generate_insert_statement_substitution(data["stta"], data["id"])

    if data["type"]["name"] == "Starting XI":
        generate_insert_statement_starting_xi(data["tactics"], data["id"])

    if data["type"]["name"] == "Tactical Shift":
        generate_insert_statement_tactical_shift(data["tactics"], data["id"])

    id = data["id"]
    if data.get('type')['name'] == "Clearance":
        generate_insert_statement_clearance(data.get("clearance"), id)
    if data.get('type')['name'] == "Goal Keeper":
        generate_insert_statement_goal_keeper(data.get("goalkeeper"), id)
    if data.get('type')['name'] == "Foul Committed":
        generate_insert_statement_foul_committed(data.get("foul_committed"), id)
    if data.get('type')['name'] == "Miscontrol":
        generate_insert_statement_miscontrol(data.get("miscontrol"), id)
    if data.get('type')['name'] == "Dribbled Past":
        generate_insert_statement_dribble_past(data.get("counterpress"), id)
    if data.get('type')['name'] == "Pressure":
        generate_insert_statement_pressure(data.get("counterpress"), id)
    if data.get('type')['name'] == "Half Start":
        generate_insert_statement_half_start(data.get("half_start"), id)
    if data.get('type')['name'] == "Duel":
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
    columns_names = ["event_id", "key_pass_id", "end_location_x", "end_location_y", "end_location_z", "aerial_won", "follows_dribble", "first_time", "open_goal", "statsbomb_xg", "deflected", "technique", "body_part", "type", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        end_location = {"end_location_x":0, "end_location_y":1, "end_location_z":2}
        try:
            if name in ["technique", "body_part", "type", "outcome"]:
                values.append(data[name]["name"])
            elif name in ["end_location_x", "end_location_y", "end_location_z"]:
                try:
                    values.append(data["end_location"][end_location[name]])
                except:
                    values.append(None)
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
    global lineup_id
    lineup_values = []
    for player in data["lineup"]:
        lineup_values.append(player["player"]["id"])

    columns_names = ["event_id", "formation"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    columns = ', '.join(columns_names + columns_names_lineup) 
    values = ', '.join(map(repr, (values + lineup_values)))
    statement = f"INSERT INTO starting_xi ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/starting_xi.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")
    lineup_id += 1

def generate_insert_statement_tactical_shift(data, event_id):
    global lineup_id
    lineup_values = []
    for player in data["lineup"]:
        lineup_values.append(player["player"]["id"])

    columns_names = ["event_id", "formation"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    columns = ', '.join(columns_names + columns_names_lineup) 
    values = ', '.join(map(repr, (values + lineup_values)))
    statement = f"INSERT INTO tactical_shift ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
    with open("../insert_statements/tactical_shift.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")
    
    lineup_id += 1

def generate_insert_statement_50_50(data, event_id):
    columns_names = ["event_id", "outcome", "counterpress"]
    values = []
    values.append(event_id)
    values.append(data["50_50"]["outcome"]["name"])

    try:
        values.append(data["counterpress"])
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO fifty_fifty ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;" # table name can't start with numbers, writing as words
    statement = statement.replace("None", "NULL")
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
        values.append(data["counterpress"])
    except KeyError:
        values.append(None)

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO block ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
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
    with open("../insert_statements/bad_behaviour.sql", "a", encoding='utf-8') as file:
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
    except KeyError:
        values.append(None) # defensive
        values.append(None) # advantage
        values.append(None) # penalty

    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO foul_won ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace("None", "NULL")
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
                new_values[i] = data[i]["name"]
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
    statement = f"INSERT INTO foul_committed ({columns}) VALUES ({values}) ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/foul_committed.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_miscontrol(data, id):
    new_values = {}
    new_values["event_id"] = id
    try:
        new_values["aerial_won"] = data["aerial_won"]
    except: 
        new_values["aerial_won"] = None
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
    with open("../insert_statements/pressure.sql", "a", encoding='utf-8') as file:
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

def generate_insert_statement_pass(data, event_id):
    columns_names = ["event_id",
                     "recipient_id",
                     "length",
                     "angle",
                     "height",
                     "end_location_x",
                     "end_location_y",
                     "assisted_shot_id", 
                     "deflected", 
                     "miscommunication", 
                     "cross_", 
                     "switch", 
                     "shot_assist", 
                     "goal_assist", 
                     "body_part",
                     "type", 
                     "outcome", 
                     "technique", 
                     "through_ball"
                     ]
    values = []
    values.append(event_id)
    for name in columns_names[1:]:
        try:
            if name == "recipient_id":
                values.append(data["recipient"]["id"])
            elif name == "end_location_x":
                values.append(data["end_location"][0])
            elif name == "end_location_y":
                values.append(data["end_location"][1])
            elif name == "cross_":
                values.append(data["cross"])
            elif name in ["body_part", "outcome", "height", "type", "technique"]:
                values.append(data[name]["name"])
            else:
                values.append(data[name])
        except KeyError:
            values.append(None)


    columns = ', '.join(columns_names)
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO pass ({columns}) VALUES ({values})" + " ON CONFLICT (event_id) DO NOTHING;"
    statement = statement.replace('None', 'NULL')
    with open("../insert_statements/pass.sql", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def convert_json_to_sql_events(file_path, player):
    with open(f"../statsbomb_data/events/{file_path}", 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for data in json_data:
        statements += (generate_insert_statement_events("events", data, os.path.splitext(file_path)[0])) 
    return statements

sql_statements = []
directory = "../statsbomb_data/lineups/"
files = os.listdir(directory)

matches = []
with open(f"../statsbomb_data/matches/11/90.json", 'r', encoding='utf-8') as file:
    json_data = json.load(file)
    for data in json_data:
        matches.append(data["match_id"])

player = {}
for file in files:
    sql_statements += convert_json_to_sql_events(file, player)

sql_statements = list(set(sql_statements)) # deduplicate

# separated events into 4 files because of space
fourth = round(len(sql_statements) / 4)
for statement in sql_statements[:fourth]:
    with open("../insert_statements/events1.sql", "a", encoding='utf-8') as file:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")
for statement in sql_statements[fourth:fourth*2]:
    with open("../insert_statements/events2.sql", "a", encoding='utf-8') as file:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")
for statement in sql_statements[fourth*2:fourth*3]:
    with open("../insert_statements/events3.sql", "a", encoding='utf-8') as file:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")
for statement in sql_statements[fourth*3:]:
    with open("../insert_statements/events4.sql", "a", encoding='utf-8') as file:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")


