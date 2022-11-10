import pandas as pd

from utils.PandasUtils import PandasUtils
from repositories.SteamBadgesRepository import SteamBadgesRepository


class SteamBadges:

    __name = 'badges'
    __columns = ['id', 'name', 'level', 'experience', 'foil', 'game_id', 'pure_badge_page_id', 'unlocked_at']
    __game_badges_columns = ['id', 'game_id', 'name', 'level', 'foil']
    __pure_badges_columns = ['id', 'pure_badge_page_id', 'name']
    __user_badges_columns = ['id', 'user_id', 'game_badge_id', 'pure_badge_id', 'experience', 'unlocked_at']

    def __init__(self, data = None):
        if isinstance(data, pd.DataFrame):
            self.__df = data
        elif isinstance(data, list):
            if len(data) == len(self.__get_columns()):
                self.__df = pd.DataFrame(data=[data], columns=self.__get_columns())
            if len(data) == (len(self.__get_columns()) - 1):
                self.__df = pd.DataFrame(data=[data], columns=self.__get_columns(with_id=False))
                self.__df = self.__df.reindex(columns=self.__get_columns())
        else:
            self.__df = pd.DataFrame(columns=self.__columns)

    def __add__(self, other):
        if isinstance(other, SteamBadges):
            self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
            self.__df.drop_duplicates(inplace=True)
            return self

    @property
    def df(self) -> pd.DataFrame:
        return self.__df.copy()

    @classmethod
    def all_from_db(cls, badge_type: str, user_id = 0):
        if badge_type == 'user':
            data = SteamBadgesRepository.get_all_by_user_id(user_id)
        else:
            data = SteamBadgesRepository.get_all(badge_type)
        df = pd.DataFrame(data=data, columns=cls.__get_columns(badge_type))
        return cls(df)

    def save(self, user_id: int) -> None:
        game_badges = self.__df[self.__df['pure_badge_page_id'].isna()]
        self.__save_by_type(
            'game', game_badges, columns_to_check_difference=['game_id', 'level', 'foil']
        )

        pure_badges = self.__df[~self.__df['pure_badge_page_id'].isna()]
        self.__save_by_type(
            'pure', pure_badges, columns_to_check_difference=['pure_badge_page_id', 'name']
        )

        user_badges = self.__user_badges_table_with_ids(user_id)
        self.__save_by_type(
            'user', user_badges, columns_to_check_difference=['user_id', 'game_badge_id', 'pure_badge_id']
        )

    @classmethod
    def __get_columns(cls, badge_type: str = '', with_id: bool = True):
        cols = {
            '': cls.__columns.copy(),
            'game': cls.__game_badges_columns.copy(),
            'pure': cls.__pure_badges_columns.copy(),
            'user': cls.__user_badges_columns.copy(),
        }.get(badge_type, [])
        if not with_id:
            cols.remove('id')
        return cols

    def __save_by_type(self, badge_type: str, badges: pd.DataFrame, columns_to_check_difference: list[str]) -> None:
        saved = SteamBadges.all_from_db(badge_type).__df
        new = PandasUtils.df_set_difference(badges, saved, columns_to_check_difference)
        if not new.empty:
            cols_to_insert = self.__get_columns(badge_type, with_id=False)
            zipped_data = PandasUtils.zip_df_columns(new, cols_to_insert)
            if badge_type == 'game':
                SteamBadgesRepository.upsert_multiple_game_badges(zipped_data)
            if badge_type == 'pure':
                cols_to_insert.remove('pure_badge_page_id')
                cols_to_insert.insert(0, 'page_id')
                SteamBadgesRepository.insert_multiple_badges(badge_type, cols_to_insert, zipped_data)
            if badge_type == 'user':
                SteamBadgesRepository.insert_multiple_badges(badge_type, cols_to_insert, zipped_data)

    def __user_badges_table_with_ids(self, user_id: int) -> pd.DataFrame:
        saved_game_badges = self.all_from_db('game').__df
        saved_game_badges.rename(columns={'id': 'game_badge_id'}, inplace=True)
        user_game_badges = pd.merge(self.__df, saved_game_badges)

        saved_pure_badges = self.all_from_db('pure').__df
        saved_pure_badges.rename(columns={'id': 'pure_badge_id'}, inplace=True)
        user_pure_badges = pd.merge(self.__df, saved_pure_badges)

        user_badges = pd.concat([user_game_badges, user_pure_badges], ignore_index=True)
        user_badges['user_id'] = user_id
        user_badges = user_badges[self.__get_columns('user')]
        user_badges = PandasUtils.format_only_positive_int_with_nulls(user_badges, ['game_badge_id', 'pure_badge_id'])
        return user_badges
