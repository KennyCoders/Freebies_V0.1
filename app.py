from scrapers.amazon_scraper import scrape_amazon_games
from scrapers.epic_scraper import scrape_epic_games
from scrapers.sony_scraper import scrape_sony_games
from scrapers.xbox_scraper import scrape_xbox_games
from database.database_utils import close_connection


def test_scrapers():
    xbox_games = scrape_xbox_games()
    sony_games = scrape_sony_games()
    amazon_games = scrape_amazon_games()
    epic_games = scrape_epic_games()




if __name__ == '__main__':
    test_scrapers()
    close_connection()  # Close the database connection