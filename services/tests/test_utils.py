import pytest

from services.utils import PreviousDate


@pytest.mark.parametrize(
    'days_ago,end_date,start_date',
    [
        (10, '28.03.2022 12:15:38', '2022-03-18'),
        (1, '28.03.2022 12:15:38', '2022-03-27'),
        (3, '28.03.2022 12:15:38', '2022-03-25'),
    ]
)
def test_get_date_n_days_ago(days_ago, end_date, start_date):
    assert PreviousDate.get(end_date, days_ago) == start_date
