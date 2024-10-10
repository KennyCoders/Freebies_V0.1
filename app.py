import os
import subprocess
import sys
from datetime import datetime
import sqlite3
from scrapers.amazon_scraper import scrape_amazon_games
from scrapers.epic_scraper import scrape_epic_games
from scrapers.sony_scraper import scrape_sony_games
from scrapers.xbox_scraper import scrape_xbox_games
from database.database_to_json import fetch_all_games_for_current_week, write_json
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

# Path to your folders
SCRAPER_FOLDER = r"C:\Users\shahartz\PycharmProjects\Freebees_Versions\FreeGamesWebsiteDatabase-Copy(code)"
WEBSITE_FOLDER = r"C:\Users\shahartz\PycharmProjects\Freebees_Versions\Freebee"
JSON_FILE = "games.json"  # Name of the JSON file to be pushed
DB_PATH = r"C:\Users\shahartz\PycharmProjects\Freebees_Versions\FreeGamesWebsiteDatabase-Copy(code)\database\games.db"

# ... (other functions remain the same)

def convert_db_to_json():
    logger.info('Starting database to JSON conversion.')
    print('Starting database to JSON conversion.')  # Added print statement

    # Ensure the database file exists
    if not os.path.exists(DB_PATH):
        logger.error(f"Error: Database file not found at {DB_PATH}")
        print(f"Error: Database file not found at {DB_PATH}")  # Added print statement
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        games_data = fetch_all_games_for_current_week()
        print(f"Fetched {len(games_data)} games from the database.")  # Added print statement
    except sqlite3.Error as e:
        logger.error(f"Error during database connection: {e}")
        print(f"Error during database connection: {e}")  # Added print statement
        sys.exit(1)
    finally:
        if conn:
            conn.close()

    # Path for the JSON file
    json_file_path = os.path.join(WEBSITE_FOLDER, JSON_FILE)

    # Write JSON data
    write_json(games_data, json_file_path)
    logger.info(f'JSON file created at: {json_file_path}')
    print(f'JSON file created at: {json_file_path}')  # Added print statement
    return json_file_path

def push_json_to_github(json_file_path):
    print(f"Changing directory to {WEBSITE_FOLDER}")
    os.chdir(WEBSITE_FOLDER)

    if not os.path.exists(json_file_path):
        logger.error(f"Error: {JSON_FILE} not found in {WEBSITE_FOLDER}")
        print(f"Error: {JSON_FILE} not found in {WEBSITE_FOLDER}")
        sys.exit(1)

    try:
        # Check if there are changes to the JSON file
        logger.info("Checking for changes to the JSON file.")
        print("Checking for changes to the JSON file.")
        result = subprocess.run(["git", "status", "--porcelain", JSON_FILE], capture_output=True, text=True, check=True)
        logger.info(f"Git status output: {result.stdout.strip()}")
        print(f"Git status output: {result.stdout.strip()}")

        if result.stdout.strip():
            # Changes exist, commit and push only the JSON file
            logger.info("Changes detected, preparing to commit and push.")
            print("Changes detected, preparing to commit and push.")
            subprocess.run(["git", "add", JSON_FILE], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Update {JSON_FILE} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            logger.info(f"Changes to {JSON_FILE} pushed to GitHub")
            print(f"Changes to {JSON_FILE} pushed to GitHub")
        else:
            logger.info(f"No changes to {JSON_FILE} to push")
            print(f"No changes to {JSON_FILE} to push")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while pushing to GitHub: {e}")
        print(f"An error occurred while pushing to GitHub: {e}")
        sys.exit(1)

def scrape_games():

    logger.info('Starting to scrape Xbox games.')
    xbox_games = scrape_xbox_games()
    logger.info(f'Finished scraping Xbox games: {xbox_games}')

    logger.info('Starting to scrape Sony games.')
    sony_games = scrape_sony_games()
    logger.info(f'Finished scraping Sony games: {sony_games}')

    logger.info('Starting to scrape Amazon games.')
    amazon_games = scrape_amazon_games()
    logger.info(f'Finished scraping Amazon games: {amazon_games}')

    logger.info('Starting to scrape Epic games.')
    epic_games = scrape_epic_games()
    logger.info(f'Finished scraping Epic games: {epic_games}')


def main():
    logger.info('Starting the scraping and updating process.')
    print('Starting the scraping and updating process.')  # Added print statement

    scrape_games()

    try:
        # Convert the DB to JSON
        json_file_path = convert_db_to_json()

        # Push the JSON to GitHub
        push_json_to_github(json_file_path)

        logger.info('Process completed successfully.')
        print('Process completed successfully.')  # Added print statement
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")  # Added print statement
        sys.exit(1)

if __name__ == "__main__":
    main()