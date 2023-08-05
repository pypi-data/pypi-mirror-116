from datetime import datetime
from dateutil import tz
import arrow


class DateController:
    """Class contenant des méhtodes support de dates
    """
    def get_now(self, format:str):
        """Méthode permettant de retourner la date du jour au format souhaité.

        :param format: Format de sortie souhaité par l'utilisateur. Pour retourner le datetime au format Arrow il faut passer le paramètre 'native'
        :type format: str
        :return: La date du jour
        :rtype: Datetime de class Arrow ou String
        """
        if format == 'native':
            return arrow.get(datetime.now(tz.gettz("Europe/Paris")))
        return arrow.get(datetime.now(tz.gettz("Europe/Paris"))).format(format)

    def get_yesterday(self):
        """Methode support permettant de retourner la date de la veille

        :return: Retourne la date de la veille au format YYYY-MM-DD
        :rtype: string
        """
        return arrow.get(datetime.now(tz.gettz("Europe/Paris"))).shift(days=-1).format('YYYY-MM-DD')

    def get_current_month(self):
        """Fonction permettant de retourner le numéro du mois actuel

        :return: retourne le numéro du mois actuel
        :rtype: int
        """
        dt = self.get_now('native')
        return int(dt.format('MM'))

    def get_current_year(self):
        """Fonction permettant de retourner le numéro de l'année en cours

        :return: Retourne le numéro de l'année en cours
        :rtype: int
        """
        dt = self.get_now('native')
        return int(dt.format('YYYY'))

    def get_month_year_from_date(self, dt):
        """Fonction permettant d'extraire l'année et le mois à partir d'une date

        :param dt: Date à partir de laquelle on veut extraire l'année et le mois
        :type dt: Datetime Arrow
        :return: L'année et le numéro du mois
        :rtype: tuple(int, int)
        """
        return int(dt.format('YYYY')), int(dt.format('MM'))

    def get_dates_infos(self, fromDate):
        """Fonction permettant d'extraire des informations à partir d'une date

        :param fromDate: Date à partir de laquelle on veut extraire les infos. Input au format YYYY-MM-DD
        :type fromDate: string
        :return: Une liste avec les infos : Date (format date Arrow), veille, 1er jour du mois et dernier jour du mois 
        :rtype: dict
        """
        return {
            'dt': arrow.get(fromDate, 'YYYY-MM-DD'),
            'previousDay': arrow.get(fromDate, 'YYYY-MM-DD').shift(days=-1),
            'firstDayOfMonth': arrow.get(fromDate, 'YYYY-MM-DD').floor("month"),
            'lastDayOfMonth': arrow.get(fromDate, 'YYYY-MM-DD').ceil("month"),
        }

    def is_mtd(self, date):
        """Fonction permettant de déterminer si une date est dans le mois en cours

        :param date: Date à analyser
        :type date: str
        :return: Retourne Vrai si la date fait partie du mois en cours sinon Faux
        :rtype: bool
        """
        month, year = self.get_month_year_from_date(self.get_now('native'))
        month_dt, year_dt = self.get_month_year_from_date(arrow.get(date))
        if month == month_dt and year == year_dt:
            return True
        return False