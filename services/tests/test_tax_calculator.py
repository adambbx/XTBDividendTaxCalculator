import pandas as pd
import pytest

from services.nbp_api import NPBApiClient
from services.tax_calculator import XTBDividendTaxCalculator


@pytest.fixture
def dividends():
    data = [
        ['987654321', 'Dywidenda', '30.04.2022 20:17:24', 'TEST.US', 'TEST.US USD 0.3623/ SHR', '13.75'],
        ['987654321', 'Dywidenda', '30.04.2022 20:17:24', 'UDVD.UK', 'UDVD.UK USD 0.3623/ SHR', '13.75'],
    ]
    return pd.DataFrame(data, columns=['ID', 'Type', 'Time', 'Symbol', 'Comment', 'Amount'])


def test_get_dividend_tax_in_pln(mocker, dividends):
    mocker.patch.object(NPBApiClient, 'fetch_exchange_rate', return_value=4.0, autospec=True)
    tax_calculator = XTBDividendTaxCalculator(
        volumes_by_tickers={'UDVD.UK': 9, 'TEST.US': 13},
        withholding_tax_by_tickers={'UDVD.UK': 0, 'TEST.US': 0.15}
    )
    assert 3.23 == tax_calculator.get_dividend_tax_in_pln(dividends)
