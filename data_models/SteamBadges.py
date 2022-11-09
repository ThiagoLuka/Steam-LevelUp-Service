import pandas as pd

from utils.PandasUtils import PandasUtils
from repositories.SteamGameBadgesRepository import SteamGameBadgesRepository
from repositories.SteamPureBadgesRepository import SteamPureBadgesRepository


class SteamBadges:

    __name = 'badges'
    __columns = ['id', 'name', 'level', 'experience', 'foil', 'game_id', 'pure_badge_page_id', 'unlocked_datetime']
    __game_badges_columns = ['id', 'game_id', 'name', 'level', 'foil']
    __pure_badges_columns = ['id', 'pure_badge_page_id', 'name']
    __user_badges_columns = ['id', 'user_id', 'game_badge_id', 'purge_badge_id', 'experience']

    def __init__(self, data = None):
        if isinstance(data, pd.DataFrame):
            self.df = data
        elif isinstance(data, list):
            if len(data) == len(self.__columns):
                self.df = pd.DataFrame(data=[data], columns=self.__columns)
            if len(data) == (len(self.__columns) - 1):
                c = self.__columns.copy()
                c.remove('id')
                self.df = pd.DataFrame(data=[data], columns=c)
                self.df = self.df.reindex(columns=self.__columns)
        else:
            self.df = pd.DataFrame(columns=self.__columns)

    def __add__(self, other):
        if isinstance(other, SteamBadges):
            self.df = pd.concat([self.df, other.df], ignore_index=True)
            self.df.drop_duplicates(inplace=True)
            return self

    @classmethod
    def all_game_badges_from_db(cls):
        df = pd.DataFrame(data=SteamGameBadgesRepository.get_all(), columns=cls.__game_badges_columns)
        df = df.reindex(columns=cls.__columns)
        return cls(df)

    @classmethod
    def all_pure_badges_from_db(cls):
        df = pd.DataFrame(data=SteamPureBadgesRepository.get_all(), columns=cls.__pure_badges_columns)
        df = df.reindex(columns=cls.__columns)
        return cls(df)

    def save(self) -> None:
        saved_game_badges = self.all_game_badges_from_db()
        game_badges = self.df[self.df['pure_badge_page_id'].isna()]
        new_game_badges = PandasUtils.df_set_difference(game_badges, saved_game_badges.df, ['game_id', 'level', 'foil'])
        if not new_game_badges.empty:
            game_ids = tuple(new_game_badges['game_id'])
            names = tuple(new_game_badges['name'])
            levels = tuple(new_game_badges['level'])
            foils = tuple(new_game_badges['foil'])
            SteamGameBadgesRepository.upsert_multiple_game_badges(zip(game_ids, names, levels, foils))

        saved_pure_badges = self.all_pure_badges_from_db()
        pure_badges = self.df[~self.df['pure_badge_page_id'].isna()]
        new_pure_badges = PandasUtils.df_set_difference(pure_badges, saved_pure_badges.df, ['name', 'pure_badge_page_id'])
        if not new_pure_badges.empty:
            page_ids = tuple(new_pure_badges['pure_badge_page_id'])
            names = tuple(new_pure_badges['name'])
            SteamPureBadgesRepository.insert_multiple_pure_badges(zip(page_ids, names))

        # save to user_badges
