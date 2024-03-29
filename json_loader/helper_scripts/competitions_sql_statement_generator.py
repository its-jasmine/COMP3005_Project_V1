import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS competitions \n" \
           "(competition_id     INTEGER NOT NULL, \n" \
           "season_id           INTEGER NOT NULL,  \n" \
           "competition_name    VARCHAR(255) NOT NULL, \n" \
           "season_name         VARCHAR(255) NOT NULL, \n" \
           "competition_gender  VARCHAR(255) NOT NULL, \n" \
           "country             VARCHAR(255) NOT NULL, \n" \
           "PRIMARY KEY (competition_id, season_id));"

def get_competition_gender(comp_id, season_id):
    with open("../statsbomb_data/competitions.json", 'r') as file:
        json_data = json.load(file)
    
    for i in range(len(json_data)):
        if json_data[i]['competition_id'] == comp_id and json_data[i]['season_id'] == season_id:
            return json_data[i]['competition_gender']

def generate_insert_statement(table_name, data):
    statements = []
    for _ in range(len(data)):
        new_values = {}
        new_values['competition_id'] = data['competition']['competition_id']
        new_values['season_id'] = data['season']['season_id']
        new_values['competition_name'] = data['competition']['competition_name']
        new_values['season_name'] = data['season']['season_name']
        new_values['competition_gender'] = get_competition_gender(new_values.get('competition_id'), new_values.get('season_id'))
        new_values['country'] = data['competition']['country_name']

        columns = ', '.join(new_values.keys()) 

        all_values = new_values.values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        data = {}
        data['competition'] = row.get('competition')
        data['season'] = row.get('season')
        statements += (generate_insert_statement("competitions", data))
    return statements


sql_statements = []
sql_statements.append(generate_create_statement())

sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)

for statement in sql_statements:
    print(statement)
