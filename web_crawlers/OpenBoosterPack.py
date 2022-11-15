import requests

from user_interfaces.GenericUI import GenericUI
from web_crawlers.SteamWebPage import SteamWebPage
from data_models.SteamInventory import SteamInventory


class OpenBoosterPack(SteamWebPage):

    @staticmethod
    def required_user_data() -> tuple:
        return 'game_name', 'booster_pack_class_id', 'steam_alias', 'inventory'

    @staticmethod
    def required_cookies() -> tuple:
        return 'sessionid', 'steamLoginSecure'

    def interact(self, cookies: dict, **kwargs):
        game_name: str = kwargs['game_name']
        booster_pack_class_id: str = kwargs['booster_pack_class_id']
        steam_alias: str = kwargs['steam_alias']
        inventory: SteamInventory = kwargs['inventory']

        self.__open_booster_pack(game_name, booster_pack_class_id, steam_alias, inventory, cookies)

        return None

    def __open_booster_pack(
            self, game_name: str, booster_pack_class_id: str, steam_alias: str,
            inventory: SteamInventory, cookies: dict
    ):
        progress_text = 'Opening booster packs'
        GenericUI.progress_completed(progress=0, total=1, text=progress_text)

        # function below should return class_id of booster pack from that game. Should it be here?
        # booster_pack_id = db.get_booster_pack_id(game_name)  # booster_pack_id should come from db
        asset_id_list = inventory.get_all_asset_id(booster_pack_class_id)

        url = f"{super().BASESTEAMURL}id/{steam_alias}/ajaxunpackbooster/"
        for counter, asset_id in enumerate(asset_id_list):
            payload = {
                'communityitemid': asset_id,
                'sessionid': cookies['sessionid']
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            requests.post(url, data=payload, headers=headers, cookies=cookies)
            GenericUI.progress_completed(progress=counter + 1, total=len(asset_id_list), text=progress_text)
