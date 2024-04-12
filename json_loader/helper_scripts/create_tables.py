def generate_create_statement_competitions():
    return "CREATE TABLE IF NOT EXISTS competitions \n" \
           "(competition_id     INTEGER NOT NULL, \n" \
           "season_id           INTEGER NOT NULL,  \n" \
           "competition_name    VARCHAR(255) NOT NULL, \n" \
           "season_name         VARCHAR(255) NOT NULL, \n" \
           "competition_gender  VARCHAR(255) NOT NULL, \n" \
           "country             VARCHAR(255) NOT NULL, \n" \
           "PRIMARY KEY (competition_id, season_id));"

def generate_create_statement_lineups():
    return "CREATE TABLE IF NOT EXISTS lineups \n" \
            "(match_id                 INTEGER NOT NULL, \n" \
            "team_id                   INTEGER NOT NULL,  \n" \
            "player_id                 INTEGER NOT NULL,  \n" \
            "PRIMARY KEY (match_id, team_id),  \n" \
            "FOREIGN KEY (match_id) REFERENCES matches(match_id),  \n" \
            "FOREIGN KEY (team_od) REFERENCES teams(team_id),  \n" \
            "FOREIGN KEY (player_id) REFERENCES players(player_id) );"


def generate_create_statement_position():
    return "CREATE TABLE IF NOT EXISTS positions \n" \
            "(match_id                 INTEGER NOT NULL, \n" \
            "team_id                   INTEGER NOT NULL,  \n" \
            "player_id                 INTEGER NOT NULL,  \n" \
            "position_id               INTEGER NOT NULL, \n" \
            "position_name             VARCHAR(255) NOT NULL,  \n" \
            "from_time                 VARCHAR(255),  \n" \
            "to_time                   VARCHAR(255),  \n" \
            "from_period               INTEGER,  \n" \
            "to_period                 INTEGER,  \n" \
            "start_reason              VARCHAR(255) NOT NULL,  \n" \
            "end_reason                VARCHAR(255) NOT NULL,  \n" \
            "PRIMARY KEY (match_id, team_id), \n" \
            "FOREIGN KEY (match_id) REFERENCES matches(match_id),  \n" \
            "FOREIGN KEY (team_od) REFERENCES teams(team_id),  \n" \
            "FOREIGN KEY (player_id) REFERENCES players(player_id) );"

def generate_create_statement_pass():
    return "CREATE TABLE IF NOT EXISTS pass \n" \
           "(event_id           VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "recepient_id        INTEGER,  \n" \
           "length              FLOAT,  \n" \
           "angle               FLOAT, \n" \
           "height              VARCHAR(255), \n" \
           "end_location_x      FLOAT, \n" \
           "end_location_y      FLOAT, \n" \
           "assisted_shot_id    VARCHAR(255), \n"\
           "deflected           BOOLEAN, \n" \
           "miscommunication    BOOLEAN, \n"\
           "cross_              BOOLEAN, \n"\
           "switch              BOOLEAN, \n"\
           "shot_assist         BOOLEAN, \n" \
           "goal_assist         BOOLEAN, \n"\
           "body_part           VARCHAR(255), \n"\
           "type                VARCHAR(255), \n"\
           "outcome             VARCHAR(255), \n"\
           "technique           VARCHAR(255),  \n" \
           "through_ball        BOOLEAN, \n"\
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_teams():
    return "CREATE TABLE IF NOT EXISTS teams \n" \
           "(team_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "team_name    VARCHAR(255) NOT NULL, \n" \
           "team_gender  VARCHAR(255) NOT NULL, \n" \
           "team_group   VARCHAR(255),  \n" \
           "team_country VARCHAR(255) NOT NULL);"

def generate_create_statement_managers():
    return "CREATE TABLE IF NOT EXISTS managers \n" \
           "(manager_id           INTEGER NOT NULL, \n" \
           "manager_name          VARCHAR(255) NOT NULL, \n" \
           "manager_nickname      VARCHAR(255), \n" \
           "dob                   DATE NOT NULL, \n" \
           "country               VARCHAR(255) NOT NULL, \n" \
           "team_id               INTEGER NOT NULL, \n" \
           "PRIMARY KEY (manager_id, team_id),  \n" \
           "FOREIGN KEY (team_id) REFERENCES teams(team_id));"

def generate_create_statement_players():
    return "CREATE TABLE IF NOT EXISTS players \n" \
           "(player_id      INTEGER NOT NULL PRIMARY KEY, \n" \
           "player_name     VARCHAR(255) NOT NULL,  \n" \
           "player_nickname VARCHAR(255), \n" \
           "jersey_number   INTEGER NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_create_statement_referees():
    return "CREATE TABLE IF NOT EXISTS referees \n" \
           "(referee_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "referee_name    VARCHAR(255) NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_create_statement_stadiums():
    return "CREATE TABLE IF NOT EXISTS stadiums \n" \
           "(stadium_id     INTEGER NOT NULL PRIMARY KEY, \n" \
           "stadium_name    VARCHAR(255) NOT NULL, \n" \
           "country         VARCHAR(255) NOT NULL);"

