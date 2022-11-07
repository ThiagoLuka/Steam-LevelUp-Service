from user_interfaces.MainUI import MainUI
from user_interfaces.GenericUI import GenericUI
from steam_users.SteamUserController import SteamUserController
from web_crawlers.ProfileBadgesPage import ProfileBadgesPage
from web_crawlers.InventoryPage import InventoryPage
from db.DBController import DBController


class MainController:

    def __init__(self):
        SteamUserController()
        DBController()

    @staticmethod
    def run_ui():

        while True:
            command = MainUI.run()

            if command == 1:
                SteamUserController().run_ui()
            if command == 2:
                user = SteamUserController().get_active_user()
                user.scrap(ProfileBadgesPage(), logged_in=True)
            if command == 3:
                # game_name = MainUI.get_game_name()  # it should be game_name instead of booster_pack_id
                booster_pack_id = GenericUI.get_string('Digite o item_id do booster pack: ')
                user = SteamUserController().get_active_user()
                if not user.inventory_downloaded():
                    user.scrap(InventoryPage())
                interaction = {
                    'type': 'open_booster_pack',
                    'game_name': '',
                    'booster_pack_item_id': booster_pack_id,
                }
                user.interact(InventoryPage(), interaction)

            if command == 0:
                MainUI.goodbye()
                break
