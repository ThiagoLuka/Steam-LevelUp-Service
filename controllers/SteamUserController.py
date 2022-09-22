from user_interfaces import SteamUserUI
from web_scrapers import SteamUser


class SteamUserController:

    def __init__(self):
        self.__users: list = []

    def run_ui(self):
        command = 10
        while command != 0:
            command = SteamUserUI.run()
            if command == 2:
                # create_user = SteamUserUI.create_user_options()
                # if create_user == 'manual':
                #     user_data = SteamUserUI.get_user_data()
                # elif create_user == 'database':
                #     user_data = SteamUserRepo.get_user_data(user_alias: str)
                user_data: dict = {
                    'steam_id': '76561198255516125',
                    'steam_alias': 'thiagomg'
                }
                new_user = SteamUser.from_dict(user_data)
                self.__users.append(new_user)
                SteamUserUI.user_created()

            continuar = SteamUserUI.continuar()
            if (not continuar) or (command == 0):
                return self.__users
