from typing import Optional, List

import requests

from services.settings import BASE_NBP_URL
from services.utils import PreviousDate


class NPBApiClient:
    """
    A very simple NPB API wrapper to fetch the exchange rate between some currency and PLN.
    """

    def __init__(self) -> None:
        self.days_ago = 10

    def fetch_exchange_rate(self, currency: str, date: str) -> Optional[float]:
        """Fetch the average exchange rate between the currency and PLN for the previous business day.

        Args:
            currency (str): the currency to fetch the exchange rate
            date (str): the date

        Returns:
            Optional[float]: the exchange rate
        """
        start_date, end_date = PreviousDate.get(date, self.days_ago), PreviousDate.get(date, 0)
        if response := requests.get(f'{BASE_NBP_URL}/{currency}/{start_date}/{end_date}/'):
            return self._get_average_exchange_rate_from_prev_business_day(end_date, response.json().get('rates'))

    def _get_average_exchange_rate_from_prev_business_day(self, end_date: str, rates: List[dict]):
        exchange_rate = rates.pop()
        while rates and exchange_rate['effectiveDate'] == end_date:
            exchange_rate = rates.pop()
        return exchange_rate.get('mid')
