from db.DBController import DBController


class SteamPureBadgesRepository:

    @staticmethod
    def get_all() -> list[tuple]:
        query = f""" SELECT * FROM pure_badges"""
        result = DBController.execute(query=query, get_result=True)
        return result

    @staticmethod
    def insert_multiple_pure_badges(pure_badges: zip) -> None:
        values = ''
        for item in pure_badges:
            page_id, name = item
            if "'" in name:
                name = name.replace("'", "''")
            if values == '':
                values = f"('{page_id}', '{name}')"
            else:
                values += f", ('{page_id}', '{name}')"
        query = f"""
                INSERT INTO pure_badges (page_id, name)
                VALUES {values};
            """
        DBController.execute(query=query)
