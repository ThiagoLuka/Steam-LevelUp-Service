from web_scrapers.SteamWebPage import SteamWebPage


class SteamUser:

    def __init__(self, steam_id: str, steam_alias: str = ''):
        self.__steam_id: str = steam_id
        self.__steam_alias: str = steam_alias
        self.__login_cookies: dict = {}
        # self.__login_headers: dict = {}

    @classmethod
    def from_dict(cls, user_data: dict):
        return cls(user_data['steam_id'], user_data['steam_alias'])

    @property
    def steam_id(self):
        return self.__steam_id

    @property
    def steam_alias(self):
        return self.__steam_alias

    def log_in(self, cookies = None, headers = None):
        if cookies is None:
            cookies: dict = {}
        # if headers is None:
        #     headers: dict = {}
        self.__login_cookies = cookies

    def scrap(self, web_page: SteamWebPage, logged_in: bool = False):
        scrap_params = {'steam_id': self.__steam_id}

        if web_page.requires_login() or logged_in:
            for cookie in web_page.cookies_to_login():
                if cookie not in self.__login_cookies.keys():
                    return {
                        'status_code': 500,
                        'cookies_needed': web_page.cookies_to_login()
                    }

        web_page.scrap(scrap_params, self.__login_cookies)

        return {'status_code': 200}
