import json

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
           "posession            INTEGER NOT NULL, \n" \
           "posession_team_id    INTEGER NOT NULL, \n" \
           "play_pattern         VARCHAR(255) NOT NULL, \n" \
           "team_id              INTEGER, \n" \
           "duration             FLOAT, \n" \
           "location             INTEGER, \n" \
           "under_pressure       INTEGER, \n" \
           "off_camera           INTEGER, \n" \
           "out                  INTEGER, \n" \
           "related_events       INTEGER);"

# match_id = name of file
# I'm confused