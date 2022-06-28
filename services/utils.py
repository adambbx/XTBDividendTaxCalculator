from datetime import datetime, timedelta


class PreviousDate:
    """
    This class returns the date n days ago.
    """

    @classmethod
    def get(cls, date: str, days_ago: int) -> str:
        """Get the date n days ago.

        Args:
            date (str): the date string
            days_ago (int): the number of days ago

        Returns:
            str
        """
        date_obj = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        return (date_obj - timedelta(days=days_ago)).strftime('%Y-%m-%d')
