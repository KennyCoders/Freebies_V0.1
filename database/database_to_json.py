import sqlite3
import json
import os
from datetime import datetime, timedelta

# Paths to the database and JSON files
db_path = r"C:\Users\shahartz\PycharmProjects\Freebees_Versions\FreeGamesWebsiteDatabase-Copy(code)\database\games.db"
json_file_path = r'C:\Users\shahartz\PycharmProjects\Freebees_Versions\Freebee\games.json'

# Check if the database exists
if not os.path.exists(db_path):
    print(f"Error: The database file was not found at the path: {db_path}")
    exit(1)  # Exit the script if the database is not found

# Database connection


# Fetch all games from the database for the current week (Sunday as the start of the week)
def fetch_all_games_for_current_week():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Load existing JSON data if it exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {'games': []}
    else:
        existing_data = {'games': []}

    # Create a set of existing game titles for quick lookup
    existing_titles = {game['title'] for game in existing_data['games']}

    # Fetch data from each table and append to the games_data
    for table in ['amazon_games', 'epic_games', 'sony_games', 'xbox_games']:
        try:
            c.execute(f"SELECT name, link, image_src, gameplay_link, scraped_date FROM {table}")
            rows = c.fetchall()

            for row in rows:
                # Only add the game if it's not already in the JSON
                if row[0] not in existing_titles:
                    game = {
                        'title': row[0],
                        'link': row[1],
                        'image': row[2],
                        'trailer': row[3],
                        'date': row[4],
                        'platform': table  # Add the platform name
                    }
                    existing_data['games'].append(game)
                    existing_titles.add(row[0])
                    print(f"Added new game: {row[0]}")
        except sqlite3.OperationalError as e:
            print(f"Error: The table '{table}' does not exist in the database. Error: {e}")

    conn.close()
    return existing_data

# Write data to JSON file
def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Successfully updated JSON file at: {file_path}")

# Main logic
try:
    print("Starting game data update process...")
    games_data = fetch_all_games_for_current_week()
    write_json(games_data, json_file_path)
    print("Update process completed successfully!")
except Exception as e:
    print(f"An error occurred during the update process: {e}")




# Close the database connection
