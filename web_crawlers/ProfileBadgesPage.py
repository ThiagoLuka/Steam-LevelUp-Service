import requests

from lxml import html, etree

from web_crawlers.SteamWebPage import SteamWebPage
from user_interfaces.GenericUI import GenericUI
from data_models.SteamGames import SteamGames


class ProfileBadgesPage(SteamWebPage):

    def requires_login(self) -> bool:
        return False

    def required_user_data(self, interaction_type: str, logged_in: bool = False) -> dict:
        req_user_data = {
            'standard': ['steam_id'],
            'cookies': [],
        }
        if logged_in or self.requires_login():
            req_user_data['cookies'].append('steamLoginSecure')
        return req_user_data

    def possible_interactions(self) -> list:
        return []

    def scrap(self, user_data: dict, cookies: dict):
        # Extract
        badges_raw = self.__get_all_badges_raw(user_data['steam_id'], cookies)

        # Transform/Load
        games = self.__get_games_from_badges_raw(badges_raw)
        games.save()

        # badges = self.__get_badges_from_badges_raw(badges_raw)
        # badges.save()
        # badges.save_with_user(user_data['steam_id'])

    def __get_all_badges_raw(self, steam_id: str, cookies: dict) -> list:
        progress_text = 'Extracting data from badges pages'
        GenericUI.progress_completed(progress=0, total=1, text=progress_text)
        url = f"{super().BASESTEAMURL}profiles/{steam_id}/badges/?sort=a"
        response = requests.get(url, cookies=cookies)
        first_page_tree = html.fromstring(response.content)

        all_badges_raw = first_page_tree.find_class('badge_row')

        if first_page_tree.find_class('profile_paging'):
            next_pages_urls = self.__get_next_pages_links(first_page_tree, url)
            GenericUI.progress_completed(progress=1, total=len(next_pages_urls) + 1, text=progress_text)

            for counter, url in enumerate(next_pages_urls):
                response = requests.get(url, cookies=cookies)
                page_tree = html.fromstring(response.content)
                all_badges_raw.extend(page_tree.find_class('badge_row'))
                GenericUI.progress_completed(progress=counter + 2, total=len(next_pages_urls) + 1, text=progress_text)
        else:
            GenericUI.progress_completed(progress=1, total=1, text=progress_text)

        return all_badges_raw

    @staticmethod
    def __get_next_pages_links(first_page_tree: etree.Element, first_page_url: str) -> list:
        next_pages_links = []
        links = first_page_tree.find_class('pagelink')
        for elem_with_link in links:
            elem_with_link.make_links_absolute(first_page_url)
            link = elem_with_link.get('href')
            if link not in next_pages_links:
                next_pages_links.append(link)
        return next_pages_links

    @staticmethod
    def __get_games_from_badges_raw(badges_raw: list) -> SteamGames:
        progress_text = 'Cleaning and saving data: games'
        GenericUI.progress_completed(progress=0, total=len(badges_raw), text=progress_text)

        games = SteamGames()
        for index, badge_raw in enumerate(badges_raw):

            badge_details_link = badge_raw.find_class('badge_row_overlay')[0].get('href')
            if '/badges/' in badge_details_link:  # games have '/gamecards/' instead
                GenericUI.progress_completed(progress=index + 1, total=len(badges_raw), text=progress_text)
                continue
            market_id = badge_details_link.split('/')[-2]

            game_name_raw = badge_raw.find_class('badge_title')[0].text
            if 'Foil' in game_name_raw:
                game_name_raw = game_name_raw.replace('- Foil Badge', '')
            game_name = game_name_raw.replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '')

            games += SteamGames([game_name, market_id])
            GenericUI.progress_completed(progress=index + 1, total=len(badges_raw), text=progress_text)

        return games
