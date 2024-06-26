# Created by Gabriel Martell

'''
Version 1.2 (04/13/2024)
=========================================================
queries.py (Carleton University COMP3005 - Database Management Student Template Code)

This is the template code for the COMP3005 Database Project 1, and must be accomplished on an Ubuntu Linux environment.
Your task is to ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

You may modify code in terms of testing purposes (commenting out a Qn method), however, any alterations to the code, such as modifying the time, 
will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean. 

To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 

=========================================================
'''

# Imports
import psycopg
import csv
import subprocess
import os
import re

# Connection Information
''' 
The following is the connection information for this project. These settings are used to connect this file to the autograder.
You must NOT change these settings - by default, db_host, db_port and db_username are as follows when first installing and utilizing psql.
For the user "postgres", you must MANUALLY set the password to 1234.

This can be done with the following snippet:

sudo -u postgres psql
\password postgres

'''
root_database_name = "project_database"
query_database_name = "query_database"
db_username = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '5432'

# Directory Path - Do NOT Modify
dir_path = os.path.dirname(os.path.realpath(__file__))

# Loading the Database after Drop - Do NOT Modify
#================================================
def load_database(conn):
    drop_database(conn)

    cursor = conn.cursor()
    # Create the Database if it DNE
    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {query_database_name};")
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        conn.autocommit = False
    conn.close()
    
    # Connect to this query database.
    dbname = query_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Import the dbexport.sql database data into this database
    try:
        command = f'psql -h {host} -U {user} -d {query_database_name} -a -f "{os.path.join(dir_path, "dbexport.sql")}" > /dev/null 2>&1'
        env = {'PGPASSWORD': password}
        subprocess.run(command, shell=True, check=True, env=env)

    except Exception as error:
        print(f"An error occurred while loading the database: {error}")
    
    # Return this connection.
    return conn    

# Dropping the Database after Query n Execution - Do NOT Modify
#================================================
def drop_database(conn):
    # Drop database if it exists.

    cursor = conn.cursor()

    try:
        conn.autocommit = True
        cursor.execute(f"DROP DATABASE IF EXISTS {query_database_name};")
        conn.commit()

    except Exception as error:
        print(error)
        pass

    finally:
        cursor.close()
        conn.autocommit = False

# Reconnect to Root Database - Do NOT Modify
#================================================
def reconnect():
    dbname = root_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    return psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Getting the execution time of the query through EXPLAIN ANALYZE - Do NOT Modify
#================================================
def get_time(cursor, sql_query):
    # Prefix your query with EXPLAIN ANALYZE
    explain_query = f"EXPLAIN ANALYZE {sql_query}"

    try:
        # Execute the EXPLAIN ANALYZE query
        cursor.execute(explain_query)
        
        # Fetch all rows from the cursor
        explain_output = cursor.fetchall()
        
        # Convert the output tuples to a single string
        explain_text = "\n".join([row[0] for row in explain_output])
        
        # Use regular expression to find the execution time
        # Look for the pattern "Execution Time: <time> ms"
        match = re.search(r"Execution Time: ([\d.]+) ms", explain_text)
        if match:
            execution_time = float(match.group(1))
            return f"Execution Time: {execution_time} ms"
        else:
            print("Execution Time not found in EXPLAIN ANALYZE output.")
            return f"NA"
        
    except Exception as error:
        print(f"[ERROR] Error getting time.\n{error}")


# Write the results into some Q_n CSV. If the is an error with the query, it is a INC result - Do NOT Modify
#================================================
def write_csv(execution_time, cursor, i):
    # Collect all data into this csv, if there is an error from the query execution, the resulting time is INC.
    try:
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        filename = f"{dir_path}/Q_{i}.csv"

        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write column names to the CSV file
            csvwriter.writerow(colnames)
            
            # Write data rows to the CSV file
            csvwriter.writerows(rows)

    except Exception as error:
        execution_time[i-1] = "INC"
        print(error)
    
#================================================
        
