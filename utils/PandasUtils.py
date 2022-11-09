import pandas as pd
from typing import Union


class PandasUtils:

    @staticmethod
    def df_set_difference(df: pd.DataFrame, other_df: pd.DataFrame, columns: Union[str, list]) -> pd.DataFrame:
        if isinstance(columns, str):
            return df[~df[columns].isin(other_df[columns])]
        if isinstance(columns, list):
            this_set = set(map(tuple, df[columns].values))
            other_set = set(map(tuple, other_df[columns].values))
            set_diff = this_set.difference(other_set)
            df_diff = pd.DataFrame(data=set_diff, columns=columns)
            return df.merge(df_diff)
