from data_models.PandasDataModel import PandasDataModel
from data_models.PandasUtils import PandasUtils
from repositories.TradingCardsRepository import TradingCardsRepository


class TradingCards(
    PandasDataModel,
    tables={
        'item_trading_cards'
    },
    columns={
        'default': ('id', 'item_steam_id', 'game_id', 'set_number', 'foil'),
        'item_trading_cards': ('id', 'item_steam_id', 'game_id', 'set_number', 'foil'),
    },
    repository=TradingCardsRepository
):

    def __init__(self, table: str = 'default', **data):
        super().__init__(table, **data)

    def save(self):
        saved = TradingCards.get_all('item_trading_cards')
        new = PandasUtils.df_set_difference(self.df, saved.df, ['game_id', 'set_number', 'foil'])
        if new.empty:
            return
        cols_to_insert = TradingCards._get_class_columns('item_trading_cards')
        cols_to_insert.remove('id')
        zipped_data = PandasUtils.zip_df_columns(new, cols_to_insert)
        TradingCardsRepository.insert_multiples('item_trading_cards', cols_to_insert, zipped_data)

    @staticmethod
    def get_all(table: str = 'item_trading_cards', columns: list = None):
        if not columns:
            columns = TradingCards._get_class_columns(table)
        data = TradingCardsRepository.get_all(table, columns)
        return TradingCards._from_db(table, data)
