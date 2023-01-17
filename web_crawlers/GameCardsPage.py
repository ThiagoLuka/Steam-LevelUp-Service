import requests

from .SteamWebPage import SteamWebPage


class GameCardsPage(SteamWebPage, name='game_cards_page'):

    @staticmethod
    def required_user_data() -> tuple:
        return 'steam_alias', 'game_market_id',

    @staticmethod
    def required_cookies() -> tuple:
        return ()

    def interact(self, cookies: dict, **kwargs) -> requests.Response:
        steam_alias: str = kwargs['steam_alias']
        game_market_id: str = kwargs['game_market_id']

        url = f'{super().BASESTEAMURL}id/{steam_alias}/gamecards/{game_market_id}'

        response = requests.get(url, cookies=cookies)
        return response
