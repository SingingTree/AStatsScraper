from future.moves.urllib.parse import urlparse
import re
import scrapy
from astatsscraper.items import AstatsSteamappItem
from astatsscraper.items import OwnedAppItem
from astatsscraper.items import SteampoweredSteamappItem


def parse_app_page(response):
    # Extract app id from URL
    app_id = int(response.url[len('https://astats.astats.nl/astats/Steam_Game_Info.php?AppID='):])
    # Should always be able to grab a title
    title = response.xpath('//div[@class = "panel panel-default panel-gameinfo"]/div[@class = "panel-heading"]/text()').extract_first().strip()
    # TIme may or may not be present
    time_to_hundo = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Hours to 100%"]/text()[last()]')
    if not time_to_hundo:
        time_to_hundo = 0
    else:
        # If time is present parse it to a float
        time_to_hundo = time_to_hundo.extract_first().strip()
        time_to_hundo = time_to_hundo.replace('.', '')
        time_to_hundo = time_to_hundo.replace(',', '.')
        time_to_hundo = float(time_to_hundo)
    # Points may or may not be present, default to 0 if absent
    points = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Points"]/text()[last()]').extract_first()
    if not points:
        points = 0
    else:
        points = int(points.strip())
    # Players should always be present, but guard edge case
    num_players = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Players"]/text()[last()]').extract_first()
    if not num_players:
        num_players = 0
    else:
        num_players = int(num_players.strip())
    num_players_to_hundo = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Players 100%"]/text()[last()]').extract_first()
    if not num_players_to_hundo:
        num_players_to_hundo = 0
    else:
        num_players_to_hundo = int(num_players_to_hundo.strip())

    yield AstatsSteamappItem({
        'app_id': app_id,
        'title': title,
        'time_to_100': time_to_hundo,
        'total_points': points,
        'num_players': num_players,
        'num_players_to_100': num_players_to_hundo,
        })


def parse_search_result_for_apps(response):
    for href in response.xpath('//table//table//a/@href'):
        relative_url = href.extract()
        if relative_url.startswith('Steam_Game_Info.php?AppID='):
            yield AstatsSteamappItem({
                'app_id': relative_url[len('Steam_Game_Info.php?AppID='):]
            })


def parse_search_result_for_next_page(response):
    return urlparse.urljoin(response.url, response.xpath('//table[@class="Pager"]//ul[@class="pagination"]/li/a[text()=">"]/@href').extract_first())


def parse_search_result_for_apps_recursive(response):
    next_page_url = parse_search_result_for_next_page(response)
    for app in parse_search_result_for_apps(response):
        yield app
    if next_page_url:
        yield scrapy.Request(next_page_url, parse_search_result_for_apps_recursive)


def parse_owned_games_for_apps(response):
    relative_url_app_prefix = 'User_Achievements_Per_Game.php?AppID='
    relative_url_owner_prefix = 'SteamID64='
    for table_cell in response.xpath('//table//table[td/@align="left"]'):
        number_achieved_and_total = table_cell.xpath('tr/td/p/font/text()').extract_first()
        number_achieved = int(number_achieved_and_total.split(' ')[0])
        name_and_percentage = table_cell.xpath('td/p/font/text()').extract_first()
        try:
            percentage_achieved = int(name_and_percentage.split(' ')[-1][:-1])
        except ValueError:
            percentage_achieved = None
        href = table_cell.xpath('tr/a/@href')
        relative_url = href.extract_first()
        owner_id = relative_url[relative_url.find(relative_url_owner_prefix) + len('SteamID64='):]
        app_id = int(relative_url[len(relative_url_app_prefix):relative_url.find(relative_url_owner_prefix) - 1])
        if relative_url.startswith(relative_url_app_prefix):
            yield OwnedAppItem({
                'owner_id': owner_id,
                # Find url and trim prefix
                'app_id': app_id,
                # Find percentage and trim '%' char
                'percentage_achieved': percentage_achieved,
                # Find number achieved out of total
                'number_achieved': number_achieved
            })


def parse_steam_powered_app_page(response):
    """Find ratings on steam powered pages and extract the percentage value, stripping the '%' char."""
    app_id_re = re.compile(r'[/](\d+)[/]?$')
    matches = app_id_re.search(response.url)
    if matches:
        app_id = int(matches.group(1))
    else:
        print("Couldn't find app id in: " + response.url)
        return
    review_text = response.xpath('//div[@class="user_reviews"]/div[@class="user_reviews_summary_row"]/@data-tooltip-text')

    def parse_rating(rating_text):
        first_word = rating_text.split(' ')[0]
        if first_word == "Need":
            # "Need more user reviews to generate a score"
            return None
        return int(first_word.strip('%'))

    if len(review_text) == 2:
        recent_rating = parse_rating(review_text[0].extract())
        overall_rating = parse_rating(review_text[1].extract())
    else:
        recent_rating = None
        overall_rating = parse_rating(review_text[0].extract())
    yield SteampoweredSteamappItem({
        'app_id': app_id,
        'recent_rating': recent_rating,
        'overall_rating': overall_rating
    })
