import json


def get_values_by_key(json_data, target_key):
    values = []
    if isinstance(json_data, dict):
        if target_key in json_data:
            values.append(json_data[target_key])
        for value in json_data.values():
            values.extend(get_values_by_key(value, target_key))
    elif isinstance(json_data, list):
        for item in json_data:
            values.extend(get_values_by_key(item, target_key))
    return values


def write_values_to_file(values, file_path):
    try:
        with open(file_path, 'a') as file:
            for value in values:
                file.write(str(value) + '\n')
        print(f"Values have been written to '{file_path}' successfully.")
    except IOError:
        print("Error writing to file.")

def main():

    paths = [
        "statsbomb_data/matches/2/44.json",
        "statsbomb_data/matches/11/42.json",
        "statsbomb_data/matches/11/90.json",
        "statsbomb_data/matches/11/4.json"
    ]

    target_key = "match_id"

    try:
        for json_file_path in paths:
            with open(json_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                data = json.load(file)
                values = get_values_by_key(data, target_key)

                print(f"file: {json_file_path}, Values for key '{target_key}': {values}")
                write_values_to_file(values, "output")

    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError as e:
        print("Invalid JSON format.", e)
    except UnicodeDecodeError as e:
        print("Invalid unicode format.", e)




if __name__ == "__main__":
    main()
