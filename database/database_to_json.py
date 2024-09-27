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

    games_data = {'games': []}
    current_date = datetime.now()

    # Calculate the difference in days from Sunday (weekday() returns 6 for Sunday)
    # If it's Sunday (weekday() == 6), no adjustment needed
    start_of_week = current_date - timedelta(days=(current_date.weekday() + 1) % 7)  # Adjusts to Sunday start
    start_of_week_str = start_of_week.strftime('%Y-%m-%d')

    # Fetch data from each table and append to the games_data
    for table in ['amazon_games', 'epic_games', 'sony_games', 'xbox_games']:
        try:
            c.execute(f"SELECT name, link, image_src, gameplay_link, scraped_date FROM {table} WHERE scraped_date >= ?", (start_of_week_str,))
            rows = c.fetchall()
            for row in rows:
                game = {
                    'title': row[0],
                    'link': row[1],
                    'image': row[2],
                    'trailer': row[3],
                    'date': row[4],
                    'platform': table  # Add the platform name
                }
                games_data['games'].append(game)
        except sqlite3.OperationalError:
            print(f"Error: The table '{table}' does not exist in the database.")
    conn.close()

    return games_data

# Write data to JSON file
def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Main logic
games_data = fetch_all_games_for_current_week()
write_json(games_data, json_file_path)

# Close the database connection
