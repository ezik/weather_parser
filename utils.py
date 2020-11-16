# -*- coding: utf-8 -*-
from datetime import date, timedelta

BASE_IMAGE = "./python_snippets/external_data/probe.jpg"


def forecast_dates(sdate, edate):
    """
    Calculates dates for requested range
    :param sdate: Date object, start date for forecasts request
    :param edate: Date object, end date for forecasts request
    :return: List of dates strings
    """
    max_future_date = date.today() + timedelta(days=10)
    if sdate > edate:
        sdate, edate = edate, sdate
    if edate > max_future_date:
        edate = max_future_date
    delta = edate - sdate
    dates_str_lst = [str(sdate + timedelta(days=i)) for i in range(delta.days + 1)]
    return dates_str_lst


def get_args():
    print("Вы используете утилиту для получения прогноза погоды за прошлое и немного в будущем. У Вас есть такие опции:"
          "\n1. Добавление прогнозов за диапазон дат в базу данных"
          "\n2. Получение прогнозов за диапазон дат из базы"
          "\n3. Создание открыток из полученных прогнозов"
          "\n4. Выведение полученных прогнозов на консоль\n")
    print("Выберите одну из опций указав ее номер")
    line = input('>> ')
    return line.split()
