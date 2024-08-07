import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

def get_gameplay_link(driver, game_name):
    logger.info(f'Searching gameplay link for game: {game_name}')
    # Open YouTube
    driver.get("https://www.youtube.com")
    time.sleep(5)

    # Locate the search bar using CSS selector
    search_bar_css = "input#search"
    search_bar = driver.find_element(By.CSS_SELECTOR, search_bar_css)

    # Enter search query and perform the search
    search_query = f"{game_name} gameplay"
    search_bar.click()
    search_bar.send_keys(search_query)
    search_bar.send_keys(Keys.RETURN)
    logger.info(f'Entered search query: {search_query}')

    # Give the search results some time to load
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

    logger.info('Initializing Chrome driver for gameplay links.')
    driver = webdriver.Chrome(options=chrome_options)

    for game_info in game_info_list:
        game_name = game_info["name"]
        gameplay_link = get_gameplay_link(driver, game_name)
        game_info["gameplay_link"] = gameplay_link

    driver.quit()
    logger.info('Closed Chrome driver after fetching gameplay links.')

    return game_info_list
