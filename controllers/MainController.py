from controllers.SteamUserController import SteamUserController
from user_interfaces.MainUI import MainUI
from web_scrapers.ProfileBadgesPage import ProfileBadgesPage


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

            if command == 0:
                MainUI.goodbye()
                break
