import requests

def download_file(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file: {url}")

def main():
    file_path = 'output'

    with open(file_path, 'r') as file:
        file.seek(0)  
        for line in file:
            match_id = line.strip()
            file_url = f'https://raw.githubusercontent.com/statsbomb/open-data/0067cae166a56aa80b2ef18f61e16158d6a7359a/data/lineups/{match_id}.json'
            local_file_path = f'../statsbomb_data/lineups/{match_id}.json'
            download_file(file_url, local_file_path)


if __name__ == "__main__":
    main()
