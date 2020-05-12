import requests

url = 'https://prime.exchangerate-api.com/v5/71116ad855e009ecb51fc45c/latest/USD'
response = requests.get(url)
data = response.json()


def currency_rate(currency):
    '''Returns current rate of given currency in relation to 1 usd. '''
    return data['conversion_rates'].get(currency)

