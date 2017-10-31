import krakenex
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context
k = krakenex.API()

def get_quotes(ticker):
    response = k.query_public('Ticker', {'pair': ticker})
    r = response['result'][ticker]
    op = {'bid':float(r['b'][0]),
            'bid_volume':float(r['b'][2]),
            'ask':float(r['a'][0]),
            'ask_volume':float(r['a'][2]),
            'timestamp':time.time()}
    return op

if __name__=="__main__":
    print(get_quotes('XXBTZUSD'))
