import json

from fire import Fire

from services.csv import import_transactions_from_csv
from services.tax_calculator import XTBDividendTaxCalculator
from services.volume import ShareVolumeCounter


def calculate_tax(csv_file: str, withholding_tax_file: str) -> None:
    transactions_df = import_transactions_from_csv(csv_file)
    with open(withholding_tax_file, 'r') as json_fl:
        total_divident_tax = XTBDividendTaxCalculator(
            volumes_by_tickers=ShareVolumeCounter(transactions_df).count(),
            withholding_tax_by_tickers=json.loads(json_fl.read())
        ).get_dividend_tax_in_pln(transactions_df)
        print(f'Total dividend tax: {total_divident_tax} PLN')


if __name__ == '__main__':
    Fire(calculate_tax)
