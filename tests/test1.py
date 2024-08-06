from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyautogui




def get_gameplay_link(driver, game_name):
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

    # Give the search results some time to load
    time.sleep(3)

    # Simulate right-click to open context menu (assuming pyautogui for demonstration)
    pyautogui.moveTo(307, 550)
    pyautogui.click()
    time.sleep(3)
    gameplay_link = driver.current_url


    return gameplay_link

def scrape_amazon_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://gaming.amazon.com/home")
    time.sleep(5)

    free_games_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div/div/div[3]/div/div[1]/div/div[2]/button/div/div/p')
    free_games_button.click()
    time.sleep(3)

    game_cards = driver.find_elements(By.CSS_SELECTOR, 'div.item-card__action')

    game_info_list = []
    counter = 0
    for game_card in game_cards:
        game_name = game_card.find_element(By.XPATH, './/a').get_attribute('aria-label')
        game_link = game_card.find_element(By.XPATH, './/a').get_attribute('href')
        try:
            image_src = game_card.find_element(By.CSS_SELECTOR, 'img.tw-image').get_attribute('src')
        except NoSuchElementException:
            image_src = None
        time.sleep(4)

        game_info_list.append({
            "name": game_name,
            "link": game_link,
            "image_src": image_src
        })

        counter += 1
        if counter == 15:
            break

    driver.quit()


    return game_info_list


def get_gameplay_links(game_info_list):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    for game_info in game_info_list:
        game_name = game_info["name"]
        gameplay_link = get_gameplay_link(driver, game_name)
        game_info["gameplay_link"] = gameplay_link

    driver.quit()

    return game_info_list

if __name__ == "__main__":
    game_info_list = scrape_amazon_games()
    game_info_list_with_links = get_gameplay_links(game_info_list)

    for game_info in game_info_list_with_links:
        print(f"Game Name: {game_info['name']}")
        print(f"Game Link: {game_info['link']}")
        print(f"Image Source: {game_info['image_src']}")
        print(f"Gameplay Link: {game_info['gameplay_link']}")
        print("\n")


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# import time
#
# # Initialize WebDriver
# driver = webdriver.Chrome()
#
# # JavaScript to track mouse movement
# mouse_tracker_js = """
# document.addEventListener('mousemove', function(event) {
#     window.mouseX = event.clientX;
#     window.mouseY = event.clientY;
# });
# """
#
# # Function to get mouse coordinates from the browser
# def get_mouse_coordinates():
#     x = driver.execute_script("return window.mouseX;")
#     y = driver.execute_script("return window.mouseY;")
#     return x, y
#
# # Open YouTube
# driver.get("https://www.youtube.com")
#
# # Inject the JavaScript for mouse tracking
# driver.execute_script(mouse_tracker_js)
#
# # Continuously log mouse coordinates every second
# try:
#     while True:
#         x, y = get_mouse_coordinates()
#         print(f"Mouse Coordinates: X={x}, Y={y}")
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Stopped by user")
#
# # Close the browser
# driver.quit()
#
#
#
# #=======================
#
# from flask import Flask, render_template
# from scrapers.amazon_scraper import scrape_amazon_games
# from scrapers.epic_scraper import scrape_epic_games
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     amazon_games = scrape_amazon_games()
#     epic_games = scrape_epic_games()
#
#     # Print game name and gameplay link for Amazon games
#     for game in amazon_games:
#         print(f"Amazon Game: {game['name']}, Gameplay Link: {game['gameplay_link']}")
#
#     # Print game name and gameplay link for Epic games
#     for game in epic_games:
#         print(f"Epic Game: {game['name']}, Gameplay Link: {game['gameplay_link']}")
#
#     return render_template('index.html', amazon_games=amazon_games, epic_games=epic_games)
#
# if __name__ == '__main__':
#     app.run(debug=True)