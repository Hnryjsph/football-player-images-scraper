import scrapy
import pandas as pd

file_path = r'C:\Users\user\Desktop\scraper\questionScraper\questionScraper\spiders\Euro2024_Images.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load all sheets into a dictionary of DataFrames
sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}


def get_player_names(sheet):
    # Assuming the player names are in a column named 'Player'
    player_names = sheet['Player Name'].dropna().tolist()
    # print(player_names)
    return player_names


sheet_name = xls.sheet_names[0]
player_names = get_player_names(sheets[sheet_name])


class QscraperSpider(scrapy.Spider):
    name = "qScraper"
    allowed_domains = ["transfermarkt.com"]

    start_urls = [f"https://transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={player.replace(' ', '+')}" for
                  player in player_names]

    def parse(self, response):
        tables = response.css("tbody")
        players = tables.css("tr")

        name_of_player = players[0].css("td  a::attr(title)")[0].get()

        link = players[0].css("td  a::attr(href)")[1].get()

        yield response.follow(link, callback=self.download_link)

    def download_link(self, response):
        club_image = response.css("header div.data-header__box--big a img::attr(srcset)").get()
        player_image = response.css("header div.data-header__profile-container div.modal-trigger img::attr(src)").get()
        player_name = response.css("header h1.data-header__headline-wrapper strong::text").get()
        clean_club_image = club_image.split("\n")[2].strip().replace("2x", "").strip()

        yield {'player_name': player_name, 'club_image': clean_club_image, 'player_image': player_image}
