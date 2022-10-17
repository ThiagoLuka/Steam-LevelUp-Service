import requests

from web_scrapers.SteamWebPage import SteamWebPage
from controllers.SteamUserController import SteamUserController
from data_models.SteamInventory import SteamInventory


class InventoryPage(SteamWebPage):

    def requires_login(self) -> bool:
        return False

    def cookies_to_login(self) -> list:
        return ['steamLoginSecure']

    def headers_to_login(self) -> list:
        return []

    def scrap(self, scrap_params: dict, cookies: dict):

        full_inventory_page_raw = self.__download_full_inventory(scrap_params['steam_id'], cookies)
        inventory = SteamInventory(full_inventory_page_raw)
        # print(inventory.get_all_assets_id('2551450198'))
        return inventory

    def __download_full_inventory(self, steam_id: str, cookies: dict) -> dict:
        print("Please wait a few seconds, downloading today's inventory... ")

        count = 2000
        first_page_url = f'{super().BASESTEAMURL}inventory/{steam_id}/753/6?count={count}'
        inventory_first_page = requests.get(first_page_url).json()

        inventory_pages_raw = inventory_first_page

        page_counter = 0
        while 'more_items' in inventory_first_page.keys():
            next_page_url = first_page_url + '&start_assetid=' + inventory_first_page['last_assetid']
            inventory_first_page = requests.get(next_page_url).json()

            inventory_pages_raw['assets'].extend(inventory_first_page['assets'])
            inventory_pages_raw['descriptions'].extend(inventory_first_page['descriptions'])
            # future logging
            page_counter += 1
            print(f"\r{page_counter*count/inventory_pages_raw['total_inventory_count']*100:.2f}%", end='', flush=True)
        print('\r100.00%', flush=True)
        print(inventory_pages_raw['total_inventory_count'], len(inventory_pages_raw['assets']))
        if inventory_pages_raw['total_inventory_count'] == len(inventory_pages_raw['assets']):
            print('Inventory downloaded correctly and ready to use!')
        else:
            print('Some items were not downloaded correctly...\nTry redownloading it')

        return inventory_pages_raw


if __name__ == '__main__':
    SteamUserController()
    user = SteamUserController().get_user()
    inventory1 = InventoryPage()
    user.scrap(inventory1)
