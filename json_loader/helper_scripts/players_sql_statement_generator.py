import json

columns_names = ["player_id", "player_name", "player_nickname", "jersey_number", "country"]

# TODO CREATE TABLE
def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS players \n" \
           "(player_id       INTEGER NOT NULL, \n" \
           "player_name     VARCHAR(255) NOT NULL,  \n" \
           "player_nickname VARCHAR(255), \n" \
           "jersey_number   INTEGER NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_insert_statement(table_name, data):
    statements = []
    for i in range(len(data['lineup'])):
        del data['lineup'][i]['cards']
        del data['lineup'][i]['positions']
        data['lineup'][i]['country'] = data['lineup'][i]['country']['name']

        columns = ', '.join(data['lineup'][i].keys()) # TODO we will hard code these values
        all_values = data['lineup'][i].values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values})"  + ";") # TODO add IF NOT EXISTS
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        row.pop("team_id", None)
        row.pop("team_name", None)
        statements += (generate_insert_statement("players", row)) # Replace 'YourTableName' with your actual table name
    return statements

# Path to the JSON file
file_path = "../statsbomb_data/lineups/15946.json"  # Replace 'your_file.json' with the actual file path

# Convert JSON data to SQL statements
sql_statements = []
sql_statements.append(generate_create_statement())
sql_statements += convert_json_to_sql(file_path)

# Print SQL statements
for statement in sql_statements:
    statement = statement.replace("None", "NULL")
    print(statement)
