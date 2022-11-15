

class SteamWebPage:

    BASESTEAMURL = 'https://steamcommunity.com/'

    @staticmethod
    def required_user_data() -> tuple:
        pass

    @staticmethod
    def required_cookies() -> tuple:
        pass

    def interact(self, cookies: dict, **kwargs):
        pass
