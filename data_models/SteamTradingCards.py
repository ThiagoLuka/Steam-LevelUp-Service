import pandas as pd

from repositories.SteamTradingCardsRepository import SteamTradingCardsRepository
from data_models.PandasUtils import PandasUtils


class SteamTradingCards:

    __columns = ['id', 'game_id', 'set_number', 'name', 'url_name']

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
        if isinstance(other, SteamTradingCards):
            self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
            self.__df.drop_duplicates(inplace=True)
            return self

    @property
    def df(self) -> pd.DataFrame:
        return self.__df.copy()

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
        saved = SteamTradingCards.get_all()
        new_and_update = PandasUtils.df_set_difference(self.__df, saved.__df, ['game_id', 'set_number'])
        if not new_and_update.empty:
            cols_to_insert = self.__get_columns(with_id=False)
            zipped_data = PandasUtils.zip_df_columns(new_and_update, cols_to_insert)
            SteamTradingCardsRepository.insert_multiple_tcgs(zipped_data)

    @staticmethod
    def get_all() -> 'SteamTradingCards':
        data = SteamTradingCardsRepository.get_all()
        return SteamTradingCards.__from_db(data)
