from typing import Any

from web_crawlers.SteamWebPage import SteamWebPage
from web_crawlers.InventoryPage import InventoryPage
from web_crawlers.ProfileBadgesPage import ProfileBadgesPage
from web_crawlers.OpenBoosterPack import OpenBoosterPack
from web_crawlers.GameCardsPage import GameCardsPage


class SteamWebCrawler:

    valid_cookies = 'sessionid', 'steamMachineAuth', 'steamLoginSecure', 'timezoneOffset'
    web_pagess: dict = {}

    def __init__(self, steam_id: str, data: dict):
        self.__steam_id = steam_id
        self.__web_pages: dict[str, SteamWebPage] = {
            'open_booster_pack': OpenBoosterPack(),
            'get_badges': ProfileBadgesPage(),
            'get_inventory': InventoryPage(),
            'get_trading_cards': GameCardsPage(),
        }
        self.__cookies: dict = {}
        self.__set_cookies(data)
        # self.__web_session = None  # it should be implemented later

    def interact(self, interaction_type: str, logged_in: bool = False, **kwargs) -> (int, Any):

        web_page = self.__web_pages.get(interaction_type, None)

        # checking if data is good
        if web_page is None:
            return 404, 'not implemented'

        for user_data in kwargs.keys():
            if user_data not in web_page.required_user_data():
                return 400, f'missing user data: {user_data}'

        # getting needed cookies
        cookies = {}

        if logged_in:
            if 'steamLoginSecure' in self.__cookies:
                cookies['steamLoginSecure'] = self.__cookies['steamLoginSecure']
            else:
                return 403, f'missing cookie: steamLoginSecure'

        for required_cookie in web_page.required_cookies():
            if required_cookie == 'steamMachineAuth':
                required_cookie = 'steamMachineAuth' + self.__steam_id
            if required_cookie not in self.__cookies.keys():
                return 403, f'missing cookie: {required_cookie}'
            cookies[required_cookie] = self.__cookies[required_cookie]

        #
        try:
            result = web_page.interact(cookies, **kwargs)
            return 200, result
        except Exception as e:
            return 500, e

    def __set_cookies(self, cookies_to_add: dict):
        for name, cookie in cookies_to_add.items():
            if name == 'steamMachineAuth':
                self.__cookies[name + self.__steam_id] = cookie
                continue
            if name in SteamWebCrawler.valid_cookies:
                self.__cookies[name] = cookie
