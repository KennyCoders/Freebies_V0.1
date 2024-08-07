import requests
from bs4 import BeautifulSoup
from database.database_utils import insert_game
from scrapers.gameplay_scraper import get_gameplay_links
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

def scrape_sony_games():
    url = "https://store.playstation.com/en-us/view/25d9b52a-7dcf-11ea-acb6-06293b18fe04/bc428b4a-f1b7-11ea-aadc-062143ad1e8d"
    logger.info(f'Starting to scrape Sony games from URL: {url}')
    response = requests.get(url)

    if response.status_code == 200:
        logger.info('Successfully fetched the Sony store page.')
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        games_list = soup.find('ul', {'class': 'psw-strand-scroller'})
        game_info_list = []

        for game_item in games_list.find_all('li'):
            game_name = game_item.find('span', {'data-qa': lambda val: val and 'product-name' in val}).text
            game_link = "https://store.playstation.com" + game_item.find('a', {'data-qa': ''})['href']
            game_image_link = game_item.find('img', {'data-qa': lambda val: val and 'game-art#image#image' in val})['src']
            game_info_list.append({
                'name': game_name,
                'link': game_link,
                'image_src': game_image_link
            })
            logger.info(f'Scraped game: {game_name}')

        game_info_list_with_links = get_gameplay_links
