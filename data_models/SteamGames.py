import pandas as pd

from repositories.SteamGamesRepository import SteamGamesRepository
from data_models.PandasUtils import PandasUtils


class SteamGames:

    __columns = ['id', 'name', 'market_id']

    def __init__(self, **data):
        if not data:
            self.__df = pd.DataFrame(columns=self.__get_columns())
        else:
            if (
                    list(data.keys()) != self.__get_columns() and
                    list(data.keys()) != self.__get_columns(with_id=False)
            ):
                raise TypeError(f'Trying to set {self.__class__.__name__} with invalid data')
            self.__df = pd.DataFrame(data.values(), index=list(data.keys())).T

    def __add__(self, other):
        if isinstance(other, SteamGames):
            self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
            self.__df.drop_duplicates(inplace=True)
            return self

    def __iter__(self):
        for index, row in self.__df.iterrows():
            yield dict(row)

    @property
    def df(self) -> pd.DataFrame:
        return self.__df.copy()

    @property
    def empty(self) -> bool:
        return self.__df.empty

    @classmethod
    def __from_db(cls, data: list[tuple]):
        zipped_data = zip(*data)
        dict_data = dict(zip(cls.__columns, zipped_data))
        return cls(**dict_data)

    @classmethod
    def __get_columns(cls, with_id: bool = True) -> list:
        cols = cls.__columns.copy()
        if not with_id:
            cols.remove('id')
        return cols

    def save(self) -> None:
        saved = SteamGames.get_all()
        new_and_update = PandasUtils.df_set_difference(self.__df, saved.__df, 'name')
        if not new_and_update.empty:
            names = tuple(new_and_update['name'])
            market_ids = tuple(new_and_update['market_id'])
            SteamGamesRepository.upsert_multiple_games(zip(names, market_ids))

    @staticmethod
    def get_all() -> 'SteamGames':
        data = SteamGamesRepository.get_all()
        return SteamGames.__from_db(data)

    @staticmethod
    def get_all_without_trading_cards() -> 'SteamGames':
        data = SteamGamesRepository.get_all_without_trading_cards()
        return SteamGames.__from_db(data)

    @staticmethod
    def get_id_by_market_id(market_id: str) -> str:
        result = SteamGamesRepository.get_by_market_id(market_id)
        return result[0][0]

    def get_market_ids(self) -> list:
        if self.empty:
            all_games = SteamGames.get_all()
            return list(all_games.df['market_id'])
        return list(self.__df['market_id'])
