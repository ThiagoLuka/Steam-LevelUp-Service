from db.DBController import DBController


class SteamUserRepository:

    @staticmethod
    def save_user(steam_id: str, steam_alias: str = ''):
        query = f"""
            INSERT INTO users (steam_id, steam_alias)
            VALUES ('{steam_id}', '{steam_alias}')
            ON CONFLICT (steam_id) DO UPDATE
            SET steam_alias = EXCLUDED.steam_alias;
        """
        DBController.execute(query=query)

    @staticmethod
    def get_by_steam_id(steam_id: str):
        query = f"""
            SELECT *
            FROM users
            WHERE steam_id = '{steam_id}';
        """
        result = DBController.execute(query=query, get_result=True)
        return result
