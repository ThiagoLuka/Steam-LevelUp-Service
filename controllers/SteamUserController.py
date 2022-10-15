from singleton.Singleton import Singleton
from user_interfaces.SteamUserUI import SteamUserUI
from steam_users.SteamUser import SteamUser


class SteamUserController(metaclass=Singleton):

    def __init__(self):
        self.__users: dict = {}
        self.__load_standard_user()

    def get_user(self) -> SteamUser:
        user_options = self.view_all_users()
        index = SteamUserUI.choose_user(len(user_options))
        return self.__users[user_options[index]]

    def view_all_users(self) -> list:
        user_options: list = []
        if not self.__users:
            SteamUserUI.no_user()
        else:
            user_options = SteamUserUI.view_users(self.__users)
        return user_options

    def run_ui(self) -> None:
        while True:
            command = SteamUserUI.run()

            if command == 1:
                self.view_all_users()
            # if command == 2:
            #     new_user_data = SteamUserUI.create_new_user()
            #     new_user = SteamUser(new_user_data)
            #     self.__users[new_user.name] = new_user
            # if command == 3:
            #     user = self.get_user()
            #     cookies: dict = SteamUserUI.get_cookies_for_user()
            #     user.log_in(cookies)
            #     self.__users.update({user.name: user})
            # if command == 4:
            #     user = self.get_user()
            #     cookies: dict = SteamUserUI.get_headers_for_user()
            #     user.log_in(cookies)
            #     self.__users.update({user.name: user})

            if command == 0:
                return None

    def __load_standard_user(self) -> None:
        user_data: dict = {}

        with open('standard_user.txt', 'r') as file:
            for line in file.readlines():
                line_data = line.strip().split('=', 1)
                user_data[line_data[0]] = line_data[1]
        new_user = SteamUser(user_data)

        self.__users[new_user.name] = new_user
        SteamUserUI.user_loaded()
