#!/usr/bin/env python3

import datetime
import requests
import time

domain = "https://api.btcmarkets.net"

def get_request(A,B):
    uri = "/market/%s/%s/tick"%(A,B)
    url = domain + uri
    r = requests.get(url, verify=True)

    ask = str(r.json()["bestAsk"])
    bid = str(r.json()["bestBid"])
    last = str(r.json()["lastPrice"])
    spread = str(round(r.json()["bestAsk"] - r.json()["bestBid"], 2))
    tstamp = r.json()["timestamp"]
    ltime = time.ctime(tstamp)
    utime = time.asctime(time.gmtime(tstamp))

    return({'bid':bid,'ask':ask,'spread':spread,'last':last,'utime':utime})

def run():
    while True:
        get_request()
        time.sleep(1)

if __name__=="__main__":
    run()
