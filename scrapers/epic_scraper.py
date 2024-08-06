import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import dateutil.parser
import time
from scrapers.gameplay_scraper import get_gameplay_links
from database.database_utils import insert_game



def get_game_info(game_element, driver):
    game_name = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("alt")
    game_link = game_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    image_url = game_element.find_element(By.CSS_SELECTOR, "img[data-testid='picture-image']").get_attribute("src")

    availability_span = game_element.find_element(By.XPATH, ".//div[contains(@class, 'css-y2j3ic')]/span")
    availability_text = availability_span.text

    time_elements = game_element.find_elements(By.TAG_NAME, "time")
    date_value = time_elements[0].get_attribute("datetime")
    time_value = time_elements[1].get_attribute("datetime")
    date = dateutil.parser.parse(date_value).strftime("%b %d")
    time = dateutil.parser.parse(time_value).strftime("%I:%M %p")
    availability = f"{availability_text} until {date} at {time}"


    return {
        "name": game_name,
        "link": game_link,
        "image_url": image_url,
        "availability": availability,
    }


def scrape_epic_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://store.epicgames.com/en-US/free-games")
    time.sleep(10)

    game_elements = driver.find_elements(By.CSS_SELECTOR,
                                         "[data-component='VaultOfferCard'], [data-component='FreeOfferCard']")

    game_info_list = []
    for game_element in game_elements:
        game_info = get_game_info(game_element, driver)
        game_info_list.append(game_info)

    game_info_list = [get_game_info(game_element, driver) for game_element in game_elements]

    game_info_list_with_links = get_gameplay_links(game_info_list)

    # Insert games into the database
    for game_info in game_info_list_with_links:
        insert_game('epic', game_info)

    driver.quit()

    return game_info_list_with_links