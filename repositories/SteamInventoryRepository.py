from repositories.QueryBuilderPG import QueryBuilderPG
from db.DBController import DBController


class SteamInventoryRepository:

    @staticmethod
    def get_current_by_user_id(user_id: int, columns: list) -> list[tuple]:
        query = f"""
            SELECT {', '.join(columns)}
            FROM item_steam_assets
            WHERE
                user_id = '{user_id}'
                AND removed_at IS NULL;
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def get_current_size_by_user_id(user_id: int) -> int:
        query = f"""
            SELECT COUNT(id) FROM item_steam_assets
            WHERE
                user_id = '{user_id}'
                AND removed_at IS NULL;
        """
        result = DBController.execute(query=query, get_result=True)
        return result[0][0]

    @staticmethod
    def get_booster_pack_assets_id(user_id: int, game_name: str) -> list[tuple]:
        game_name = QueryBuilderPG.sanitize_string(game_name)
        query = f"""
            SELECT asset_id 
            FROM item_steam_assets isa 
            INNER JOIN items_steam is2 ON is2.id = isa.item_steam_id
            INNER JOIN item_steam_types ist ON ist.id = is2.item_steam_type_id
            INNER JOIN games g ON g.id = is2.game_id
            WHERE
                user_id = '{user_id}'
                AND g."name" = '{game_name}'
                AND ist."name" = 'Booster Pack'
                AND removed_at IS NULL;
        """
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def upsert_new_assets(assets: zip, columns: list[str]) -> None:
        values = QueryBuilderPG.unzip_to_query_values_str(assets)
        query = f"""
            INSERT INTO item_steam_assets ({', '.join(columns)})
            VALUES {values}
            ON CONFLICT (user_id, asset_id) DO NOTHING;
        """
        DBController.execute(query=query)

    @staticmethod
    def update_removed_assets(assets: zip) -> None:
        values = QueryBuilderPG.unzip_to_query_values_str(assets)
        query = f"""
            UPDATE item_steam_assets
            SET
                removed_at = update.removed_at::timestamp
            FROM (
                VALUES {values}
            ) AS update(id, removed_at)
            WHERE
                item_steam_assets.id = update.id::int;
        """
        DBController.execute(query=query)
