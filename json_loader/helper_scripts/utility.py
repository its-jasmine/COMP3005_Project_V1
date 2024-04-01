file_path = "output" 
global match_id_list
match_id_list = []
with open(file_path, 'r') as file:
    file.seek(0)  # Move the file pointer back to the beginning
    for line in file:

        match_id = line.strip()
        match_id_list.append(match_id)

import psycopg
global conn
try:
    conn = psycopg.connect(
        dbname="University", #fill in with database name
        user="postgres",
        password="nivetha", #fill in with password
        host="localhost",
        port="5432"
    )
except psycopg.OperationalError as e:
    print(f"Error: {e}")
    exit(1)
        
def execute_query(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit() #commit the data to the database