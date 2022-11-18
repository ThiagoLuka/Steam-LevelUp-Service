from web_crawlers.SteamWebCrawler import SteamWebCrawler
from data_models.SteamInventory import SteamInventory
from repositories.SteamUserRepository import SteamUserRepository


class SteamUser:

    possible_cookies = ['sessionid', 'steamMachineAuth', 'steamLoginSecure', 'timezoneOffset']

    def __init__(self, user_data: dict):
        self.__steam_id: str = user_data['steam_id']
        self.__steam_alias: str = user_data['steam_alias']
        self.__user_id = self.__save_user()
        self.__crawler = SteamWebCrawler(self.__steam_id, user_data)
        self.__inventory = SteamInventory()

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
        pass

    def get_badges(self, logged_in: bool = True):
        status, result = self.__crawler.interact(
            'get_badges',
            logged_in=logged_in,
            user_id=self.__user_id,
            steam_id=self.steam_id,
        )
        if status != 200:
            print(result)
            return

    def download_inventory(self) -> None:
        status, result = self.__crawler.interact(
            'get_inventory',
            steam_id=self.steam_id,
        )
        if status != 200:
            print(result)
            return
        self.__inventory = result

    def inventory_downloaded(self) -> bool:
        return not self.__inventory.empty()

    def open_booster_packs(self, booster_pack_class_id: str):
        # function should use game_name instead of booster_pack_class_id
        status, result = self.__crawler.interact(
            'open_booster_pack',
            game_name='',
            booster_pack_class_id=booster_pack_class_id,
            steam_alias=self.__steam_alias,
            inventory=self.__inventory,
        )
        if status != 200:
            print(result)
            return

    def __save_user(self) -> str:
        saved = SteamUserRepository.get_by_steam_id(self.__steam_id)
        if not saved:
            SteamUserRepository.save_user(self.__steam_id, self.__steam_alias)
        saved = SteamUserRepository.get_by_steam_id(self.__steam_id)
        user_id = saved[0][0]
        return user_id