def generate_create_statement_matches():
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

def generate_create_statement_events():
    return "CREATE TABLE IF NOT EXISTS events \n" \
            "(event_id            VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "match_id             INTEGER NOT NULL,  \n" \
            "index                INTEGER NOT NULL, \n" \
            "period               INTEGER NOT NULL, \n" \
            "timestamp            TIME NOT NULL, \n" \
            "minute               INTEGER NOT NULL, \n" \
            "second               INTEGER NOT NULL, \n" \
            "type                 VARCHAR(255) NOT NULL, \n" \
            "possession            INTEGER NOT NULL, \n" \
            "possession_team_id    INTEGER NOT NULL, \n" \
            "play_pattern         VARCHAR(255) NOT NULL, \n" \
            "team_id              INTEGER, \n" \
            "duration             FLOAT, \n" \
            "location_x             FLOAT, \n" \
            "location_y             FLOAT, \n" \
            "under_pressure       BOOLEAN, \n" \
            "off_camera           BOOLEAN, \n" \
            "out                  BOOLEAN, \n" \
            "player_id            INTEGER, \n" \
            "FOREIGN KEY (match_id) REFERENCES matches(match_id), \n" \
            "FOREIGN KEY (team_id) REFERENCES teams(team_id), \n" \
            "FOREIGN KEY (player_id) REFERENCES players(player_id), \n" \
            "FOREIGN KEY (possession_team_id) REFERENCES teams(team_id));"

def generate_create_statement_ball_recovery():
    return "CREATE TABLE IF NOT EXISTS ball_recovery \n" \
            "(event_id            VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "offensive            BOOLEAN,  \n" \
            "recovery_failure     BOOLEAN,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_dribble():
    return "CREATE TABLE IF NOT EXISTS dribble \n" \
            "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "overrun      BOOLEAN,  \n" \
            "nutmeg       BOOLEAN,  \n" \
            "outcome      VARCHAR(255),  \n" \
            "no_touch     BOOLEAN,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_shot():
    return "CREATE TABLE IF NOT EXISTS shot \n" \
            "(event_id         VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "key_pass_id       VARCHAR(255),  \n" \
            "end_location_x    FLOAT,  \n" \
            "end_location_y    FLOAT,  \n" \
            "end_location_z    FLOAT,  \n" \
            "aerial_won        BOOLEAN,  \n" \
            "follows_dribble   BOOLEAN,  \n" \
            "first_time        BOOLEAN,  \n" \
            "open_goal         BOOLEAN,  \n" \
            "statsbomb_xg      FLOAT,  \n" \
            "deflected         BOOLEAN,  \n" \
            "technique         VARCHAR(255),  \n" \
            "body_part         VARCHAR(255),  \n" \
            "type              VARCHAR(255),  \n" \
            "outcome           VARCHAR(255),  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_injury_stoppage():
    return "CREATE TABLE IF NOT EXISTS injury_stoppage \n" \
            "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "in_chain     BOOLEAN,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_ball_receipt():
    return "CREATE TABLE IF NOT EXISTS ball_receipt \n" \
            "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "outcome      VARCHAR(255),  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_substitution():
    return "CREATE TABLE IF NOT EXISTS substitution \n" \
            "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "replacement    VARCHAR(255),  \n" \
            "outcome        VARCHAR(255),  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_starting_xi():
    return "CREATE TABLE IF NOT EXISTS starting_xi \n" \
            "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "formation    INTEGER,  \n" \
            "lineup_id    INTEGER,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id),  \n" \
            "FOREIGN KEY (lineup_id) REFERENCES lineups(lineup_id));"

def generate_create_statement_tactical_shift():
    return "CREATE TABLE IF NOT EXISTS tactical_shift \n" \
            "(event_id    VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "formation    INTEGER,  \n" \
            "lineup_id    INTEGER,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id),  \n" \
            "FOREIGN KEY (lineup_id) REFERENCES lineups(lineup_id));"

def generate_create_statement_50_50():
    return "CREATE TABLE IF NOT EXISTS fifty_fifty \n" \
            "(event_id          VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "outcome            VARCHAR(255),  \n" \
            "counterpress       BOOLEAN,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"


