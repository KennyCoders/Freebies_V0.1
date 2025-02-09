import requests
from bs4 import BeautifulSoup
from database.database_utils import insert_game
from scrapers.gameplay_scraper import get_gameplay_links
from logger import Logger

# Initialize logger
logger = Logger().get_logger()


def scrape_sony_games():
    url = "https://www.playstation.com/en-us/ps-plus/whats-new/"
    logger.info(f'Starting to scrape Sony games from URL: {url}')
    print(f'Starting to scrape Sony games from URL: {url}')

    try:
        response = requests.get(url)
        logger.info('Fetching URL...')
        print('Fetching URL...')

        if response.status_code == 200:
            logger.info('Successfully fetched the Sony store page.')
            print('Successfully fetched the Sony store page.')
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all game boxes
            game_info_list = []
            game_boxes = soup.find_all('div', class_='box--light')

            if game_boxes:
                logger.info(f'Found {len(game_boxes)} game boxes.')
                print(f'Found {len(game_boxes)} game boxes.')

                for game_box in game_boxes:
                    try:
                        # Extract image source
                        image_src = game_box.find('div', class_='media-block')['data-src']
                        # Extract game name
                        game_name = game_box.find('h3', class_='txt-style-medium-title').text.strip()
                        # Extract game link using data-uuid
                        game_link = "https://store.playstation.com" + game_box.find('a', {'data-uuid': True})['href']

                        game_info_list.append({
                            'name': game_name,
                            'link': game_link,
                            'image_src': image_src
                        })

                        logger.info(f'Scraped game: {game_name}, Link: {game_link}')
                        print(f'Scraped game: {game_name}, Link: {game_link}')

                    except Exception as e:
                        logger.error(f'Error scraping game item: {e}')
                        print(f'Error scraping game item: {e}')
            else:
                logger.warning('No game boxes found.')
                print('No game boxes found.')

        else:
            logger.error(f'Failed to fetch the Sony store page. Status code: {response.status_code}')
            print(f'Failed to fetch the Sony store page. Status code: {response.status_code}')

    except Exception as e:
        logger.error(f'Error during the request: {e}')
        print(f'Error during the request: {e}')

    # Process gameplay links if needed
    try:
        game_info_list_with_links = get_gameplay_links(game_info_list)
        logger.info('Successfully retrieved gameplay links.')
        print('Successfully retrieved gameplay links.')

        # Insert games into the database
        for game_info in game_info_list_with_links:
            insert_game('sony', game_info)
            logger.info(f'Inserted game into database: {game_info}')
            print(f'Inserted game into database: {game_info}')

    except Exception as e:
        logger.error(f'Error getting gameplay links: {e}')
        print(f'Error getting gameplay links: {e}')

    print('Scraping of Sony games completed.')
    logger.info('Scraping of Sony games completed.')


