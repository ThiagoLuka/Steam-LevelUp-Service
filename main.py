from user_interfaces.MainUI import MainUI
from user_interfaces.GenericUI import GenericUI
from steam_users.SteamUserController import SteamUserController
from db.DBController import DBController


if __name__ == '__main__':

    SteamUserController()
    DBController()

    while True:
        command = MainUI.run()
        user = SteamUserController().get_active_user()

        if command == 1:
            SteamUserController().run_ui()
        if command == 2:
            user.get_badges()
        if command == 3:
            # open_booster_packs should use game_name instead of booster_pack_class_id
            # game_name = MainUI.get_game_name()
            booster_pack_class_id = GenericUI.get_string('Digite o class_id do booster pack: ')

            if not user.inventory_downloaded():
                user.download_inventory()
            user.open_booster_packs(booster_pack_class_id)

        if command == 0:
            MainUI.goodbye()
            break
