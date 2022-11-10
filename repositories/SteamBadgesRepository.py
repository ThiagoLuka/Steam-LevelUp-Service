from repositories.QueryBuilderPG import QueryBuilderPG
from db.DBController import DBController


class SteamBadgesRepository:

    @staticmethod
    def get_all(badge_type: str) -> list[tuple]:
        query = f""" SELECT * FROM {badge_type}_badges;"""
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def get_all_by_user_id(user_id: int) -> list[tuple]:
        query = f"""
            SELECT * FROM user_badges
            WHERE user_id = '{user_id}';
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def get_all_by_game_name(game_name: str) -> list[tuple]:
        query = f"""
            SELECT * FROM game_badges
            INNER JOIN games ON games.id = game_badges.game_id
            WHERE games.name = '{game_name}';
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def upsert_multiple_game_badges(game_badges: zip) -> None:
        values = QueryBuilderPG.unzip_to_values_query_str(game_badges)
        query = f"""
            INSERT INTO game_badges (game_id, name, level, foil)
            VALUES {values}
            ON CONFLICT (game_id, level, foil) DO UPDATE
            SET name = EXCLUDED.name;
        """
        DBController.execute(query=query)

    @staticmethod
    def insert_multiple_badges(badge_type: str, cols_to_insert: list[str], pure_badges: zip) -> None:
        columns = QueryBuilderPG.cols_list_to_cols_str(cols_to_insert)
        values = QueryBuilderPG.unzip_to_values_query_str(pure_badges)
        query = f"""
            INSERT INTO {badge_type}_badges {columns}
            VALUES {values};
        """
        DBController.execute(query=query)