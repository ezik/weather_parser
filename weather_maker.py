# -*- coding: utf-8 -*-
import requests
import bs4
from datetime import date


class WeatherMaker:
    SETTINGS = {
        "Clear": ["clear"],
        "Rain": ["rain", "drizzle"],
        "Snow": ["sleet", "flurries", "snow"],
        "Cloud": ["cloudy", "overcasts", "overcast"]
    }

    def __init__(self, dates):
        self.dates = dates

    def get_url(self, coordinates, date):
        return f'https://darksky.net/details/{coordinates}/{date}/us12/en'

    def get_forecast_html(self, date):
        url = self.get_url("50.4501,30.5234", date)
        html = requests.get(url).text
        return bs4.BeautifulSoup(html, 'html.parser')

    def get_forecast_str(self, html_source):
        return html_source.select('p[id="summary"]')[0].text.lower()

    def get_temperatures(self, html_source):
        temp_lst = html_source.find_all('span', {"class": "temp"})
        # Temperature in Fahrenheits
        low_temp_f = temp_lst[0].contents[0][:-1]
        high_temp_f = temp_lst[1].contents[0][:-1]
        # Celsius conversion
        low_temp = str(self.fahrenheit_to_celsius(int(low_temp_f)))
        high_temp = str(self.fahrenheit_to_celsius(int(high_temp_f)))
        return low_temp, high_temp

    def weather_type(self, forecast_str):
        forecast_split = forecast_str.split()
        for key, values in self.SETTINGS.items():
            common = set(forecast_split).intersection(set(values))
            if len(common):
                return key
            else:
                continue

    def fahrenheit_to_celsius(self, temperature):
        return int((temperature - 32) * 5.0 / 9.0)

    def date_str_convert(self, date_str):
        return date.fromisoformat(date_str)

    def get_forecast_data(self):
        forecast_data = []
        for date in self.dates:
            res = {}
            html_source = self.get_forecast_html(date)
            forecast_str = self.get_forecast_str(html_source)
            low_temp, high_temp = self.get_temperatures(html_source=html_source)
            res['weather_type'] = self.weather_type(forecast_str=forecast_str)
            res['temperature'] = f'{high_temp} {low_temp}'
            res['date'] = self.date_str_convert(date)
            forecast_data.append(res)

        return forecast_data
