from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import dateutil.parser
import time
from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger
import re

# Initialize logger
logger = Logger().get_logger()

# Specify the path to your existing ChromeDriver
CHROME_DRIVER_PATH = r"C:\Users\shahartz\AppData\Local\Programs\Python\Python39\Scripts\chromedriver.exe"



def clean_text(text):
    # Regular expression pattern to keep only alphanumeric characters and spaces
    pattern = r'[^\w\s]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def get_game_info(game_element, driver):
    print("Getting game info...")
    game_name = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("alt")
    game_name = clean_text(game_name)  # Clean the game name
    print(f"Name: {game_name}")

    game_link = game_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    print(f"Link: {game_link}")

    image_url = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("src")
    print(f"Image URL: {image_url}")

    availability_span = game_element.find_element(By.CSS_SELECTOR, "p.eds_1ypbntd0.eds_1ypbntd9.eds_1ypbntdl")
    availability_text = availability_span.text
    print(f"Availability text: {availability_text}")

    time_elements = game_element.find_elements(By.TAG_NAME, "time")
    date_value = time_elements[0].get_attribute("datetime")
    time_value = time_elements[1].get_attribute("datetime")
    date = dateutil.parser.parse(date_value).strftime("%b %d")
    time = dateutil.parser.parse(time_value).strftime("%I:%M %p")
    availability = f"{availability_text} until {date} at {time}"
    print(f"Full availability: {availability}")

    return {
        "name": game_name,
        "link": game_link,
        "image_url": image_url,
        "availability": availability,
    }


def scrape_epic_games():
    print("Starting Epic Games scraper...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print('Navigating to Epic Games Store')
    driver.get("https://store.epicgames.com/en-US/free-games")

    game_info_list_with_links = []

    try:
        print("Waiting for game elements to be present...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[data-component='VaultOfferCard'], [data-component='FreeOfferCard']"))
        )

        print("Finding game elements...")
        game_elements = driver.find_elements(By.CSS_SELECTOR,
                                             "[data-component='VaultOfferCard'], [data-component='FreeOfferCard']")
        print(f"Found {len(game_elements)} game elements")

        game_info_list = []
        for i, game_element in enumerate(game_elements, 1):
            print(f"\nProcessing game {i}:")
            game_info = get_game_info(game_element, driver)
            print(f'Scraped game info: {game_info}')
            game_info_list.append(game_info)

        print("\nGetting gameplay links...")
        game_info_list_with_links = get_gameplay_links(game_info_list)

        print("\nInserting games into the database:")
        for game_info in game_info_list_with_links:
            insert_game('epic', game_info)
            print(f'Inserted game into database: {game_info}')

    except Exception as e:
        print(f"An error occurred while scraping Epic Games: {str(e)}")
        logger.error(f"An error occurred while scraping Epic Games: {str(e)}")

    finally:
        driver.quit()
        print('Closed Chrome driver after scraping Epic Games.')

    return game_info_list_with_links