'''
The following 10 methods, (Q_n(), where 1 < n < 10) will be where you are tasked to input your queries.
To reiterate, any modification outside of the query line will be flagged, and then marked as potential cheating.
Once you run this script, these 10 methods will run and print the times in order from top to bottom, Q1 to Q10 in the terminal window.
'''
def Q_1(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    WITH 
        SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'La Liga' AND SEASON_NAME = '2020/2021'),
            
        PLAYERS_XG_SCORES_IN_SEASON AS (
            SELECT PLAYER_ID, STATSBOMB_XG
            FROM (SHOT JOIN EVENTS ON SHOT.EVENT_ID = EVENTS.EVENT_ID) NATURAL JOIN SEASON_MATCH_IDS
            WHERE STATSBOMB_XG > 0),
    
        PLAYERS_AVG_XG_SCORES AS (
            SELECT PLAYER_ID, AVG(STATSBOMB_XG) AS AVG_XG_SCORE
            FROM PLAYERS_XG_SCORES_IN_SEASON
            GROUP BY PLAYER_ID)
    SELECT PLAYER_NAME, AVG_XG_SCORE
    FROM PLAYERS_AVG_XG_SCORES NATURAL JOIN PLAYERS
    ORDER BY AVG_XG_SCORE DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[0] = (time_val)

    write_csv(execution_time, cursor, 1)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_2(conn, execution_time):

    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    SELECT PLAYER_NAME, SHOT_COUNT
    FROM
        (SELECT PLAYER_ID, COUNT (*) AS SHOT_COUNT
            FROM (
                    (SELECT MATCH_ID, PLAYER_ID
                        FROM EVENTS
                        WHERE EVENTS.TYPE = 'Shot') AS PLAYER_SHOTS
                NATURAL JOIN
                    (SELECT MATCH_ID
                        FROM COMPETITIONS
                        NATURAL JOIN MATCHES
                        WHERE COMPETITION_NAME = 'La Liga'
                            AND SEASON_NAME = '2020/2021') AS SEASON_MATCH_IDS)
            GROUP BY PLAYER_ID)
    NATURAL JOIN PLAYERS
    ORDER BY SHOT_COUNT DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[1] = (time_val)

    write_csv(execution_time, cursor, 2)

    cursor.close()
    new_conn.close()

    return reconnect()
    
