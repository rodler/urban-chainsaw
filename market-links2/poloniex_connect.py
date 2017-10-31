import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import ssl

def get_quotes():
    context = ssl._create_unverified_context()
    ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/public?command=returnTicker'),context=context)
    return(json.loads(ret.read().decode('ascii')))

if __name__=="__main__":
    print(get_quotes())
