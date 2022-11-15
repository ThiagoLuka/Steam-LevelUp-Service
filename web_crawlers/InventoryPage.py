import requests

from user_interfaces.GenericUI import GenericUI
from web_crawlers.SteamWebPage import SteamWebPage
from data_models.SteamInventory import SteamInventory


class InventoryPage(SteamWebPage):

    @staticmethod
    def required_user_data() -> tuple:
        return 'steam_id',

    @staticmethod
    def required_cookies() -> tuple:
        return 'steamMachineAuth', 'steamLoginSecure'

    def interact(self, cookies: dict, **kwargs):
        steam_id: str = kwargs['steam_id']

        # Extract
        full_inventory_raw = self.__download_full_inventory(steam_id, cookies)

        # Transform
        inventory = SteamInventory.from_inventory_page(full_inventory_raw)

        return inventory

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
