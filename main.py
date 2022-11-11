from user_interfaces.MainUI import MainUI
from user_interfaces.GenericUI import GenericUI
from steam_users.SteamUserController import SteamUserController
from web_crawlers.ProfileBadgesPage import ProfileBadgesPage
from web_crawlers.InventoryPage import InventoryPage
from db.DBController import DBController


if __name__ == '__main__':

    SteamUserController()
    DBController()

    while True:
        command = MainUI.run()

        if command == 1:
            SteamUserController().run_ui()
        if command == 2:
            user = SteamUserController().get_active_user()
            user.scrap(ProfileBadgesPage(), logged_in=True)
        if command == 3:
            # command should use game_name instead of booster_pack_class_id
            # game_name = MainUI.get_game_name()
            booster_pack_id = GenericUI.get_string('Digite o class_id do booster pack: ')
            user = SteamUserController().get_active_user()
            if not user.inventory_downloaded():
                user.scrap(InventoryPage())
            interaction = {
                'type': 'open_booster_pack',
                'game_name': '',
                'booster_pack_class_id': booster_pack_id,
            }
            user.interact(InventoryPage(), interaction)

        if command == 0:
            MainUI.goodbye()
            break
