import requests

from lxml import html, etree

from web_scrapers.SteamWebPage import SteamWebPage
from user_interfaces.GenericUI import GenericUI


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
        print('Scraping badges pages...')
        GenericUI.progress_completed(progress=0, total=1)
        main_url = f"{super().BASESTEAMURL}profiles/{user_data['steam_id']}/badges/?sort=a"
        response = requests.get(main_url, cookies=cookies)
        main_page_tree = html.fromstring(response.content)

        self.__scrap_single_page(main_page_tree)
        next_pages_urls = self.__get_next_pages_links(main_page_tree, main_url)
        GenericUI.progress_completed(progress=1, total=len(next_pages_urls) + 1)

        for counter, url in enumerate(next_pages_urls):
            response = requests.get(url, cookies=cookies)
            page_tree = html.fromstring(response.content)
            self.__scrap_single_page(page_tree)
            GenericUI.progress_completed(progress=counter + 2, total=len(next_pages_urls) + 1)

    # change to a page generator later
    @staticmethod
    def __scrap_single_page(page_tree: etree.Element):
        for elem in page_tree.find_class('badge_row'):
            badge_details_link = elem.find_class('badge_row_overlay')[0].get('href')
            if 'gamecards' in badge_details_link:
                game_title = elem.find_class('badge_title')[0].text.strip()
                if 'Foil Badge' in game_title:
                    game_title = game_title.replace('- Foil Badge', '').strip()
                game_market_hash = elem.find_class('badge_row_overlay')[0].get('href').split('/')[-2]
                # save/update database
                # print(f'{game_market_hash} {game_title}')

    @staticmethod
    def __get_next_pages_links(main_page_tree: etree.Element, main_url: str) -> list:
        next_pages_links = []
        links_menu = main_page_tree.find_class('pageLinks')
        if links_menu:
            page_links_elems = links_menu[0].find_class('pagelink')
            for elem in page_links_elems:
                elem.make_links_absolute(main_url)
                next_pages_links.append(elem.get('href'))
        return next_pages_links
