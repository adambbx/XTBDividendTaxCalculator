from services.nbp_api import NPBApiClient
from services.settings import BASE_NBP_URL


def test_npb_client_get_exchange_rate_success(requests_mock):
    requests_mock.get(
        f'{BASE_NBP_URL}/USD/2022-03-18/2022-03-28/',
        json={
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "060/A/NBP/2022",
                    "effectiveDate": "2022-03-27",
                    "mid": 4.1764
                },
                {
                    "no": "060/A/NBP/2022",
                    "effectiveDate": "2022-03-28",
                    "mid": 4.2784
                }
            ]
        })

    assert 4.1764 == NPBApiClient().fetch_exchange_rate('USD', '28.03.2022 10:22:12')


def test_nbp_api_client_get_exchange_rate_404_not_found(requests_mock):
    requests_mock.get(
        f'{BASE_NBP_URL}/XXX/2022-03-18/2022-03-28/',
        text='Not Found',
        status_code=404
    )
    assert not NPBApiClient().fetch_exchange_rate('XXX', '28.03.2022 10:22:12')
