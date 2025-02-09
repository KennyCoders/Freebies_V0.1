import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import dateutil.parser
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger  # Ensure this imports your Logger class

# Initialize logger
logger = Logger().get_logger()

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')

def get_game_info(game_element, driver):
    try:
        logger.info("Attempting to scrape game name.")
        game_name = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("alt")
        logger.info(f"Scraped game name: {game_name}")

        logger.info("Attempting to scrape game link.")
        game_link = game_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        logger.info(f"Scraped game link: {game_link}")

        logger.info("Attempting to scrape image source.")
        image_src = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("src")
        logger.info(f"Scraped image source: {image_src}")

        logger.info("Attempting to scrape availability text.")
        availability_span = game_element.find_element(By.XPATH, ".//span[contains(text(), 'Free')]")
        availability_text = availability_span.text
        logger.info(f"Scraped availability text: {availability_text}")

        logger.info("Attempting to scrape time elements.")
        time_elements = game_element.find_elements(By.TAG_NAME, "time")
        logger.info(f"Scraped time elements: {len(time_elements)} found.")

        if len(time_elements) >= 2:
            date_value = time_elements[0].get_attribute("datetime")
            time_value = time_elements[1].get_attribute("datetime")
            logger.info(f"Scraped date value: {date_value}, time value: {time_value}")

            date = dateutil.parser.parse(date_value).strftime("%b %d")
            time = dateutil.parser.parse(time_value).strftime("%I:%M %p")
            availability = f"{availability_text} until {date} at {time}"
        else:
            logger.warning("Insufficient time elements to parse availability.")
            availability = availability_text  # Fallback

        logger.info(f"Scraped availability: {availability}")

        return {
            "name": game_name,
            "link": game_link,
            "image_src": image_src,
            "availability": availability,
        }

    except Exception as e:
        logger.error(f"Error scraping game element: {str(e)}")
        return None


def scrape_epic_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # Initialize the WebDriver with the specified path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info('Initialized Chrome driver for Epic Games scraping.')

    game_info_list_with_links = []

    try:
        driver.get("https://store.epicgames.com/en-US/free-games")
        logger.info('Navigated to Epic Games Free Games page.')
        time.sleep(10)

        logger.info("Attempting to locate game elements.")
        game_elements = driver.find_elements(By.CSS_SELECTOR,
                                             "[data-component='VaultOfferCard'], [data-component='FreeOfferCard']")
        if not game_elements:
            logger.warning("No game elements found. Exiting scraping process.")
            return []

        logger.info(f"Located {len(game_elements)} game elements.")

        game_info_list = []

        for idx, game_element in enumerate(game_elements):
            logger.info(f"Processing game element {idx}: {game_element}")
            logger.info(f"Outer HTML of game element {idx}: {game_element.get_attribute('outerHTML')}")
            try:
                game_info = get_game_info(game_element, driver)
                if game_info:
                    game_info_list.append(game_info)
                    logger.info(f"Scraped info for game {idx}: {game_info}")
                else:
                    logger.warning(f"No data returned for game element {idx}")
            except Exception as e:
                logger.error(f"Error processing game element {idx}: {str(e)}")

        game_info_list_with_links = get_gameplay_links(game_info_list)

        for game_info in game_info_list_with_links:
            insert_game('epic', game_info)
            logger.info(f'Inserted game into database: {game_info}')

    except Exception as e:
        logger.error(f"An error occurred while scraping Epic Games: {str(e)}")

    finally:
        driver.quit()
        logger.info('Closed Chrome driver after scraping Epic Games.')

    logger.info('Scraping of Epic Games completed.')
    return game_info_list_with_links

