import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from forex_python.bitcoin import BtcConverter
from datetime import datetime
from datetime import timedelta

'''
I decided to play around a little bit with more than one way of getting the 
cryptocurrencies data, so BTC will be taken from Forex_python module, and
ETH & Dash using pandas
'''

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
DATE = datetime.now()

START = '{}{:02d}{:02d}'.format(DATE.year-1, DATE.month, DATE.day)
END = '{}{:02d}{:02d}'.format(DATE.year, DATE.month, DATE.day)


class CryptoForecaster:
    def __init__(self):
        pass

    @staticmethod
    def bitcoin_data():
        ''' Gets bitcoin values from last 365 days. '''
        b = BtcConverter()

        year_ago = DATE - timedelta(days=365)
        bitcoin_values = list(
            b.get_previous_price_list('USD', year_ago, DATE).values())

        return bitcoin_values

    # Splitted it to two methods, because I wanted it to be more explicit
    @staticmethod
    def ethereum_data():
        ''' Gets ethereum values from last 365 days. '''
        link = f'https://coinmarketcap.com/currencies/ethereum/historical-data?start={START}&end={END}'
        eth = pd.read_html(link)[2]

        ethereum_values = eth['Close**']
        return list(reversed(ethereum_values))

    @staticmethod
    def dash_data():
        ''' Gets dash values from last 365 days. '''
        link = f'https://coinmarketcap.com/currencies/dash/historical-data?start={START}&end={END}'
        dash = pd.read_html(link)[2]

        dash_values = dash['Close**']
        return list(reversed(dash_values))

    def months_names(self):
        ''' Names of last 12 months used in plot to display time series. '''
        m = DATE.month
        return MONTHS[m-1:] + MONTHS[:m+3]

    def predict(self, data):
        ''' Forecasts cryptocurrency value for the next 90 days (based on values from last 4 months). '''
        model = ARIMA(data[len(data)-120:], order=(3, 1, 1)).fit()
        return model.forecast(steps=90)[0]
