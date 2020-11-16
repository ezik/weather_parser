# -*- coding: utf-8 -*-
import peewee
from playhouse.db_url import connect

database = peewee.SqliteDatabase("weather.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    weather_type = peewee.CharField()
    temperature = peewee.CharField()
    date = peewee.DateField(unique=True)


database.create_tables([Weather])

db = connect('sqlite:///weather.db')


class DatabaseUpdater(Weather):
    def insert_forecasts(self, forecasts_lst):
        with db:
            Weather.insert_many(forecasts_lst).on_conflict_ignore().execute()

    def get_forecasts_range(self, sdate, edate):
        """
        :param sdate: Date object for start date
        :param edate: Date object for end date
        :return: Forecasts list for the provided dates range from DB
        """
        delta = abs(edate - sdate)
        if sdate > edate:
            with db:
                results = Weather.select().where(Weather.date.between(edate, sdate))
        else:
            with db:
                results = Weather.select().where(Weather.date.between(sdate, edate))
        if delta.days > len(results):
            print('К сожалению, не для всех дат есть данные в БД')
        return results

    def get_dates_range(self, sdate, edate):
        """
        :param sdate: Date object for start date
        :param edate: Date object for end date
        :return: Dates list of existing forecasts in DB
        """
        results = self.get_forecasts_range(sdate, edate)
        dates = [str(el.date) for el in results]
        return dates


    def get_forecasts(self):
        """
        :return: Forecasts list for ALL entries in DB
        """
        with db:
            results = Weather.select().order_by(Weather.date)
        return results
