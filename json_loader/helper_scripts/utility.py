file_path = "output" 
global match_id_list
match_id_list = []
with open(file_path, 'r') as file:
    file.seek(0)  # Move the file pointer back to the beginning
    for line in file:

        match_id = line.strip()
        match_id_list.append(match_id)
        