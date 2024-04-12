import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS referees \n" \
           "(referee_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "referee_name    VARCHAR(255) NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_insert_statement(table_name, data):
    statements = []
    new_values = {}
    new_values['referee_id'] = data['id']
    new_values['referee_name'] = data['name']
    new_values['country'] = data['country']['name']

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
        if row.get('referee'):
            # some entries don't have a stadium
            data = row.get('referee')
            statements += (generate_insert_statement("referees", data))
    return statements


sql_statements = []
#sql_statements.append(generate_create_statement())
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)

with open("../insert_statements/referees.sql", "a", encoding='utf-8') as file:
    for statement in sql_statements:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")