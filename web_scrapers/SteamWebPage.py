

class SteamWebPage:

    BASESTEAMURL = 'https://steamcommunity.com/'

    def requires_login(self) -> bool:
        pass

    def cookies_to_login(self) -> list:
        pass

    # def headers_to_login(self) -> list:
    #     pass

    def scrap(self, scrap_params: dict, cookies: dict):
        pass
