from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from logging.handlers import RotatingFileHandler
import os
from urllib.parse import urlparse, parse_qs

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')

# Initialize logger with proper file handling
def setup_logger():
    logger = logging.getLogger('gameplay_scraper')
    logger.setLevel(logging.INFO)

    # Create a new handler with a lock file
    log_file = 'scraper.log'
    handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,
        backupCount=5,
        delay=True
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()


def extract_video_id(youtube_url):
    """
    Extracts the video ID from a YouTube URL.
    Supports standard watch URLs and Shorts URLs.
    """
    if 'v=' in youtube_url:
        # Standard YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
        parsed_url = urlparse(youtube_url)
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]
    elif '/shorts/' in youtube_url:
        # YouTube Shorts URL (e.g., https://www.youtube.com/shorts/VIDEO_ID)
        video_id = youtube_url.split('/shorts/')[1].split('?')[0]
    else:
        # Invalid or unsupported URL
        video_id = None

    return video_id


def get_gameplay_link(driver, game_name):
    print(f"\n=== Starting search for {game_name} ===")
    logger.info(f'Searching gameplay link for game: {game_name}')

    # Navigate to YouTube
    print("Navigating to YouTube...")
    driver.get("https://www.youtube.com")

    # Find and interact with search bar
    print("Looking for search bar...")
    search_bar_css = 'input[name="search_query"]'
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, search_bar_css))
    )

    # Perform search
    search_query = f"{game_name} gameplay"
    print(f"Entering search query: {search_query}")
    search_bar.click()
    search_bar.send_keys(search_query)
    search_bar.send_keys(Keys.RETURN)

    # Wait for search results to load
    print("Waiting for search results to load...")
    time.sleep(3)

    # Find all video thumbnails
    print("Looking for video thumbnails...")
    video_thumbnails = driver.find_elements(By.CSS_SELECTOR, 'a#thumbnail')

    if len(video_thumbnails) < 2:
        print("Not enough videos found.")
        return None

    # Select the second video (index 1 since lists are zero-based)
    gameplay_link = video_thumbnails[1].get_attribute('href')
    print(f"Selected gameplay link: {gameplay_link}")

    # Extract video ID and construct embed URL
    video_id = extract_video_id(gameplay_link)
    if video_id:
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        print(f"Generated embed URL: {embed_url}")
        return embed_url
    else:
        print("Failed to extract video ID from URL.")
        return None


def get_gameplay_links(game_info_list):
    print("\n=== Starting gameplay link collection process ===")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    service = Service(CHROME_DRIVER_PATH)
    print("Initializing Chrome driver...")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for game_info in game_info_list:
            game_name = game_info["name"]
            print(f"\nProcessing game: {game_name}")
            gameplay_link = get_gameplay_link(driver, game_name)
            game_info["gameplay_link"] = gameplay_link
            print(f"Saved gameplay link for {game_name}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        logger.error(f"An error occurred while getting gameplay links: {str(e)}")
    finally:
        print("\nClosing Chrome driver...")
        driver.quit()

    return game_info_list