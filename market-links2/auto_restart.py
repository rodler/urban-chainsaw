import zmq
from forex_python.converter import CurrencyRates
import time
from datetime import datetime
import os

curr = CurrencyRates()
TIMEOUT = 5
class Restart:
    def __init__(self):
        self.fid = open('restart.log','a')
        self.last_kraken_time=datetime.now()
        self.last_poloniex_time=datetime.now()
        self.last_bitstamp_time=datetime.now()
        self.last_gdax_time=datetime.now()
        self.last_btcm_time=datetime.now()
        self.last_bitfinex_time=datetime.now()

    def parse_data(self,quote):
        exch_rate = quote['usdaud']
        exchange = quote['exchange']
        if exchange == 'kraken':
            self.last_kraken_time = datetime.now()
        elif exchange == 'poloniex':
            self.last_poloniex_time = datetime.now()
        elif exchange == 'bitstamp':
            self.last_bitstamp_time = datetime.now()
        elif exchange == 'gdax':
            self.last_gdax_time = datetime.now()
        elif exchange == 'btc_markets':
            self.last_btcm_time = datetime.now()
        elif exchange == 'bitfinex':
            self.last_bitfinex_time = datetime.now()

        kraken = (datetime.now() - self.last_kraken_time).total_seconds()
        poloniex = (datetime.now() - self.last_poloniex_time).total_seconds()
        bitstamp = (datetime.now() - self.last_bitstamp_time).total_seconds()
        gdax = (datetime.now() - self.last_gdax_time).total_seconds()
        btcm = (datetime.now() - self.last_btcm_time).total_seconds()
        bitfinex = (datetime.now() - self.last_bitfinex_time).total_seconds()

        times = [kraken,poloniex,bitstamp,gdax,btcm,bitfinex]
        exceeded = [t>TIMEOUT for t in times]
        if sum(exceeded):
            self.fid.write('restart system at %s || %s'%(datetime.now(),times))
            print('++++++++RESTART NEEDED++++++++')
            os.system('bash kill_and_restart_market_link.sh')

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        socket.connect ("tcp://localhost:%s" %(5557))
        socket.setsockopt(zmq.SUBSCRIBE, b'')

        while True:
    	# print(socket.recv_pyobj()['exchange'])
            topic,data = socket.recv_pyobj()
            if topic == 'market-update':
                self.parse_data(data)
            elif topic == 'heartbeat':
                print('****heartbeat****')

if __name__=="__main__":
    restart = Restart()
    restart.run()
