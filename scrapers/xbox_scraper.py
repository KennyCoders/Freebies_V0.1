import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

from webdriver_manager.chrome import ChromeDriverManager

from database.database_utils import insert_game
from scrapers.gameplay_scraper import get_gameplay_links
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

# Specify the path to your existing ChromeDriver
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')


def scrape_xbox_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # Initialize the WebDriver with the specified path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    logger.info('Initializing Chrome driver for Xbox games scraping.')
    driver.get("https://www.xbox.com/en-us/xbox-game-pass?xr=shellnav")
    logger.info('Navigated to Xbox Game Pass page.')

    game_info_list = []
    game_info_list_with_links = []

    try:
        # Wait for the game list to be present
        game_list = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 '/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/div/div/ul/li[position() >= 3 and position() <= 8]'))
        )

        logger.info(f'Found {len(game_list)} games on Xbox page.')

        for game_item in game_list:
            try:
                game_name_element = game_item.find_element(By.XPATH, './/a')
                game_name = game_name_element.get_attribute('aria-label').split('.')[0]
                game_link = game_name_element.get_attribute('href')

                try:
                    image_element = game_item.find_element(By.XPATH, './/img')
                    image_src = image_element.get_attribute('src')
                except NoSuchElementException:
                    image_src = None

                game_info = {
                    "name": game_name,
                    "link": game_link,
                    "image_src": image_src
                }
                game_info_list.append(game_info)

                # Debug: Print game name to the console
                print(f"Scraped game: {game_name}")

                logger.info(f'Scraped game: {game_name}')
            except NoSuchElementException as e:
                logger.error(f"Error finding element: {e}")

        game_info_list_with_links = get_gameplay_links(game_info_list)

        # Insert games into the database
        for game_info in game_info_list_with_links:
            insert_game('xbox', game_info)
            logger.info(f'Inserted game into database: {game_info}')

    except TimeoutException:
        logger.error("Timeout occurred while waiting for game list to load")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

    finally:
        driver.quit()
        logger.info('Closed Chrome driver after scraping Xbox games.')

    return game_info_list_with_links