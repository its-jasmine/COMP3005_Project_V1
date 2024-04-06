import json
match_id_list = []
with open("output", 'r') as file:
    file.seek(0)
    for line in file:
        match_id = line.strip()
        match_id_list.append(match_id)

""" Create Table Statements """
def generate_create_statement_clearance():
    return "CREATE TABLE IF NOT EXISTS clearance \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "aerial_won     BOOLEAN, \n" \
           "body_part      VARCHAR(255),  \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_goal_keeper():
    return "CREATE TABLE IF NOT EXISTS goal_keeper \n" \
           "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "position        VARCHAR(255) NOT NULL, \n" \
           "end_location_x  FLOAT NOT NULL, \n" \
           "end_location_y  FLOAT NOT NULL, \n" \
           "technique       VARCHAR(255), \n" \
           "body_part       VARCHAR(255), \n" \
           "type            VARCHAR(255) NOT NULL, \n" \
           "outcome         VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_foul_committed():
    return "CREATE TABLE IF NOT EXISTS foul_committed \n" \
           "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress    VARCHAR(255), \n" \
           "offensive       BOOLEAN, \n" \
           "type            VARCHAR(255), \n" \
           "advantage       BOOLEAN, \n" \
           "penalty         VARCHAR(255), \n" \
           "card            VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_miscontrol():
    return "CREATE TABLE IF NOT EXISTS miscontrol \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "aerial_won     BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_dribble_past():
    return "CREATE TABLE IF NOT EXISTS dribble_past \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_pressure():
    return "CREATE TABLE IF NOT EXISTS pressure \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_half_start():
    return "CREATE TABLE IF NOT EXISTS half_start \n" \
           "(event_id          VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "late_video_start   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_duel():
    return "CREATE TABLE IF NOT EXISTS duel \n" \
           "(event_id   VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "type        VARCHAR(255), \n" \
           "outcome     VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

""" Insert Values Statements """
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
    with open("../insert_statements/clearance.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/goal_keeper.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/foul_comimitted.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/miscontrol.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/dribble_past.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/statement_pressure.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/half_start.txt", "a", encoding='utf-8') as file:
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
    with open("../insert_statements/duel.txt", "a", encoding='utf-8') as file:
        file.write(statement + "\n")

""" Grabbing Data From JSON """

def generate_insert_statement(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    statements = []
    for row in json_data:
        id = row["id"]
        if row.get('type')['name'] == "Clearance":
            statements += (generate_insert_statement_clearance(row.get("clearance"), id))
        elif row.get('type')['name'] == "Goal Keeper":
            statements += (generate_insert_statement_goal_keeper(row.get("goalkeeper"), id))
        elif row.get('type')['name'] == "Foul Committed":
            statements += (generate_insert_statement_foul_committed(row.get("foul_committed"), id))
        elif row.get('type')['name'] == "Miscontrol":
            statements += (generate_insert_statement_miscontrol(row.get("miscontrol"), id))
        elif row.get('type')['name'] == "Dribbled Past":
            statements += (generate_insert_statement_dribble_past(row.get("counterpress"), id))
        elif row.get('type')['name'] == "Pressure":
            statements += (generate_insert_statement_pressure(row.get("counterpress"), id))
        elif row.get('type')['name'] == "Half Start":
            statements += (generate_insert_statement_half_start(row.get("half_start"), id))
        elif row.get('type')['name'] == "Duel":
            statements += (generate_insert_statement_duel(row.get("duel"), id))
    return statements


# Convert JSON data to SQL statements
sql_statements = []
sql_statements.append(generate_create_statement_clearance())
sql_statements.append(generate_create_statement_dribble_past())
sql_statements.append(generate_create_statement_duel())
sql_statements.append(generate_create_statement_foul_committed())
sql_statements.append(generate_create_statement_goal_keeper())
sql_statements.append(generate_create_statement_half_start())
sql_statements.append(generate_create_statement_miscontrol())
sql_statements.append(generate_create_statement_pressure())

#for match_id in match_id_list:
#    sql_statements += generate_insert_statement(f"../statsbomb_data/events/{match_id}.json")
    
#sql_statements = set(sql_statements) # deduplicate

for statement in sql_statements:
    # statement = statement.replace('None', 'NULL')
    print(statement)