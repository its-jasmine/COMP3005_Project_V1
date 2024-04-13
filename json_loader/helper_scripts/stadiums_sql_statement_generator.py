import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS stadiums \n" \
           "(stadium_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "stadium_name    VARCHAR(255) NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_insert_statement(table_name, data):
    statements = []
    new_values = {}
    new_values['stadium_id'] = data['id']
    new_values['stadium_name'] = data['name']
    new_values['country'] = data['country']['name']

    columns = ', '.join(new_values.keys()) 

    all_values = new_values.values()
    values = ', '.join(map(repr, all_values))
    statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values}) "+ " ON CONFLICT (stadium_id) DO NOTHING;")
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        if row.get('stadium'):
            data = row.get('stadium')
            statements += (generate_insert_statement("stadiums", data))
    return statements


sql_statements = []
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)

for statement in sql_statements:
    # "St. Mary''s Stadium" and "St. James'' Park" are causing issues w sql... workaround:
    statement = statement.replace("''", "")
    statement = statement.replace('"', "'")


with open("../insert_statements/stadiums.sql", "a", encoding='utf-8') as file:
    for statement in sql_statements:
        # "St. Mary''s Stadium" and "St. James'' Park" are causing issues w sql... workaround:
        statement = statement.replace("''", "")
        statement = statement.replace('"', "'")
        file.write(statement + "\n")