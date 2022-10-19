from web_scrapers.SteamWebPage import SteamWebPage
from data_models.SteamInventory import SteamInventory


class SteamUser:

    possible_cookies = ['sessionid', 'steamMachineAuth', 'steamLoginSecure']

    def __init__(self, user_data: dict):
        self.__steam_id: str = user_data['steam_id']
        self.__steam_alias: str = user_data['steam_alias']
        self.__cookies: dict = {}
        self.log_in(user_data)
        self.__inventory: SteamInventory = SteamInventory()

    @property
    def steam_id(self):
        return self.__steam_id

    @property
    def name(self):
        if self.__steam_alias is not None:
            return self.__steam_alias
        return self.__steam_id

    def log_in(self, login_data: dict):
        self.__add_cookies(login_data)

    def inventory_downloaded(self):
        if self.__inventory.empty():
            return False
        return True

    def scrap(self, web_page: SteamWebPage, logged_in: bool = False):

        req_user_data = web_page.required_user_data('scrap', logged_in)

        if web_page.requires_login() or logged_in:
            missing_user_data = self.__missing_user_data_for_request(req_user_data)
            if missing_user_data:
                return missing_user_data

        user_data = self.__user_data_for_request(req_user_data)

        result = web_page.scrap(user_data, self.__cookies)

        if isinstance(result, SteamInventory):
            self.__inventory = result

        return 200

    def interact(self, web_page: SteamWebPage, action: dict):

        possible_interactions = web_page.possible_interactions()
        if action['type'] not in possible_interactions:
            return possible_interactions

        req_user_data = web_page.required_user_data(action['type'], logged_in=True)

        missing_user_data = self.__missing_user_data_for_request(req_user_data)
        if missing_user_data:
            return missing_user_data

        user_data = self.__user_data_for_request(req_user_data)

        result = web_page.interact(action, user_data)

        return 200

    def __add_cookies(self, cookies: dict):
        for cookie in SteamUser.possible_cookies:
            if cookie in cookies.keys():
                self.__cookies[cookie] = cookies[cookie]

    def __missing_user_data_for_request(self, required_user_data: dict) -> list:
        for cookie in required_user_data['cookies']:
            if cookie not in self.__cookies.keys():
                return required_user_data['cookies']
        return []

    def __user_data_for_request(self, required_user_data: dict) -> dict:
        user_data: dict = {
            'cookies': {},
        }
        if 'steam_id' in required_user_data['standard']:
            user_data['steam_id'] = self.__steam_id
        if 'steam_alias' in required_user_data['standard']:
            user_data['steam_alias'] = self.__steam_alias
        if 'inventory' in required_user_data['standard']:
            user_data['inventory'] = self.__inventory
        for cookie in required_user_data['cookies']:
            if cookie == 'steamMachineAuth':
                user_data['cookies'][cookie + self.__steam_id] = self.__cookies[cookie]
            else:
                user_data['cookies'][cookie] = self.__cookies[cookie]

        return user_data
