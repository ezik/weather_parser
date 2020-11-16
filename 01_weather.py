# -*- coding: utf-8 -*-
from data_provider import DataProvider
from utils import get_args

dp = DataProvider()
dp.load_forecast_past_db()
args = get_args()
if args[0] == '1':
    dp.load_forecast_range_db()
elif args[0] == '2':
    dp.show_forecast_range_db()
elif args[0] == '3':
    dp.create_forecast_images()
elif args[0] == '4':
    dp.show_forecast_all()
else:
    print('Такой опции нет')
