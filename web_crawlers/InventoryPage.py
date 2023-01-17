import requests

from .SteamWebPage import SteamWebPage


class InventoryPage(SteamWebPage, name='inventory_page'):

    @staticmethod
    def required_user_data() -> tuple:
        return 'steam_id',

    @staticmethod
    def required_cookies() -> tuple:
        return 'steamMachineAuth', 'steamLoginSecure',

    def interact(self, cookies: dict, **kwargs) -> requests.Response:
        items_per_page: int = kwargs['items_per_page'] if 'items_per_page' in kwargs.keys() else 2000
        start_assetid: str = kwargs['start_assetid'] if 'start_assetid' in kwargs.keys() else None

        params = {
            'count': items_per_page,
            'start_assetid': start_assetid,
        }

        page_url = f'{super().BASESTEAMURL}inventory/{steam_id}/753/6/'
        response = requests.get(page_url, params=params, cookies=cookies)
        return response
