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

def generate_create_statement_ball_recovery():
    return "CREATE TABLE IF NOT EXISTS ball_recovery \n" \
           "(event_id            VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "offensive            VARCHAR(255),  \n" \
           "recovery_failure     VARCHAR(255) );"

def generate_create_statement_dribble():
    return "CREATE TABLE IF NOT EXISTS dribble \n" \
           "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "overrun      VARCHAR(255),  \n" \
           "nutmeg       VARCHAR(255),  \n" \
           "outcome      VARCHAR(255),  \n" \
           "no_touch     VARCHAR(255));"

def generate_create_statement_shot():
    return "CREATE TABLE IF NOT EXISTS shot \n" \
           "(event_id         VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "key_pass_id       VARCHAR(255),  \n" \
           "end_location      VARCHAR(255),  \n" \
           "aerial_won        VARCHAR(255),  \n" \
           "follows_dribble   VARCHAR(255),  \n" \
           "first_time        VARCHAR(255),  \n" \
           "open_goal         VARCHAR(255),  \n" \
           "statsbomb_xg      INTEGER,  \n" \
           "deflected         VARCHAR(255),  \n" \
           "technique         VARCHAR(255),  \n" \
           "body_part         VARCHAR(255),  \n" \
           "type              VARCHAR(255),  \n" \
           "outcome           VARCHAR(255));"

def generate_create_statement_injury_stoppage():
    return "CREATE TABLE IF NOT EXISTS injury_stoppage \n" \
           "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "in_chain      VARCHAR(255));"

def generate_create_statement_ball_receipt():
    return "CREATE TABLE IF NOT EXISTS ball_receipt \n" \
           "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "outcome      VARCHAR(255));"

def generate_create_statement_substitution():
    return "CREATE TABLE IF NOT EXISTS substitution \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "replacement    VARCHAR(255),  \n" \
           "outcome        VARCHAR(255));"

def generate_create_statement_starting_xi():
    return "CREATE TABLE IF NOT EXISTS starting_xi \n" \
           "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "formation    INTEGER,  \n" \
           "lineup_id    INTEGER);"

def generate_create_statement_tactical_shift():
    return "CREATE TABLE IF NOT EXISTS tactical_shift \n" \
           "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "formation    INTEGER,  \n" \
           "lineup_id    INTEGER);"

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

    if "dribble" in data.keys():
        generate_insert_statement_dribble(data["dribble"], data["id"])

    if "shot" in data.keys():
        generate_insert_statement_shot(data["shot"], data["id"])

    if "injury_stoppage" in data.keys():
        generate_insert_statement_injury_stoppage(data["injury_stoppage"], data["id"])

    if "ball_receipt" in data.keys():
        generate_insert_statement_ball_receipt(data["ball_receipt"], data["id"])

    if data["type"]["name"] == "Substitution":
        try:
            generate_insert_statement_substitution(data["substitution"], data["id"])
        except KeyError:
            generate_insert_statement_substitution(data["stta"], data["id"])

    if data["type"]["name"] == "Starting XI":
        generate_insert_statement_starting_xi(data["tactics"], data["id"])

    if data["type"]["name"] == "Tactical Shift":
        generate_insert_statement_tactical_shift(data["tactics"], data["id"])
    
    return statements

def generate_insert_statement_ball_recovery(data, event_id):
    columns_names = ["event_id", "offensive", "recovery_failure"]
    values = []
    
    values.append(event_id)
    for name in columns_names[1:]:
        try:
            values.append(data[name])
        except KeyError:
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO ball_recovery ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/ball_recovery.txt", "a", encoding='utf-8') as file:
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
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO dribble ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/dribble.txt", "a", encoding='utf-8') as file:
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
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO shot ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/shot.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_injury_stoppage(data, event_id):
    columns_names = ["event_id", "in_chain"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name])
        except KeyError:
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO injury_stoppage ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/injury_stoppage.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_ball_receipt(data, event_id):
    columns_names = ["event_id", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name]["name"])
        except KeyError:
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO ball_receipt ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/ball_receipt.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_substitution(data, event_id):
    columns_names = ["event_id", "replacement", "outcome"]
    values = []
    values.append(event_id)

    for name in columns_names[1:]:
        try:
            values.append(data[name]["name"])
        except KeyError:
            values.append("NULL")

    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO substitution ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/substitution.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_starting_xi(data, event_id):
    columns_names = ["event_id", "formation", "lineup_id"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    values.append("lineup id???")
    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO starting_xi ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/starting_xi.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

def generate_insert_statement_tactical_shift(data, event_id):
    columns_names = ["event_id", "formation", "lineup_id"]
    values = []
    values.append(event_id)
    values.append(data["formation"])
    values.append("lineup id???")
    columns = ', '.join(columns_names) 
    values = ', '.join(map(repr, values))
    statement = f"INSERT INTO tactical_shift ({columns}) VALUES ({values})"  + " ON CONFLICT (event_id) DO NOTHING;"
    with open("../insert_statements/tactical_shift.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")


def generate_create_statement_50_50():
    return "" # TODO

def generate_create_statement_block():
    return "" # TODO

def generate_create_statement_interception():
    return "" # TODO

def generate_create_statement_bad_behaviour():
    return "" # TODO


def generate_create_statement_player_off():
    return ""  # TODO

def generate_create_statement_half_end():
    return ""  # TODO

def generate_create_statement_carry():
    return ""  # TODO

def generate_create_statement_foul_won():
    return ""  # TODO


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

# for file in files:
#     sql_statements += convert_json_to_sql(file)

sql_statements += convert_json_to_sql_events(files[0]) #just to test 

sql_statements = set(sql_statements) # deduplicate
for statement in sql_statements:
    statement = statement.replace("None", "NULL")
    # execute_query(statement)
    # print(statement)