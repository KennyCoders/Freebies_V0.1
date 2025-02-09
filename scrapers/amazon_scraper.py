import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

from webdriver_manager.chrome import ChromeDriverManager

from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')


def scrape_amazon_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # Initialize the WebDriver with the specified path
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info('Initializing Chrome driver for Amazon games scraping.')

    game_info_list_with_links = []  # Initialize to avoid UnboundLocalError

    try:
        driver.get("https://gaming.amazon.com/home")
        logger.info('Navigated to Amazon Gaming Home page.')
        time.sleep(5)

        # Click on Free Games button
        try:
            free_games_button = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/main/div/div/div/div[3]/div/div[1]/div/div[2]/button/div/div/p')
            free_games_button.click()
            logger.info('Clicked on Free Games button.')
            time.sleep(3)
        except NoSuchElementException as e:
            logger.error(f'Free Games button not found: {e}')
            driver.quit()
            return []

        # Set a maximum number of games to scrape
        max_games = 16
        game_info_list = []

        while len(game_info_list) < max_games:
            game_cards = driver.find_elements(By.CSS_SELECTOR, 'div.item-card__action')
            logger.info(f'Found {len(game_cards)} game cards.')

            for game_card in game_cards[len(game_info_list):]:  # Only process new cards
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", game_card)
                    time.sleep(1)  # Brief pause to allow loading

                    game_name = game_card.find_element(By.XPATH, './/a').get_attribute('aria-label')
                    game_link = game_card.find_element(By.XPATH, './/a').get_attribute('href')
                    image_src = game_card.find_element(By.CSS_SELECTOR, 'img.tw-image').get_attribute('src')
                    logger.info(f'Scraped game: {game_name}')

                    game_info_list.append({
                        "name": game_name,
                        "link": game_link,
                        "image_src": image_src,
                    })

                    if len(game_info_list) >= max_games:
                        break  # Stop if we've reached the max_games limit

                except NoSuchElementException as e:
                    logger.warning(f'Could not scrape game card: {e}')
                    continue

            # Scroll down to load more cards if necessary
            if len(game_info_list) < max_games:
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)  # Pause for new content to load

        # Get gameplay links and insert games into the database
        game_info_list_with_links = get_gameplay_links(game_info_list)
        for game_info in game_info_list_with_links:
            insert_game('amazon', game_info)
            logger.info(f'Inserted game into database: {game_info}')

    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping Amazon games: {str(e)}")

    finally:
        driver.quit()
        logger.info('Closed Chrome driver after scraping Amazon games.')

    logger.info('Scraping of Amazon games completed.')
    return game_info_list_with_links

