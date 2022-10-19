import requests

from web_scrapers.SteamWebPage import SteamWebPage
from controllers.SteamUserController import SteamUserController
from data_models.SteamInventory import SteamInventory


class InventoryPage(SteamWebPage):

    def requires_login(self) -> bool:
        return False

    def required_user_data(self, interaction_type: str, logged_in: bool = False) -> dict:
        interactions = {
            'scrap': {
                'standard': ['steam_id'],
                'cookies': [],
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

        full_inventory_page_raw = self.__download_full_inventory(user_data['steam_id'], cookies)
        inventory = SteamInventory.from_inventory_page(full_inventory_page_raw)
        # print(inventory.get_all_assets_id('2551450198'))
        return inventory

    def interact(self, action: dict, user_data: dict):
        if action['type'] == 'open_booster_pack':
            self.__open_booster_pack(
                action['game_name'],
                action['booster_pack_item_id'],
                user_data['steam_alias'],
                user_data['inventory'],
                user_data['cookies'],
            )

    def __download_full_inventory(self, steam_id: str, cookies: dict) -> dict:
        print("Please wait a few seconds, downloading today's inventory... ")

        count = 2000
        first_page_url = f'{super().BASESTEAMURL}inventory/{steam_id}/753/6?count={count}'
        inventory_first_page = requests.get(first_page_url, cookies=cookies).json()

        inventory_pages_raw = inventory_first_page

        page_counter = 0
        while 'more_items' in inventory_first_page.keys():
            next_page_url = first_page_url + '&start_assetid=' + inventory_first_page['last_assetid']
            inventory_first_page = requests.get(next_page_url, cookies=cookies).json()

            inventory_pages_raw['assets'].extend(inventory_first_page['assets'])
            inventory_pages_raw['descriptions'].extend(inventory_first_page['descriptions'])
            # future logging
            page_counter += 1
            print(f"\r{page_counter*count/inventory_pages_raw['total_inventory_count']*100:.2f}%", end='', flush=True)
        print('\r100.00%', flush=True)
        print(inventory_pages_raw['total_inventory_count'], len(inventory_pages_raw['assets']))

        return inventory_pages_raw

    def __open_booster_pack(self, game_name: str, booster_pack_item_id: str, steam_alias: str,
                            inventory: SteamInventory, cookies: dict):

        # returns item_id of booster pack from that game
        # booster_pack_id = db.get_booster_pack_id(game_name)  # should come from db
        asset_id_list = inventory.get_all_asset_id(booster_pack_item_id)

        url = f"{super().BASESTEAMURL}id/{steam_alias}/ajaxunpackbooster/"
        for counter, asset_id in enumerate(asset_id_list):
            payload = {
                'communityitemid': asset_id,
                'sessionid': cookies['sessionid']
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            requests.post(url, data=payload, headers=headers, cookies=cookies)
            print(f"\r{(counter + 1) / len(asset_id_list) * 100:.2f}%", end='', flush=True)
        print('\r100.00%', flush=True)
