from controllers.SteamUserController import SteamUserController
from user_interfaces.MainUI import MainUI
from user_interfaces.GenericUI import GenericUI
from web_scrapers.ProfileBadgesPage import ProfileBadgesPage
from web_scrapers.InventoryPage import InventoryPage


class MainController:

    def __init__(self):
        SteamUserController()

    @staticmethod
    def run_ui():

        while True:
            command = MainUI.run()

            if command == 1:
                SteamUserController().run_ui()

            if command == 2:
                user = SteamUserController().get_user()
                user.scrap(ProfileBadgesPage(), logged_in=True)

            if command == 3:
                # game_name = MainUI.get_game_name()  # it should be game_name
                booster_pack_item_id = GenericUI.get_string('Digite o item_id do booster pack: ')
                user = SteamUserController().get_user()
                if not user.inventory_downloaded():
                    user.scrap(InventoryPage())
                interaction = {
                    'type': 'open_booster_pack',
                    'game_name': '',
                    'booster_pack_item_id': booster_pack_item_id,
                }
                user.interact(InventoryPage(), interaction)

            if command == 0:
                MainUI.goodbye()
                break
