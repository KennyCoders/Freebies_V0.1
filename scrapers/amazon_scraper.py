from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

def scrape_amazon_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # Use the specific ChromeDriver path
    service = Service(r'C:\Users\shahartz\AppData\Local\Programs\Python\Python39\Scripts\chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    print('Initializing Chrome driver for Amazon games scraping.')
    logger.info('Initializing Chrome driver for Amazon games scraping.')

    try:
        driver.get("https://gaming.amazon.com/home")
        print('Navigated to Amazon Gaming Home page.')
        logger.info('Navigated to Amazon Gaming Home page.')
        time.sleep(5)

        try:
            free_games_button = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/main/div/div/div/div[3]/div/div[1]/div/div[2]/button/div/div/p')
            free_games_button.click()
            print('Clicked on Free Games button.')
            logger.info('Clicked on Free Games button.')
            time.sleep(3)
        except NoSuchElementException as e:
            print(f'Free Games button not found: {e}')
            logger.error(f'Free Games button not found: {e}')
            driver.quit()
            return []

        game_cards = driver.find_elements(By.CSS_SELECTOR, 'div.item-card__action')
        print(f'Found {len(game_cards)} game cards.')
        logger.info(f'Found {len(game_cards)} game cards.')

        game_info_list = []
        counter = 0
        for game_card in game_cards:
            try:
                game_name = game_card.find_element(By.XPATH, './/a').get_attribute('aria-label')
                game_link = game_card.find_element(By.XPATH, './/a').get_attribute('href')
                time.sleep(3)
                image_src = game_card.find_element(By.CSS_SELECTOR, 'img.tw-image').get_attribute('src')
                print(f'Scraped game: {game_name}')
                logger.info(f'Scraped game: {game_name}')
            except NoSuchElementException as e:
                image_src = None
                print(f'Image not found for game: {game_name}, error: {e}')
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
            print(f'Inserted game into database: {game_info}')
            logger.info(f'Inserted game into database: {game_info}')

    except Exception as e:
        print(f"An unexpected error occurred while scraping Amazon games: {str(e)}")
        logger.error(f"An unexpected error occurred while scraping Amazon games: {str(e)}")

    finally:
        driver.quit()
        print('Closed Chrome driver after scraping Amazon games.')
        logger.info('Closed Chrome driver after scraping Amazon games.')

    print('Scraping of Amazon games completed.')
    logger.info('Scraping of Amazon games completed.')
    return game_info_list_with_links
