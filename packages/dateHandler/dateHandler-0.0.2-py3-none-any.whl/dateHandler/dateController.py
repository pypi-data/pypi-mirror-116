from datetime import datetime
from typing import Optional

import arrow
from dateutil import tz



class DateController:

    def __init__(self, timezone:Optional[str] = None) -> None:
        self.timezone = timezone if timezone else 'Europe/Paris'

    def get_current_date_str(self, format:Optional[str] = 'YYYY-MM-DD') -> str:
        """Get current date in a string format.

        :param format: Expected output format, defaults to 'YYYY-MM-DD'
        :type format: Optional[str], optional
        :return: A string representation of the current date
        :rtype: str
        """
        return arrow.get(datetime.now(tz.gettz(self.timezone))).format(format)

    def get_current_date_dt(self) -> arrow.arrow.Arrow:
        """Get current date in an Arrow Datetime Object.

        :return: Arrow Datetime Object
        :rtype: arrow.arrow.Arrow
        """
        return arrow.get(datetime.now(tz.gettz(self.timezone)))

    def get_dates_infos(self, date:str) -> dict:
        """This function allow user to enter a specific date 'YYYY-MM-DD' and get informations about it.

        :param date: String representation of the date to study
        :type date: str
        :return: Object containing several information about the date
        :rtype: dict
        """
        dt = arrow.get(date, 'YYYY-MM-DD')

        return {
            'currentDate': dt,
            'weekDayNumber': dt.isoweekday(),
            'weekDayName': dt.format('dddd'),
            'previousDay': dt.shift(days=-1),
            'nextDay': dt.shift(days=+1),
            'firstDayOfMonth': dt.floor("month"),
            'lastDayOfMonth': dt.ceil("month"),
            'numberOfDaysInMonth': (dt.ceil("month") - dt.floor("month")).days + 1,
            'elapsedDaysInMonth': int(dt.format('DD')),
            'remainingDaysInMonth': int(dt.ceil("month").format('DD')) - int(dt.format('DD')),
            'isMTD': self._is_mtd(dt),
            'weekNumber': datetime.date(dt.datetime).isocalendar()[1],
            'monthNumber': int(dt.format('MM')),
            'monthName': dt.format('MMMM'),
            'year': int(dt.format('YYYY')),
        }

    def _is_mtd(self, date):
        """Fonction permettant de déterminer si une date est dans le mois en cours

        :param date: Date à analyser
        :type date: str
        :return: Retourne Vrai si la date fait partie du mois en cours sinon Faux
        :rtype: bool
        """
        month, year = self.get_month_year_from_date(self.get_current_date_dt())
        month_dt, year_dt = self.get_month_year_from_date(arrow.get(date))
        if month == month_dt and year == year_dt:
            return True
        return False


if __name__ == '__main__':
    pass
