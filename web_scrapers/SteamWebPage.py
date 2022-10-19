

class SteamWebPage:

    BASESTEAMURL = 'https://steamcommunity.com/'

    def requires_login(self) -> bool:
        pass

    def required_user_data(self, interaction_type: str, logged_in: bool) -> dict:
        pass

    def possible_interactions(self) -> list:
        pass

    def scrap(self, user_data: dict, cookies: dict) -> dict:
        pass

    def interact(self, action: dict, user_data: dict) -> dict:
        pass
