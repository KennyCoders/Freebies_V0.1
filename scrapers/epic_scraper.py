
from selenium import webdriver
from selenium.webdriver.common.by import By
import dateutil.parser
import time
from selenium.webdriver.chrome.service import Service
from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger  # Ensure this imports your Logger class

# Initialize logger
logger = Logger().get_logger()


def get_game_info(game_element, driver):
    game_name = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("alt")
    game_link = game_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    image_src = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("src")

    availability_span = game_element.find_element(By.XPATH, ".//span[contains(text(), 'Free')]")
    availability_text = availability_span.text

    time_elements = game_element.find_elements(By.TAG_NAME, "time")
    date_value = time_elements[0].get_attribute("datetime")
    time_value = time_elements[1].get_attribute("datetime")
    date = dateutil.parser.parse(date_value).strftime("%b %d")
    time = dateutil.parser.parse(time_value).strftime("%I:%M %p")
    availability = f"{availability_text} until {date} at {time}"

    logger.info(f'Scraped game info: {game_name}, link: {game_link}, availability: {availability}')

    return {
        "name": game_name,
        "link": game_link,
        "image_src": image_src,
        "availability": availability,
    }


def scrape_epic_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # Use the specific ChromeDriver path
    service = Service(r'C:\Users\shahartz\AppData\Local\Programs\Python\Python39\Scripts\chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info('Initialized Chrome driver for Epic Games scraping.')

    try:
        driver.get("https://store.epicgames.com/en-US/free-games")
        logger.info('Navigated to Epic Games Free Games page.')
        time.sleep(10)

        game_elements = driver.find_elements(By.CSS_SELECTOR,
                                             "[data-component='VaultOfferCard'], [data-component='FreeOfferCard']")

        logger.info(f'Found {len(game_elements)} game elements to scrape.')
        game_info_list = []

        for game_element in game_elements:
            game_info = get_game_info(game_element, driver)
            game_info_list.append(game_info)

        game_info_list_with_links = get_gameplay_links(game_info_list)

        # Insert games into the database
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
