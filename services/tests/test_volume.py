import pandas as pd
import pytest

from services.volume import ShareVolumeCounter, CommentParser


@pytest.fixture
def purchased_shares():
    data = [
        ['123456789', 'Zakup akcji/ETF', '29.04.2022 20:17:24', 'TEST', 'OPEN BUY 80 @ 8.73', '-3000'],
        ['987654321', 'Zakup akcji/ETF', '30.04.2022 20:17:24', 'XYZ', 'OPEN BUY 80 @ 8.73', '-3000'],
        ['111144445', 'Sprzedaż akcji/ETF', '14.05.2022 19:13:42', 'XYZ', 'OPEN SOLD 40 @ 8.73', '1500'],
    ]
    return pd.DataFrame(data, columns=['ID', 'Type', 'Time', 'Symbol', 'Comment', 'Amount'])


def test_count_volumes(purchased_shares):
    assert {'TEST': 80, 'XYZ': 40} == ShareVolumeCounter(purchased_shares).count()


def test_parse_volume_from_comment():
    assert 40 == CommentParser().parse_volume('OPEN BUY 40 @ 8.73')
    assert 1 == CommentParser().parse_volume('OPEN BUY 1/2 @ 8.73')
