from typing import Dict

from pandas import DataFrame


class CommentParser:
    """
    This class parses a number of purchased/sold shares (volume) from the comment field.
    """

    def parse_volume(self, comment: str) -> int:
        """Parse a volume of purchased/sold shares from the comment.
        If shares were sold, return negative integer.

        Args:
            comment (str): the comment to parse

        Returns:
            int
        """
        raw_volume = comment.split(maxsplit=3)[2]
        volume = int(raw_volume.split('/')[0])
        return volume if comment.startswith('OPEN BUY') else -volume


class ShareVolumeCounter:
    """
    This class counts how many shares were purchased per company.
    """

    def __init__(self, transactions: DataFrame) -> None:
        self.transactions = transactions
        self.comment_parser = CommentParser()

    def count(self) -> Dict[str, int]:
        """Count currently held shares per company.

        Returns:
            Dict[str, int]
        """
        df = self.transactions.copy()
        df = df.loc[df['Type'].isin(['Zakup akcji/ETF', 'Sprzedaż akcji/ETF'])]
        df['Volume'] = df['Comment'].apply(self.comment_parser.parse_volume)
        return dict(df.groupby('Symbol')['Volume'].sum())
