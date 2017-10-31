import requests

def get_quotes(pair):
    r = requests.get(url='https://www.bitstamp.net/api/v2/ticker/%s'%pair)
    res = dict(r.json())
    return {k:float(res[k]) for k in res}

if __name__=="__main__":
    print(get_quotes('btcusd'))
