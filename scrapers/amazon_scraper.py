from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

def scrape_amazon_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    logger.info('Initializing Chrome driver.')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://gaming.amazon.com/home")
    logger.info('Navigated to Amazon Gaming Home page.')
    time.sleep(5)

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

    game_cards = driver.find_elements(By.CSS_SELECTOR, 'div.item-card__action')
    logger.info(f'Found {len(game_cards)} game cards.')

    game_info_list = []
    counter = 0
    for game_card in game_cards:
        try:
            game_name = game_card.find_element(By.XPATH, './/a').get_attribute('aria-label')
            game_link = game_card.find_element(By.XPATH, './/a').get_attribute('href')
            image_src = game_card.find_element(By.CSS_SELECTOR, 'img.tw-image').get_attribute('src')
            time.sleep(2)
            logger.info(f'Scraped game: {game_name}')
        except NoSuchElementException as e:
            image_src = None
            logger.warning(f'Image not found for game: {game_name}, error: {e}')

        game_info_list.append({
            "name": game_name,
            "link": game_link,
            "image_src": image_src,
        })

        counter += 1
        if counter == 5:
            break

    game_info_list_with_links = get_gameplay_links(game_info_list)

    # Insert games into the database
    for game_info in game_info_list_with_links:
        insert_game('amazon', game_info)
        logger.info(f'Inserted game into database: {game_info}')

    logger.info('Scraping of Amazon games completed.')
    driver.quit()

    return game_info_list_with_links
