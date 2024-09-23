from scrapers.amazon_scraper import scrape_amazon_games
from scrapers.epic_scraper import scrape_epic_games
from scrapers.sony_scraper import scrape_sony_games
from scrapers.xbox_scraper import scrape_xbox_games
from database.database_utils import close_connection
from logger import Logger

# Initialize logger
logger = Logger().get_logger()

def test_scrapers():
    # logger.info('Starting to scrape Xbox games.')
    # xbox_games = scrape_xbox_games()
    # logger.info(f'Finished scraping Xbox games: {xbox_games}')
    #
    # logger.info('Starting to scrape Sony games.')
    # sony_games = scrape_sony_games()
    # logger.info(f'Finished scraping Sony games: {sony_games}')
    #
    # logger.info('Starting to scrape Amazon games.')
    # amazon_games = scrape_amazon_games()
    # logger.info(f'Finished scraping Amazon games: {amazon_games}')

    logger.info('Starting to scrape Epic games.')
    epic_games = scrape_epic_games()
    logger.info(f'Finished scraping Epic games: {epic_games}')

if __name__ == '__main__':
    logger.info('Starting the scraping process.')
    test_scrapers()
    close_connection()  # Close the database connection
    logger.info('Scraping process finished and database connection closed.')