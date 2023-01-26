from lxml import html


class ItemMarketPageCleaner:

    def __init__(self, page_bytes: bytes):
        self.__page: html.HtmlElement = html.fromstring(page_bytes)

    def item_url_is_valid(self) -> bool:
        if self.__page.find_class('market_listing_iteminfo'):
            return True
        elif self.__page.find_class('market_listing_table_message'):
            return False
        else:
            raise Exception('Unknown page response')
