

class SteamItem:

    def __init__(self, descript: dict):
        # will change when db is implemented
        # search for equivalent info in db. If not found, add new in db using smthg like this
        self.__item_id = descript['classid']
        self.__name = descript['name']
        if descript['type'] == 'Booster Pack':
            self.__game = descript['name'].replace(' Booster Pack', '')
        else:
            self.__game = descript['type'].replace(' Trading Card', '')
        self.__game_market_hash = descript['market_fee_app']

    def market_hash_name(self):
        return f'{str(self.__game_market_hash)}-{self.__name}'
