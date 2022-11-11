from web_crawlers.SteamWebPage import SteamWebPage
from web_crawlers.InventoryPage import InventoryPage
from web_crawlers.ProfileBadgesPage import ProfileBadgesPage
from data_models.SteamInventory import SteamInventory
from repositories.SteamUserRepository import SteamUserRepository


class SteamUser:

    possible_cookies = ['sessionid', 'steamMachineAuth', 'steamLoginSecure', 'timezoneOffset']

    def __init__(self, user_data: dict):
        self.__steam_id: str = user_data['steam_id']
        self.__steam_alias: str = user_data['steam_alias']
        self.__user_id = self.__save_user()
        self.__cookies: dict = {}
        self.log_in(user_data)
        self.__inventory: SteamInventory = SteamInventory()

    @property
    def steam_id(self) -> str:
        return self.__steam_id

    @property
    def name(self) -> str:
        return (
            self.__steam_alias
            if self.__steam_alias is not None
            else self.__steam_id
        )

    def log_in(self, login_data: dict) -> None:
        self.__add_cookies(login_data)

    def get_badges(self):
        self.__scrap(ProfileBadgesPage(), logged_in=True)

    def download_inventory(self) -> None:
        self.__inventory = self.__scrap(InventoryPage(), logged_in=True)

    def inventory_downloaded(self) -> bool:
        return False if self.__inventory.empty() else True

    def open_booster_packs(self, booster_pack_class_id: str):
        # function should use game_name instead of booster_pack_class_id
        interaction = {
            'type': 'open_booster_pack',
            'game_name': '',
            'booster_pack_class_id': booster_pack_class_id,
        }
        self.__interact(InventoryPage(), interaction)

    def __scrap(self, web_page: SteamWebPage, logged_in: bool = False):
        req_user_data = web_page.required_user_data('scrap', logged_in)

        if web_page.requires_login() or logged_in:
            missing_user_data = self.__missing_user_data_for_request(req_user_data)
            if missing_user_data:
                return missing_user_data

        user_data = self.__user_data_for_request(req_user_data)

        result = web_page.scrap(user_data, self.__cookies)

        return result

    def __interact(self, web_page: SteamWebPage, action: dict):
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

    def __save_user(self) -> str:
        saved = SteamUserRepository.get_by_steam_id(self.__steam_id)
        if not saved:
            SteamUserRepository.save_user(self.__steam_id, self.__steam_alias)
        saved = SteamUserRepository.get_by_steam_id(self.__steam_id)
        user_id = saved[0][0]
        return user_id

    def __add_cookies(self, cookies: dict) -> None:
        for cookie in SteamUser.possible_cookies:
            if cookie in cookies.keys():
                self.__cookies[cookie] = cookies[cookie]

    def __missing_user_data_for_request(self, required_user_data: dict) -> list:
        missing_cookies = []
        for cookie in required_user_data['cookies']:
            if cookie not in self.__cookies.keys():
                missing_cookies.append(cookie)
        return missing_cookies

    def __user_data_for_request(self, required_user_data: dict) -> dict:
        user_data: dict = {
            'cookies': {},
        }
        if 'user_id' in required_user_data['standard']:
            user_data['user_id'] = self.__user_id
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
