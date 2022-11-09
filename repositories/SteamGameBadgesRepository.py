from db.DBController import DBController


class SteamGameBadgesRepository:

    @staticmethod
    def get_all() -> list[tuple]:
        query = f""" SELECT * FROM game_badges"""
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def get_by_game_name(game_name: str) -> list[tuple]:
        query = f"""
            SELECT *
            FROM game_badges
            INNER JOIN games ON games.id = game_badges.game_id
            WHERE games.name = '{game_name}';
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def upsert_multiple_game_badges(game_badges: zip) -> None:
        values = ''
        for item in game_badges:
            game_id, name, level, foil = item
            if "'" in name:
                name = name.replace("'", "''")
            if values == '':
                values = f"('{game_id}', '{name}', '{level}', '{foil}')"
            else:
                values += f", ('{game_id}', '{name}', '{level}', '{foil}')"
        query = f"""
                INSERT INTO game_badges (game_id, name, level, foil)
                VALUES {values}
                ON CONFLICT (game_id, level, foil) DO UPDATE
                SET name = EXCLUDED.name;
            """
        DBController.execute(query=query)
