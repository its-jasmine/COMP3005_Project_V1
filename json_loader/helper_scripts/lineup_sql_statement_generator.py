
columns_names = ['goalkeeper', 'right_back', 'right_center_back', 'left_center_back', 'left_back', 'right_defensive_midfield', 'left_defensive_midfield', 'right_midfield', 'left_midfield', 'right_center_forward', 'left_center_forward']


def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS lineups \n" \
            "(goalkeeper            VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "right_back             INTEGER NOT NULL,  \n" \
            "right_center_back                INTEGER NOT NULL, \n" \
            "left_center_back               INTEGER NOT NULL, \n" \
            "left_back            TIME NOT NULL, \n" \
            "minute               INTEGER NOT NULL, \n" \
            "second               INTEGER NOT NULL, \n" \
            "type                 VARCHAR(255) NOT NULL, \n" \
            "possession            INTEGER NOT NULL, \n" \
            "possession_team_id    INTEGER NOT NULL, \n" \
            "play_pattern         VARCHAR(255) NOT NULL, \n" \
            "team_id              INTEGER, \n" \
            "duration             FLOAT, \n" \
            "location             INTEGER, \n" \
            "under_pressure       INTEGER, \n" \
            "off_camera           INTEGER, \n" \
            "out                  INTEGER, \n" \
            "related_events       INTEGER);"

