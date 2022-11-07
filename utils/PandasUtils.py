import pandas as pd


class PandasUtils:

    @staticmethod
    def df_set_difference(df: pd.DataFrame, other_df: pd.DataFrame, column: str):
        return df[~df[column].isin(other_df[column])]
