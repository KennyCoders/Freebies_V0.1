import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

# Define the ChromeDriver path
CHROME_DRIVER_PATH = r'C:\Users\shahartz\AppData\Local\Programs\Python\Python39\Scripts\chromedriver.exe'


def get_gameplay_link(driver, game_name):
    logger.info(f'Searching gameplay link for game: {game_name}')

    # Open YouTube
    driver.get("https://www.youtube.com")

    # Wait for the search bar to be visible
    search_bar_css = "input#search"
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, search_bar_css))
    )

    # Enter search query and perform the search
    search_query = f"{game_name} gameplay"
    search_bar.click()
    search_bar.send_keys(search_query)
    search_bar.send_keys(Keys.RETURN)
    logger.info(f'Entered search query: {search_query}')

    # Wait for search results to load
    time.sleep(3)

    # Simulate right-click to open context menu (assuming pyautogui for demonstration)
    pyautogui.moveTo(307, 550)
    pyautogui.click()
    time.sleep(3)

    gameplay_link = driver.current_url
    logger.info(f'Found gameplay link: {gameplay_link} for game: {game_name}')
    return gameplay_link


def get_gameplay_links(game_info_list):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    service = Service(CHROME_DRIVER_PATH)

    logger.info('Initializing Chrome driver for gameplay links.')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for game_info in game_info_list:
            game_name = game_info["name"]
            gameplay_link = get_gameplay_link(driver, game_name)
            game_info["gameplay_link"] = gameplay_link
    except Exception as e:
        logger.error(f"An error occurred while getting gameplay links: {str(e)}")
    finally:
        driver.quit()
        logger.info('Closed Chrome driver after fetching gameplay links.')

    return game_info_list