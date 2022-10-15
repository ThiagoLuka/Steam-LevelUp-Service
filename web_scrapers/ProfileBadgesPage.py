import requests

from lxml import html, etree

from web_scrapers.SteamWebPage import SteamWebPage


class ProfileBadgesPage(SteamWebPage):

    def requires_login(self) -> bool:
        return False

    def cookies_to_login(self) -> list:
        return ['steamLoginSecure']

    def headers_to_login(self) -> list:
        return []

    def scrap(self, scrap_params, cookies: dict):
        main_url = super().BASESTEAMURL + 'profiles/' + scrap_params['steam_id'] + '/badges/?sort=a'
        response = requests.get(main_url, cookies=cookies)
        main_page_tree = html.fromstring(response.content)

        self.__scrap_single_page(main_page_tree)
        next_pages_urls = self.__get_next_pages_links(main_page_tree, main_url)

        for url in next_pages_urls:
            response = requests.get(url, cookies=cookies)
            page_tree = html.fromstring(response.content)
            self.__scrap_single_page(page_tree)

    def interact(self, action: dict, cookies: dict, headers: dict):
        pass

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
                print(f'{game_market_hash} {game_title}')

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
