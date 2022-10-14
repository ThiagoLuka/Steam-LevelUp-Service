import logging

from controllers.SteamUserController import SteamUserController
from user_interfaces.MainUI import MainUI
from web_scrapers.ProfileBadgesPage import ProfileBadgesPage


class MainController:

    def __init__(self):
        self.__users: list = []

    @staticmethod
    def run_ui():

        while True:
            command = MainUI.run()

            if command == 1:
                steam_users = SteamUserController().run_ui()
                if steam_users:
                    steam_users[0].scrap(ProfileBadgesPage())

            if command == 0:
                MainUI.goodbye()
