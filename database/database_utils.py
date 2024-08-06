import sqlite3
import datetime
import os

db_path = os.path.join('database', 'games.db')


# Database connection
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create tables
def create_tables():
    # Amazon table
    c.execute("""CREATE TABLE IF NOT EXISTS amazon_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        link TEXT,
        image_src TEXT,
        gameplay_link TEXT,
        scraped_date TEXT
    )""")

    # Epic Games table
    c.execute("""CREATE TABLE IF NOT EXISTS epic_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        link TEXT,
        image_url TEXT,
        availability TEXT,
        gameplay_link TEXT,
        scraped_date TEXT
    )""")

    # Sony Games table
    c.execute("""CREATE TABLE IF NOT EXISTS sony_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        link TEXT,
        image_src TEXT,
        gameplay_link TEXT,
        scraped_date TEXT
    )""")

    # Xbox Games table
    c.execute("""CREATE TABLE IF NOT EXISTS xbox_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            link TEXT,
            image_src TEXT,
            gameplay_link TEXT,
            scraped_date TEXT
        )""")
    conn.commit()
# Insert a new game into the corresponding table
def insert_game(platform, game_info):
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    if platform == 'amazon':
        try:
            c.execute("INSERT INTO amazon_games (name, link, image_src, gameplay_link, scraped_date) VALUES (?, ?, ?, ?, ?)",
                      (game_info['name'], game_info['link'], game_info['image_src'], game_info['gameplay_link'], current_date))
        except sqlite3.IntegrityError:
            print(f"Game '{game_info['name']}' already exists in the amazon_games table.")
    elif platform == 'epic':
        try:
            c.execute("INSERT INTO epic_games (name, link, image_url, availability, gameplay_link, scraped_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (game_info['name'], game_info['link'], game_info['image_url'], game_info['availability'], game_info['gameplay_link'], current_date))
        except sqlite3.IntegrityError:
            print(f"Game '{game_info['name']}' already exists in the epic_games table.")
    elif platform == 'sony':
        try:
            c.execute("INSERT INTO sony_games (name, link, image_src, gameplay_link, scraped_date) VALUES (?, ?, ?, ?, ?)",
                      (game_info['name'], game_info['link'], game_info['image_src'], game_info['gameplay_link'], current_date))
        except sqlite3.IntegrityError:
            print(f"Game '{game_info['name']}' already exists in the sony_games table.")

    elif platform == 'xbox':
        try:
            c.execute("INSERT INTO xbox_games (name, link, image_src, gameplay_link, scraped_date) VALUES (?, ?, ?,?, ?)",
                      (game_info['name'], game_info['link'], game_info['image_src'], game_info['gameplay_link'], current_date))
        except sqlite3.IntegrityError:
            print(f"Game '{game_info['name']}' already exists in the xbox_games table.")
    conn.commit()

# Other database operations (read, update, delete) can be added here

# Close the database connection
def close_connection():
    conn.close()

# Create the tables
create_tables()