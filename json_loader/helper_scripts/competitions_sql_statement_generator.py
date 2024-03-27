import json

# TODO CREATE TABLE
def generate_insert_statement(table_name, data):
    columns = ', '.join(data.keys()) # TODO we will hard code these values
    values = ', '.join(map(repr, data.values()))
    return f"INSERT INTO {table_name} ({columns}) VALUES ({values});" # TODO add IF NOT EXISTS

def convert_json_to_sql(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        row.pop("match_updated", None)
        row.pop("match_updated_360", None)
        row.pop("match_available_360", None)
        row.pop("match_available", None)
        statements.append(generate_insert_statement("competitions", row))  # Replace 'YourTableName' with your actual table name
    return statements

# Path to the JSON file
file_path = "../statsbomb_data/competitions.json"  # Replace 'your_file.json' with the actual file path

# Convert JSON data to SQL statements
sql_statements = convert_json_to_sql(file_path)

# Print SQL statements
for statement in sql_statements:
    print(statement)
