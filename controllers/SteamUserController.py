from user_interfaces.SteamUserUI import SteamUserUI
from steam_users.SteamUser import SteamUser


class SteamUserController:

    def __init__(self):
        self.__users: list = []

    def run_ui(self):

        while True:
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
            if (command == 0) or (not continuar):
                return self.__users
