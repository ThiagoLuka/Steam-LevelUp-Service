from data_models.SteamItem import SteamItem


class SteamInventory:
    """data format example:
    self.__data: dict = {
        '123456789': {  # item_id (class_id on steam)
            'details': SteamItem,
            'asset_id': list,
            'instance_id': list,
            'amount_marketable': int,
        },
    }"""

    def __init__(self, data: dict = None):
        self.__data = data
        if data is None:
            self.__data = {}

    @classmethod
    def from_inventory_page(cls, inventory_page_raw: dict):
        data: dict = {}
        # add items descriptions
        for descript in inventory_page_raw['descriptions']:
            data.setdefault(
                descript['classid'],
                {
                    'details': SteamItem(descript),
                    'asset_id': [],
                    'instance_id': [],
                    'amount_marketable': 0,
                }
            )

        # add assets count and detailed info
        for asset in inventory_page_raw['assets']:
            item_id = asset['classid']
            asset_id = asset['assetid']
            instance_id = asset['instanceid']

            data[item_id]['asset_id'].append(asset_id)
            data[item_id]['instance_id'].append(instance_id)
            if instance_id == '0':
                data[item_id]['amount_marketable'] += 1
        return cls(data)

    def empty(self) -> bool:
        if self.__data:
            return False
        return True

    def get_all_asset_id(self, item_id: str):
        return self.__data[item_id]['asset_id']
