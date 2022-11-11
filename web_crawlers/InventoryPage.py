import requests

from user_interfaces.GenericUI import GenericUI
from web_crawlers.SteamWebPage import SteamWebPage
from data_models.SteamInventory import SteamInventory


class InventoryPage(SteamWebPage):

    def requires_login(self) -> bool:
        return True

    def required_user_data(self, interaction_type: str, logged_in: bool = False) -> dict:
        interactions = {
            'scrap': {
                'standard': ['steam_id'],
                'cookies': ['steamMachineAuth', 'steamLoginSecure'],
            },
            'open_booster_pack': {
                'standard': ['steam_alias', 'inventory'],
                'cookies': ['sessionid', 'steamLoginSecure'],
            },
        }
        required_user_data = interactions.get(interaction_type)
        if (logged_in or self.requires_login()) and ('steamLoginSecure' not in required_user_data['cookies']):
            required_user_data['cookies'].append('steamLoginSecure')
        return required_user_data

    def possible_interactions(self) -> list:
        return ['open_booster_pack']

    def scrap(self, user_data: dict, cookies: dict):
        # Extract
        full_inventory_raw = self.__download_full_inventory(user_data['steam_id'], cookies)

        # Transform
        inventory = SteamInventory.from_inventory_page(full_inventory_raw)

        return inventory

    def interact(self, action: dict, user_data: dict):
        if action['type'] == 'open_booster_pack':
            self.__open_booster_pack(
                action['game_name'],
                action['booster_pack_class_id'],
                user_data['steam_alias'],
                user_data['inventory'],
                user_data['cookies'],
            )

    def __download_full_inventory(self, steam_id: str, cookies: dict) -> dict:
        progress_text = 'Downloading inventory'
        GenericUI.progress_completed(progress=0, total=1, text=progress_text)

        progress_counter = 0
        items_per_page = 2000

        first_page_url = f'{super().BASESTEAMURL}inventory/{steam_id}/753/6?count={items_per_page}'
        inventory_page = requests.get(first_page_url, cookies=cookies).json()

        inventory_size = inventory_page['total_inventory_count']

        progress_counter += 1
        progress = progress_counter * items_per_page
        GenericUI.progress_completed(progress=progress, total=inventory_size, text=progress_text)

        full_inventory_pages_raw = inventory_page
        while 'more_items' in inventory_page.keys():
            next_page_url = f"{first_page_url}&start_assetid={inventory_page['last_assetid']}"
            inventory_page = requests.get(next_page_url, cookies=cookies).json()

            full_inventory_pages_raw['assets'].extend(inventory_page['assets'])
            full_inventory_pages_raw['descriptions'].extend(inventory_page['descriptions'])

            progress_counter += 1
            progress = progress_counter * items_per_page
            GenericUI.progress_completed(progress=progress, total=inventory_size, text=progress_text)
        GenericUI.progress_completed(progress=1, total=1, text=progress_text)

        return full_inventory_pages_raw

    def __open_booster_pack(self, game_name: str, booster_pack_class_id: str, steam_alias: str,
                            inventory: SteamInventory, cookies: dict):
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
