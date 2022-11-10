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
            if len(data) == len(self.__columns):
                self.__df = pd.DataFrame(data=[data], columns=self.__columns)
            if len(data) == (len(self.__columns) - 1):
                c = self.__columns.copy()
                c.remove('id')
                self.__df = pd.DataFrame(data=[data], columns=c)
                self.__df = self.__df.reindex(columns=self.__columns)
        else:
            self.__df = pd.DataFrame(columns=self.__columns)

    def __add__(self, other):
        if isinstance(other, SteamGames):
            self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
            self.__df.drop_duplicates(inplace=True)
            return self

    @property
    def df(self) -> pd.DataFrame:
        return self.__df.copy()

    @classmethod
    def all_from_db(cls):
        df = pd.DataFrame(data=SteamGamesRepository.get_all(), columns=cls.__columns)
        return cls(df)

    @staticmethod
    def get_id_by_market_id(market_id: str) -> str:
        result = SteamGamesRepository.get_by_market_id(market_id)
        return result[0][0]

    def save(self) -> None:
        saved = self.all_from_db()
        new_and_update = PandasUtils.df_set_difference(self.__df, saved.__df, 'name')
        if not new_and_update.empty:
            names = tuple(new_and_update['name'])
            market_ids = tuple(new_and_update['market_id'])
            SteamGamesRepository.upsert_multiple_games(zip(names, market_ids))
