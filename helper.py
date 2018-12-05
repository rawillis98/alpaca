from datetime import datetime
import pandas as pd
import requests
import alpaca_trade_api as tradeapi
from pushbullet import Pushbullet

def getKey(f):
    with open(f, 'r') as key:
        for line in key:
            return line

def push(msg):
    print(msg)
    actuallyPush = True
    if actuallyPush:
        apiKey = getKey('pushbullet.key')
        pb = Pushbullet(apiKey)
        pb.push_note("Alpaca: Wood Gold", msg)


def getCurrentPrice(api, symbol):
    bar = api.get_barset(symbol, "minute")[symbol][-1]
    return sum([bar.o, bar.h, bar.l, bar.c])/4

def getAPI():
    endpoint = 'https://paper-api.alpaca.markets'
    key_id = getKey('alpaca_id.key')
    secret_key = getKey('alpaca_secret.key')
    api = tradeapi.REST(key_id, secret_key, endpoint)
    return api

def getHistory(symbol):
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&outputsize=full&apikey=A0P4")
    r = r.json()['Time Series (Daily)']
    hist = []
    dates = []
    for key in r.keys():
        dates.append(datetime.strptime(key, '%Y-%m-%d'))
        row = [float(x) for x in list(r[key].values())]
        hist.append(row)
    hist.reverse()
    dates.reverse()
    out = pd.DataFrame.from_records(hist, index = dates, columns = ["Open", "High", "Low", "Close", "Volume"])
    return out

def addReturnsColumn(a):
    returns = pd.Series(index = a.index)
    returns.iloc[0] = 0
    for i in range(1, len(a.index)):
        date = a.index[i]
        returns[date] = 100*(a.iloc[i]['Close']-a.iloc[i-1]['Close'])/a.iloc[i-1]['Close']
    a['Returns'] = returns
    return a
