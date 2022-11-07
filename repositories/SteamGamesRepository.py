from db.DBController import DBController


class SteamGamesRepository:

    @staticmethod
    def get_all():
        query = f""" SELECT * FROM games"""
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def get_by_name(name: str):
        query = f"""
            SELECT *
            FROM games
            WHERE name = '{name}';
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def upsert_single_game(name: str, market_id: str) -> None:
        if "'" in name:
            name = name.replace("'", "''")
        query = f"""
            INSERT INTO games (name, market_id)
            VALUES ('{name}', '{market_id}')
            ON CONFLICT (market_id) DO UPDATE
            SET name = EXCLUDED.name;
        """
        DBController.execute(query=query)

    @staticmethod
    def upsert_multiple_games(games: zip) -> None:
        values = ''
        for item in games:
            name, market_id = item
            if "'" in name:
                name = name.replace("'", "''")
            if values == '':
                values = f"('{name}', '{market_id}')"
            else:
                values += f", ('{name}', '{market_id}')"
        query = f"""
                INSERT INTO games (name, market_id)
                VALUES {values}
                ON CONFLICT (market_id) DO UPDATE
                SET name = EXCLUDED.name;
            """
        DBController.execute(query=query)
