import pandas as pd

from repositories.SteamGamesRepository import SteamGamesRepository
from utils.PandasUtils import PandasUtils


class SteamGames:

    __name = 'games'
    __columns = ['id', 'name', 'market_id']

    def __init__(self, data = None):
        if isinstance(data, pd.DataFrame):
            self.__df = data
        elif isinstance(data, list):
            if len(data) == 3:
                self.__df = pd.DataFrame(data=[data], columns=self.__columns)
            if len(data) == 2:
                c = self.__columns.copy()
                c.remove('id')
                self.__df = pd.DataFrame(data=[data], columns=c)
                self.__df['id'] = None
                self.__df = self.__df[self.__columns]
        else:
            self.__df = pd.DataFrame(columns=self.__columns)

    def __add__(self, other):
        if isinstance(other, SteamGames):
            self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
            self.__df.drop_duplicates(inplace=True)
            return self

    @classmethod
    def all_from_db(cls):
        df = pd.DataFrame(data=SteamGamesRepository.get_all(), columns=cls.__columns)
        return cls(df)

    def save(self):
        saved = self.all_from_db()
        new_and_update = PandasUtils.df_set_difference(self.__df, saved.__df, 'name')
        if not new_and_update.empty:
            names = tuple(new_and_update['name'])
            market_ids = tuple(new_and_update['market_id'])
            SteamGamesRepository.upsert_multiple_games(zip(names, market_ids))
