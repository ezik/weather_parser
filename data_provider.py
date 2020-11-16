# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
from db_initializer import DatabaseUpdater
from image_maker import ImageMaker
from utils import forecast_dates
from weather_maker import WeatherMaker
import logging


def handle_date_str(a, b):
    frmt = '%Y-%m-%d'
    if datetime.strptime(a, frmt) and datetime.strptime(b, frmt):
        return True
    else:
        print('Incorrect input')


logger = logging.getLogger()
logging.basicConfig(filename='weather_parser.log', level=logging.DEBUG)

dbUpdater = DatabaseUpdater()


class DataProvider:

    def load_forecast_past_db(self):
        """
        Requests data from site for the past week and inserts it into db
        :return: None
        """
        today = date.today()
        past_date = date.today() - timedelta(days=7)

        try:
            missing_dates = self.get_missing_dates(past_date, today)
            if missing_dates:
                print('Загружаю данные за прошлую неделю...')
                self.add_data_to_db(missing_dates)
        except Exception as err:
            logger.error(err, exc_info=True)

    def load_forecast_range_db(self):
        """
        Requests data for user dates from site and inserts it into db
        :return: None
        """
        try:
            sdate_str, edate_str = self.get_user_dates()
            sdate = date.fromisoformat(sdate_str)
            edate = date.fromisoformat(edate_str)

            missing_dates = self.get_missing_dates(sdate, edate)
            if missing_dates:
                print('Загружаю недостающие данные...')
                self.add_data_to_db(missing_dates)
            else:
                print('Данные есть в базе')
        except Exception as err:
            logger.error(err, exc_info=True)

    def get_missing_dates(self, sdate, edate):
        """
        Difference between user-requested dates and existing DB dates
        :param sdate: Date object, start date for forecasts request
        :param edate: Date object, end date for forecasts request
        :return: List of dates strings which absent in DB
        """
        db_existing_dates = set(dbUpdater.get_dates_range(sdate, edate))
        dates = forecast_dates(sdate=sdate, edate=edate)
        absent_dates = [d for d in dates if d not in db_existing_dates]
        return absent_dates

    def add_data_to_db(self, missing_dates):
        """
        Get data from site and insert into DB
        :param missing_dates: List of dates strings absent in DB
        :return: None
        """
        weather = WeatherMaker(missing_dates)
        forecasts_from_site_lst = weather.get_forecast_data()
        dbUpdater.insert_forecasts(forecasts_from_site_lst)

    def show_forecast_range_db(self):
        """
        Print results from DB for requested range
        :return: None
        """
        results = self.get_forecast_range_from_db()
        if results:
            for w in results:
                print(f'Date: {w.date}, Weather: {w.weather_type}, Temperature (Day Night): {w.temperature}')
        else:
            print("К сожалению на эти даты прогноза в базе нет.")

    def create_forecast_images(self):
        """
        Create forecast images basing on templates
        :return: None
        """
        results = self.get_forecast_range_from_db()
        if results:
            for w in results:
                im = ImageMaker(w.date, w.weather_type, w.temperature)
                im.write_text()
            print("Готово")
        else:
            print("К сожалению на эти даты прогноза в базе нет.")

    def get_forecast_range_from_db(self):
        """
        Gets dates range from user and returns forecasts from DB
        :return: Forecasts list from DB for user-requested dates range
        """
        sdate_str, edate_str = self.get_user_dates()
        sdate = date.fromisoformat(sdate_str)
        edate = date.fromisoformat(edate_str)
        return dbUpdater.get_forecasts_range(sdate=sdate, edate=edate)

    def get_user_dates(self):
        """
        Gets user input and returns date strings tuple
        :return: Tuple of start and end dates
        """
        print("Укажите дату начала прогноза в формате 'YYYY-MM-DD'")
        sdate_str = input('>> ')
        print("Укажите дату конца прогноза в формате 'YYYY-MM-DD'")
        edate_str = input('>> ')
        if handle_date_str(sdate_str, edate_str):
            return sdate_str, edate_str

    def show_forecast_all(self):
        """
        Prints all existing forecasts from DB
        :return: None
        """
        for el in dbUpdater.get_forecasts():
            print(f'Date: {el.date}, Weather: {el.weather_type}, Temperature (Day Night): {el.temperature}')