def Q_3(conn, execution_time):

    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    SELECT PLAYER_NAME, SHOT_COUNT
    FROM
        (SELECT PLAYER_ID, COUNT (*) AS SHOT_COUNT
            FROM (
                    (SELECT MATCH_ID, PLAYER_ID
                        FROM EVENTS, SHOT
                        WHERE EVENTS.EVENT_ID = SHOT.EVENT_ID AND SHOT.FIRST_TIME = 'true'
                        ) AS PLAYER_SHOTS
                NATURAL JOIN
                    (SELECT MATCH_ID
                        FROM COMPETITIONS
                        NATURAL JOIN MATCHES
                        WHERE COMPETITION_NAME = 'La Liga'
                            AND SEASON_NAME in ('2018/2019', '2019/2020', '2020/2021')) AS SEASON_MATCH_IDS)
            GROUP BY PLAYER_ID)
    NATURAL JOIN PLAYERS
    ORDER BY SHOT_COUNT DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[2] = (time_val)

    write_csv(execution_time, cursor, 3)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_4(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ 
    WITH 
	    SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'La Liga' AND SEASON_NAME = '2020/2021'
        ),

        PASSES_MADE AS (
            SELECT MATCH_ID, TEAM_ID
            FROM EVENTS INNER JOIN PASS ON EVENTS.EVENT_ID = PASS.EVENT_ID
        ),
        
        PASSES_MADE_PER_TEAM AS (
            SELECT TEAM_ID, count(*) AS PASS_COUNT
            FROM PASSES_MADE NATURAL JOIN SEASON_MATCH_IDS
            GROUP BY TEAM_ID
        )

    SELECT teams.TEAM_NAME, PASS_COUNT
    FROM PASSES_MADE_PER_TEAM NATURAL JOIN TEAMS
    ORDER BY PASS_COUNT DESC;"""

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[3] = (time_val)

    write_csv(execution_time, cursor, 4)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_5(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    WITH
        SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'Premier League' AND SEASON_NAME = '2003/2004'
        ),

        RECIPIENT_OF_PASSES AS (
            SELECT RECIPIENT_ID, COUNT(*) AS PASS_RECIPIENT_COUNT
            FROM (EVENTS INNER JOIN PASS ON EVENTS.EVENT_ID = PASS.EVENT_ID) NATURAL JOIN SEASON_MATCH_IDS
            GROUP BY RECIPIENT_ID
        )

    SELECT PLAYER_NAME, PASS_RECIPIENT_COUNT
    FROM RECIPIENT_OF_PASSES INNER JOIN PLAYERS ON PLAYERS.PLAYER_ID = RECIPIENT_ID
    ORDER BY PASS_RECIPIENT_COUNT DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[4] = (time_val)

    write_csv(execution_time, cursor, 5)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_6(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    SELECT TEAM_NAME, SHOT_COUNT
    FROM
        (SELECT TEAM_ID, COUNT (*) AS SHOT_COUNT
            FROM (
                    (SELECT MATCH_ID, TEAM_ID
                        FROM EVENTS
                        WHERE EVENTS.TYPE = 'Shot') AS TEAM_SHOTS
                NATURAL JOIN
                    (SELECT MATCH_ID
                        FROM COMPETITIONS
                        NATURAL JOIN MATCHES
                        WHERE COMPETITION_NAME = 'Premier League'
                            AND SEASON_NAME = '2003/2004') AS SEASON_MATCH_IDS)
            GROUP BY TEAM_ID)
    NATURAL JOIN TEAMS
    ORDER BY SHOT_COUNT DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[5] = (time_val)

    write_csv(execution_time, cursor, 6)

    cursor.close()
    new_conn.close()

    return reconnect()


def Q_7(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    WITH 
        SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'La Liga' AND SEASON_NAME = '2020/2021'),
            
        THROUGH_BALLS AS (
            SELECT EVENT_ID
            FROM PASS
            WHERE THROUGH_BALL = TRUE),
        
        THROUGH_BALLS_IN_SEASON AS (
            SELECT PLAYER_ID, COUNT(*) AS NUM_THROUGH_BALLS
            FROM ((THROUGH_BALLS NATURAL JOIN EVENTS) NATURAL JOIN SEASON_MATCH_IDS)
            GROUP BY PLAYER_ID)

    SELECT PLAYER_NAME, NUM_THROUGH_BALLS
    FROM THROUGH_BALLS_IN_SEASON NATURAL JOIN PLAYERS
    ORDER BY NUM_THROUGH_BALLS DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[6] = (time_val)

    write_csv(execution_time, cursor, 7)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_8(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    SELECT TEAM_NAME, THROUGH_BALL_COUNT
    FROM
        (SELECT TEAM_ID, COUNT (*) AS THROUGH_BALL_COUNT
            FROM (
                    (SELECT MATCH_ID, TEAM_ID
                        FROM EVENTS, PASS
                        WHERE EVENTS.EVENT_ID = PASS.EVENT_ID AND PASS.THROUGH_BALL = true
                        ) AS TEAM_PASSES
                NATURAL JOIN
                    (SELECT MATCH_ID
                        FROM COMPETITIONS
                        NATURAL JOIN MATCHES
                        WHERE COMPETITION_NAME = 'La Liga'
                            AND SEASON_NAME = '2020/2021') AS SEASON_MATCH_IDS)
            GROUP BY TEAM_ID)
    NATURAL JOIN TEAMS
    ORDER BY THROUGH_BALL_COUNT DESC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[7] = (time_val)

    write_csv(execution_time, cursor, 8)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_9(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    WITH
        SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS
            NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'La Liga' AND SEASON_NAME in ('2018/2019', '2019/2020', '2020/2021')
        ),

        SUCCESSFUL_DRIBBLES AS (
            SELECT PLAYER_ID, COUNT(*) AS SUCCESSFUL_DRIBBLE_COUNT
            FROM (EVENTS NATURAL JOIN DRIBBLE) NATURAL JOIN SEASON_MATCH_IDS
            WHERE DRIBBLE.OUTCOME = 'Complete'
            GROUP BY PLAYER_ID
        )

    SELECT PLAYER_NAME, SUCCESSFUL_DRIBBLE_COUNT
    FROM SUCCESSFUL_DRIBBLES NATURAL JOIN PLAYERS 
    ORDER BY SUCCESSFUL_DRIBBLE_COUNT DESC;"""

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[8] = (time_val)

    write_csv(execution_time, cursor, 9)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_10(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    WITH 
        SEASON_MATCH_IDS AS (
            SELECT MATCH_ID
            FROM COMPETITIONS NATURAL JOIN MATCHES
            WHERE COMPETITION_NAME = 'La Liga' AND SEASON_NAME = '2020/2021'),
            
        DRIBBLE_PAST_IN_SEASON AS (
            SELECT PLAYER_ID
            FROM (DRIBBLE_PAST NATURAL JOIN EVENTS) NATURAL JOIN SEASON_MATCH_IDS),
        
        PLAYERS_NUM_DRIBBLES_PAST AS (
            SELECT PLAYER_ID, COUNT(*) AS NUM_DRIBBLE_PAST
            FROM DRIBBLE_PAST_IN_SEASON
            GROUP BY PLAYER_ID)

    SELECT PLAYER_NAME, NUM_DRIBBLE_PAST
    FROM PLAYERS_NUM_DRIBBLES_PAST NATURAL JOIN PLAYERS
    ORDER BY NUM_DRIBBLE_PAST ASC;
    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[9] = (time_val)

    write_csv(execution_time, cursor, 10)

    cursor.close()
    new_conn.close()

    return reconnect()

# Running the queries from the Q_n methods - Do NOT Modify
#=====================================================
def run_queries(conn):

    execution_time = [0,0,0,0,0,0,0,0,0,0]

    conn = Q_1(conn, execution_time)
    conn = Q_2(conn, execution_time)
    conn = Q_3(conn, execution_time)
    conn = Q_4(conn, execution_time)
    conn = Q_5(conn, execution_time)
    conn = Q_6(conn, execution_time)
    conn = Q_7(conn, execution_time)
    conn = Q_8(conn, execution_time)
    conn = Q_9(conn, execution_time)
    conn = Q_10(conn, execution_time)

    for i in range(10):
        print(execution_time[i])

''' MAIN '''
try:
    if __name__ == "__main__":

        dbname = root_database_name
        user = db_username
        password = db_password
        host = db_host
        port = db_port

        conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        run_queries(conn)
except Exception as error:
    print(error)
    #print("[ERROR]: Failure to connect to database.")
#_______________________________________________________
