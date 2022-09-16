import requests
from lxml import html
from abc import abstractmethod, ABC


class SteamWebPage(ABC):

    BASESTEAMURL = 'https://steamcommunity.com/'

    @abstractmethod
    def __generate_urls(self):
        pass

    @abstractmethod
    def __make_requests(self):
        pass

    @abstractmethod
    def __handle_responses(self):
        pass

    @abstractmethod
    def __save_results(self):
        pass


class BadgesPage(SteamWebPage):

    def __init__(self, steam_id: str) -> None:
        self.__main_page_url = self.BASESTEAMURL + 'profiles/' + steam_id + '/badges/?sort=a'
        self.__all_pages_url = [self.__main_page_url]
        self.__steam_id: str = steam_id

    def generate_all_urls(self):
        try:
            response = requests.get(self.__main_page_url)
            page_tree = html.fromstring(response.content)
            for elem in page_tree.find_class('pagelink'):
                elem.make_links_absolute(self.__main_page_url)
                if elem.get('href') not in self.__all_pages_url:
                    self.__all_pages_url.append(elem.get('href'))
        except Exception as e:
            print(e)

        print(self.__all_pages_url)


if __name__ == '__main__':
    BadgesPage('76561198255516125').generate_all_urls()
