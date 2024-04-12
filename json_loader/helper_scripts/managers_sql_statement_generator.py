import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS managers \n" \
           "(manager_id           INTEGER NOT NULL, \n" \
           "manager_name          VARCHAR(255) NOT NULL, \n" \
           "manager_nickname      VARCHAR(255), \n" \
           "dob                   DATE NOT NULL, \n" \
           "country               VARCHAR(255) NOT NULL, \n" \
           "team_id               INTEGER NOT NULL, \n" \
           "PRIMARY KEY (manager_id, team_id),  \n" \
           "FOREIGN KEY (team_id) REFERENCES teams(team_id));"

def generate_insert_statement(table_name, data):
    statements = []
    new_values = {}

    for i in range(len(data['managers'])):
        new_values['manager_id'] = data['managers'][i]['id']
        new_values['manager_name'] = data['managers'][i]['name']
        new_values['manager_nickname'] = data['managers'][i]['nickname']
        new_values['dob'] = data['managers'][i]['dob']
        new_values['country'] = data['managers'][i]['country']['name']
        new_values['team_id'] = data['team_id']

        columns = ', '.join(new_values.keys()) 

        all_values = new_values.values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values})" + " ON CONFLICT (manager_id, team_id) DO NOTHING;")
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        if row.get('home_team') and row.get('home_team').get('managers'): # some teams don't have managers listed
            data = {}
            data['team_id'] = row.get('home_team')["home_team_id"]
            data["managers"] = row.get('home_team')["managers"]
            statements += (generate_insert_statement("managers", data))
        if row.get('away_team') and row.get('away_team').get('managers'): # some teams don't have managers listed
            data = {}
            data['team_id'] = row.get('away_team')["away_team_id"]
            data["managers"] = row.get('away_team')["managers"]
            statements += (generate_insert_statement("managers", data))

    return statements


sql_statements = []
# sql_statements.append(generate_create_statement())

sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)

with open("../insert_statements/managers.sql", "a", encoding='utf-8') as file:
    for statement in sql_statements:
        # For nicknames
        statement = statement.replace("None", "NULL")
        # "David O''Leary"
        statement = statement.replace("''", "")
        statement = statement.replace('"', "'")
        file.write(statement + "\n")