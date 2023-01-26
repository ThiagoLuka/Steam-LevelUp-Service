import requests

from web_crawlers import SteamWebCrawler
from web_page_cleaning.ItemMarketPageCleaner import ItemMarketPageCleaner


class CheckItemMarketUrlName:

    def __init__(self, web_crawler: SteamWebCrawler):
        self.__crawler = web_crawler

    def run(self, **additional_info) -> str:
        verified_url_name = self.__trading_card(**additional_info)

        return verified_url_name

    def __trading_card(self, **additional_info) -> str:
        card_name: str = additional_info['card_name']
        game_market_id: str = additional_info['game_market_id']

        card_url_name = requests.utils.quote(f'{card_name}')
        url_valid: bool = self.__item_url_is_valid(game_market_id, card_url_name)
        if url_valid:
            return card_url_name

        card_name_with_parenthesis = f'{card_name} (Trading Card)'
        card_url_name = requests.utils.quote(f'{card_name_with_parenthesis}')
        url_valid: bool = self.__item_url_is_valid(game_market_id, card_url_name)
        if url_valid:
            return card_url_name

        return ''

    def __item_url_is_valid(self, game_market_id: str, item_url_name: str) -> bool:
        custom_status_code, response = self.__crawler.interact(
            'item_market_page',
            game_market_id=game_market_id,
            item_url_name=item_url_name,
        )
        page_cleaner = ItemMarketPageCleaner(response.content)
        return page_cleaner.item_url_is_valid()
