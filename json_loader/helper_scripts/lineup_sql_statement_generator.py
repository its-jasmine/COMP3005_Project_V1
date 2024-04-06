
columns_names = ['goalkeeper', 'right_back', 'right_center_back', 'left_center_back', 'left_back', 'right_defensive_midfield', 'left_defensive_midfield', 'right_midfield', 'left_midfield', 'right_center_forward', 'left_center_forward']


def generate_create_statement():
    return "CREATE TABLE IF NOT EXISTS lineups \n" \
            "(lineup_id                 INTEGER NOT NULL PRIMARY KEY, \n" \
            "goalkeeper                 INTEGER NOT NULL,  \n" \
            "right_back                 INTEGER NOT NULL,  \n" \
            "right_center_back          INTEGER NOT NULL, \n" \
            "left_center_back           INTEGER NOT NULL, \n" \
            "left_back                  INTEGER NOT NULL, \n" \
            "right_defensive_midfield   INTEGER NOT NULL, \n" \
            "left_defensive_midfield    INTEGER NOT NULL, \n" \
            "right_midfield             INTEGER NOT NULL, \n" \
            "left_midfield              INTEGER NOT NULL, \n" \
            "right_center_forward       INTEGER NOT NULL, \n" \
            "left_center_forward        INTEGER NOT NULL);"

