from data_models.SteamItem import SteamItem


class SteamInventory:

    def __init__(self, inventory_page_raw: dict):
        # example:
        # self.__data: dict = {
        #     '123456789': {  # item_id, equivalent to class_id on steam
        #         'details': SteamItem,
        #         'asset_id': list,
        #         'instance_id': list,
        #         'amount_marketable': int,
        #     },
        # }
        self.__data: dict = {}

        # add items descriptions
        for descript in inventory_page_raw['descriptions']:
            self.__data.setdefault(
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

            self.__data[item_id]['asset_id'].append(asset_id)
            self.__data[item_id]['instance_id'].append(instance_id)
            if instance_id == '0':
                self.__data[item_id]['amount_marketable'] += 1

    def get_all_assets_id(self, item_id: str):
        return self.__data[item_id]['asset_id']
