import json

def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS matches \n" \
           "(match_id            INTEGER NOT NULL PRIMARY KEY, \n" \
           "match_date           DATE NOT NULL,  \n" \
           "kick_off             TIME NOT NULL, \n" \
           "competition_id       INTEGER NOT NULL, \n" \
           "season_id            INTEGER NOT NULL, \n" \
           "home_team_id         INTEGER NOT NULL, \n" \
           "away_team_id         INTEGER NOT NULL, \n" \
           "home_score           INTEGER NOT NULL, \n" \
           "away_score           INTEGER NOT NULL, \n" \
           "match_status         VARCHAR(255) NOT NULL, \n" \
           "match_week           INTEGER NOT NULL, \n" \
           "competition_stage    VARCHAR(255) NOT NULL, \n" \
           "stadium_id           INTEGER, \n" \
           "referee_id           INTEGER, \n" \
           "FOREIGN KEY (competition_id, season_id) REFERENCES competitions(competition_id, season_id), \n" \
           "FOREIGN KEY (stadium_id) REFERENCES stadiums(stadium_id), \n" \
           "FOREIGN KEY (referee_id) REFERENCES referees(referee_id));"

def generate_insert_statement(table_name, data):
    statements = []
    for _ in range(len(data)):
        new_values = {}
        new_values['match_id'] = data['match_id']
        new_values['match_date'] = data['match_date']
        new_values['kick_off'] = data['kick_off']
        new_values['competition_id'] = data['competition']['competition_id']
        new_values['season_id'] = data['season']['season_id']
        new_values['home_team_id'] = data['home_team']['home_team_id']
        new_values['away_team_id'] = data['away_team']['away_team_id']
        new_values['home_score'] = data['home_score']
        new_values['away_score'] = data['away_score']
        new_values['match_status'] = data['match_status']
        new_values['match_week'] = data['match_week']
        new_values['competition_stage'] = data['competition_stage']['name']
        # Some matches don't have a stadium listed
        if data.get('stadium'):
            new_values['stadium_id'] = data['stadium']['id']
        else:
            new_values['stadium_id'] = None
        # Some matches don't have referees listed
        if data.get("referee"):
            new_values['referee_id'] = data['referee']['id']
        else:
            new_values['referee_id'] = None

        columns = ', '.join(new_values.keys()) 

        all_values = new_values.values()
        values = ', '.join(map(repr, all_values))
        statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values}) " + " ON CONFLICT (match_id) DO NOTHING;")
    return statements

def convert_json_to_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    statements = []
    for row in json_data:
        statements += (generate_insert_statement("matches", row))
    return statements

sql_statements = []

sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/2/44.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/4.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/42.json")
sql_statements += convert_json_to_sql(f"../statsbomb_data/matches/11/90.json")

sql_statements = set(sql_statements)


with open("../insert_statements/matches.sql", "a", encoding='utf-8') as file:
    for statement in sql_statements:
        statement = statement.replace("None", "NULL")
        file.write(statement + "\n")