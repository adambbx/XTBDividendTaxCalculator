from typing import Dict

from pandas import DataFrame

from services.nbp_api import NPBApiClient


class GrossDividend:
    """
    This class calculates the gross amount of dividend in a foreign currency.
    """

    def __init__(self, volumes_by_tickers: Dict[str, int]) -> None:
        self.volumes_by_tickers = volumes_by_tickers

    def get_amount(self, comment: str) -> float:
        """Return the gross amount of dividend from the the comment field.

        Args:
            comment (str): the comment field

        Returns:
            float
        """
        ticker, currency, raw_amount = comment.split(maxsplit=2)
        return self._dividend_per_share(raw_amount, ticker)

    def get_currency(self, comment: str) -> str:
        """Return the currency of the dividend.

        Args:
            comment (str): the comment

        Returns:
            str: the currency symbol
        """
        return comment.split(maxsplit=2)[1]

    def _dividend_per_share(self, raw_amount, ticker) -> float:
        return float(raw_amount.split('/')[0]) * self.volumes_by_tickers.get(ticker)


class XTBDividendTaxCalculator:
    """
    This class calculates the total amount of dividend tax (in PLN) from foreign companies,
    that must be paid to the tax office.
    Because dividends are in foreign the average exchange rate to PLN is calculated
    for the previous business day of the payment date.
    """

    def __init__(
            self,
            /, *,
            volumes_by_tickers: Dict[str, int],
            withholding_tax_by_tickers: Dict[str, float]
    ) -> None:
        """Initialize the dividend tax calculator.
        
        Args:
            volumes_by_tickers (Dict[str, int]): the volumes by ticker symbols
            withholding_tax_by_tickers (Dict[str, float]): the withholding taxes by ticker symbols
        """
        self.nbp_api_client = NPBApiClient()
        self.gross_dividend = GrossDividend(volumes_by_tickers)
        self.withholding_tax_by_tickers = withholding_tax_by_tickers

    def get_dividend_tax_in_pln(self, df: DataFrame) -> float:
        """Return the total dividend tax (in PLN) that must be paid to for the all dividends found in the transactions.
        Currently, the dividend tax in Poland is 19%. If a withholding tax (a tax already paid at origin) exists,
        it will reduce the percentage of the dividend tax that must be paid.
        For example, if the withholding tax was 15%, only 4% dividend tax paid extra.

        Args:
            df (DataFrame): the dataframe with all transactions

        Returns:
            float
        """
        df = df.loc[df['Type'] == 'Dywidenda']
        df = df[~df['Symbol'].str.endswith('PL')]
        df['Currency'] = df['Comment'].apply(self.gross_dividend.get_currency)
        df['GrossForeign'] = df['Comment'].apply(self.gross_dividend.get_amount)
        df['ExchangeRatePLN'] = df.apply(lambda x: self.nbp_api_client.fetch_exchange_rate(x.Currency, x.Time), axis=1)
        df['WithholdingTaxRate'] = df['Symbol'].apply(lambda ticker: self.withholding_tax_by_tickers.get(ticker, 0))
        df['DividendTaxRate'] = 0.19
        df['GrossPLN'] = df['GrossForeign'] * df['ExchangeRatePLN']
        df['TaxPLN'] = df['GrossPLN'] * (df['DividendTaxRate'] - df['WithholdingTaxRate'])
        total_tax = df['TaxPLN'].sum()
        return round(total_tax, 2)