def generate_create_statement_block():
    return "CREATE TABLE IF NOT EXISTS block \n" \
           "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "deflection      BOOLEAN,  \n" \
           "offensive       BOOLEAN,  \n" \
           "save_block      BOOLEAN,  \n" \
           "counterpress    BOOLEAN,  \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_interception():
    return "CREATE TABLE IF NOT EXISTS interception \n" \
           "(event_id          VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "outcome            VARCHAR(255) NOT NULL,  \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_bad_behaviour():
    return "CREATE TABLE IF NOT EXISTS bad_behaviour \n" \
           "(event_id        VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "card             VARCHAR(255) NOT NULL,  \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_player_off(): # TODO confirm whether including?
    return ""

def generate_create_statement_half_end(): # TODO confirm whether including?
    return ""

def generate_create_statement_carry():
    return "CREATE TABLE IF NOT EXISTS carry \n" \
            "(event_id        VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "end_location_x             INTEGER NOT NULL, \n" \
            "end_location_y             INTEGER NOT NULL,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_foul_won():
    return "CREATE TABLE IF NOT EXISTS foul_won \n" \
            "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
            "defensive      BOOLEAN,  \n" \
            "advantage       BOOLEAN,  \n" \
            "penalty      BOOLEAN,  \n" \
            "FOREIGN KEY (event_id) REFERENCES events(event_id));"


def generate_create_statement_clearance():
    return "CREATE TABLE IF NOT EXISTS clearance \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "aerial_won     BOOLEAN, \n" \
           "body_part      VARCHAR(255),  \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_goal_keeper():
    return "CREATE TABLE IF NOT EXISTS goal_keeper \n" \
           "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "position        VARCHAR(255), \n" \
           "end_location_x  FLOAT, \n" \
           "end_location_y  FLOAT, \n" \
           "technique       VARCHAR(255), \n" \
           "body_part       VARCHAR(255), \n" \
           "type            VARCHAR(255), \n" \
           "outcome         VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_foul_committed():
    return "CREATE TABLE IF NOT EXISTS foul_committed \n" \
           "(event_id       VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress    VARCHAR(255), \n" \
           "offensive       BOOLEAN, \n" \
           "type            VARCHAR(255), \n" \
           "advantage       BOOLEAN, \n" \
           "penalty         VARCHAR(255), \n" \
           "card            VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_miscontrol():
    return "CREATE TABLE IF NOT EXISTS miscontrol \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "aerial_won     BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_dribble_past():
    return "CREATE TABLE IF NOT EXISTS dribble_past \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_pressure():
    return "CREATE TABLE IF NOT EXISTS pressure \n" \
           "(event_id      VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "counterpress   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_half_start():
    return "CREATE TABLE IF NOT EXISTS half_start \n" \
           "(event_id          VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "late_video_start   BOOLEAN, \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

def generate_create_statement_duel():
    return "CREATE TABLE IF NOT EXISTS duel \n" \
           "(event_id   VARCHAR(255) NOT NULL PRIMARY KEY, \n" \
           "type        VARCHAR(255), \n" \
           "outcome     VARCHAR(255), \n" \
           "FOREIGN KEY (event_id) REFERENCES events(event_id));"

create_statements = []
create_statements.append(generate_create_statement_teams())
create_statements.append(generate_create_statement_competitions())
create_statements.append(generate_create_statement_stadiums())
create_statements.append(generate_create_statement_managers())
create_statements.append(generate_create_statement_referees())
create_statements.append(generate_create_statement_matches())
create_statements.append(generate_create_statement_players())
create_statements.append(generate_create_statement_lineups())
create_statements.append(generate_create_statement_position())
create_statements.append(generate_create_statement_events())
create_statements.append(generate_create_statement_clearance())
create_statements.append(generate_create_statement_dribble_past())
create_statements.append(generate_create_statement_duel())
create_statements.append(generate_create_statement_foul_committed())
create_statements.append(generate_create_statement_goal_keeper())
create_statements.append(generate_create_statement_half_start())
create_statements.append(generate_create_statement_miscontrol())
create_statements.append(generate_create_statement_pressure())
create_statements.append(generate_create_statement_shot())
create_statements.append(generate_create_statement_50_50())
create_statements.append(generate_create_statement_bad_behaviour())
create_statements.append(generate_create_statement_tactical_shift())
create_statements.append(generate_create_statement_ball_receipt())
create_statements.append(generate_create_statement_ball_recovery())
create_statements.append(generate_create_statement_injury_stoppage())
create_statements.append(generate_create_statement_substitution())
create_statements.append(generate_create_statement_starting_xi())
create_statements.append(generate_create_statement_block())
create_statements.append(generate_create_statement_interception())
create_statements.append(generate_create_statement_carry())
create_statements.append(generate_create_statement_foul_won())
create_statements.append(generate_create_statement_dribble())
create_statements.append(generate_create_statement_player_off())
create_statements.append(generate_create_statement_pass())
with open("../insert_statements/ddl.sql", "a", encoding='utf-8') as file:
    for statement in create_statements:
        file.write(statement + "\n")