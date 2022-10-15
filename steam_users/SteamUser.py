from web_scrapers.SteamWebPage import SteamWebPage


class SteamUser:

    # used to log_in and access more features from web pages
    possible_cookies = ['sessionid', 'steamMachineAuth', 'steamLoginSecure']
    possible_headers = ['Content-Type', 'Referer']

    def __init__(self, user_data: dict):
        self.__steam_id: str = user_data['steam_id']
        self.__steam_alias: str = user_data['steam_alias']
        self.__login_cookies: dict = {}
        self.__login_headers: dict = {}
        self.log_in(user_data)

    @property
    def steam_id(self):
        return self.__steam_id

    @property
    def name(self):
        if self.__steam_alias is not None:
            return self.__steam_alias
        return self.__steam_id

    def log_in(self, login_data: dict):
        self.__add_cookies(login_data)
        self.__add_headers(login_data)

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

        # esses returns com status code simulando http, precisa?
        return {'status_code': 200}

    def __add_cookies(self, cookies: dict):
        for cookie in SteamUser.possible_cookies:
            if cookie in cookies.keys():
                if cookie == 'steamMachineAuth':
                    self.__login_cookies[cookie + self.__steam_id] = cookies[cookie]
                else:
                    self.__login_cookies[cookie] = cookies[cookie]

    def __add_headers(self, headers):
        for header in SteamUser.possible_headers:
            if header in headers.keys():
                self.__login_headers[header] = headers[header]