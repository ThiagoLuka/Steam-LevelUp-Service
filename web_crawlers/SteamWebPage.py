

class SteamWebPage:

    BASESTEAMURL = 'https://steamcommunity.com/'

    page_names: dict = {}

    def __init_subclass__(cls, **kwargs):
        SteamWebPage.page_names.update({kwargs['name']: cls})

    @staticmethod
    def required_user_data() -> tuple:
        pass

    @staticmethod
    def required_cookies() -> tuple:
        pass

    def interact(self, cookies: dict, **kwargs):
        pass
