import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS teams \n" \
           "(team_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "team_name    VARCHAR(255) NOT NULL, \n" \
           "team_gender  VARCHAR(255) NOT NULL, \n" \
           "team_group   VARCHAR(255),  \n" \
           "team_country VARCHAR(255) NOT NULL);"
           
def generate_insert_statement(table_name, data):
    statements = []
    new_values = {}

    if data.get("home_team"):
        new_values['team_id'] = data['home_team']['home_team_id']
        new_values['team_name'] = data['home_team']['home_team_name']
        new_values['team_gender'] = data['home_team']['home_team_gender']
        new_values['team_group'] = data['home_team']['home_team_group']
        new_values['team_country'] = data['home_team']['country']['name']

        columns = ', '.join(new_values.keys()) 
        all_values = new_values.values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")

    if data.get("away_team"):
        new_values['team_id'] = data['away_team']['away_team_id']
        new_values['team_name'] = data['away_team']['away_team_name']
        new_values['team_gender'] = data['away_team']['away_team_gender']
        new_values['team_group'] = data['away_team']['away_team_group']
        new_values['team_country'] = data['away_team']['country']['name']

        columns = ', '.join(new_values.keys()) 
        all_values = new_values.values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
    
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        data = {}
        data['home_team'] = row.get('home_team')
        data['away_team'] = row.get('away_team')
        statements += (generate_insert_statement("teams", data))
    return statements

sql_statements = []
sql_statements.append(generate_create_statement())
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)

for statement in sql_statements:
    statement = statement.replace("None", "NULL")
    print(statement)