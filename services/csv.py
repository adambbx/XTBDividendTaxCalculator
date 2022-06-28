import pandas as pd
from pandas import DataFrame


def import_transactions_from_csv(csv_filepath: str) -> DataFrame:
    """Import Pandas dataframe from the csv file with XTB cash flow transactions.

    Args:
        csv_filepath (str): the path of the csv file

    Returns:
        DataFrame
    """
    return pd.read_csv(csv_filepath, sep=';')
