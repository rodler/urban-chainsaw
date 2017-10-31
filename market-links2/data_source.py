from bitfinex_connect import get_quotes as bitfinex_quotes
from btc_markets_connect import get_request as btc_markets_quotes
from bitstamp_connect import get_quotes as bitstmp_quotes
from kraken_connect import get_quotes as kraken_quotes
from gdax_connect import get_quotes as gdax_quotes
from  poloniex_connect import get_quotes as polon_quotes
from forex_python.converter import CurrencyRates
import time
import traceback
from threading import Thread,Lock,active_count
import queue
import zmq
context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind("tcp://127.0.0.1:5557")
curr = CurrencyRates()
usdaud = curr.get_rates('USD')['AUD']

class Quotes:
    def __init__(self):
        self.t = []

    def dispatch(self,data,lock,topic='',delay=5):
        lock.acquire()
        zmq_socket.send_pyobj([topic,data])
        lock.release()
        time.sleep(delay)

    def get_all_quotes(self,quotes):
        q = queue.Queue()
        lock = Lock()


        def bitfin():
            while True:
                try:
                    data = bitfinex_quotes('btcusd')
                    data['exchange'] = 'bitfinex'
                    data['currency'] = 'btcusd'
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_bitfin_sig = time.time()
                except:
                    print('**********exception in thread bitfinex**********')
                    print(traceback.format_exc())
                    time.sleep(2)

        def btcm():
            while True:
                try:
                    data = btc_markets_quotes('BTC','AUD')
                    data['exchange'] = 'btc_markets'
                    data['currency'] = 'btcaud'
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_btcm_sig = time.time()
                except:
                    print('**********exception in thread btc-markets**********')
                    print(traceback.format_exc())
                    time.sleep(2)

        def polon():
            while True:
                try:
                    data = dict(polon_quotes())['USDT_BTC']
                    data['exchange'] = 'poloniex'
                    data['currency'] = 'btcusd'
                    data['bid'] = data['highestBid']
                    data['ask'] = data['lowestAsk']
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_polon_sig = time.time()
                except:
                    print('**********exception in thread poloniex**********')
                    print(traceback.format_exc())
                    time.sleep(2)
        def btstmp():
            while True:
                try:
                    data = bitstmp_quotes('btcusd')
                    data['exchange'] = 'bitstamp'
                    data['currency'] = 'btcusd'
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_bitstmp_sig = time.time()
                except:
                    print('**********exception in thread bitstamp**********')
                    print(traceback.format_exc())
                    time.sleep(2)

        def kraken():
            while True:
                try:
                    data = kraken_quotes('XXBTZUSD')
                    data['exchange'] = 'kraken'
                    data['currency'] = 'btcusd'
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_kraken_sig = time.time()
                except:
                    print('**********exception in thread kraken**********')
                    print(traceback.format_exc())
                    time.sleep(2)

        def gdax():
            while True:
                try:
                    data = gdax_quotes('BTC-USD')
                    data['exchange'] = 'gdax'
                    data['currency'] = 'btcusd'
                    data['usdaud'] = usdaud
                    self.dispatch(data,lock,topic='market-update')
                    self.last_gdax_sig = time.time()
                    print('**********exception in thread gdax**********')
                    print(traceback.format_exc())
                except:
                    time.sleep(2)

        def start_threads():
            for func in [bitfin,btcm,polon,btstmp,kraken,gdax,heartbeat]:
                self.t.append(Thread(target=func,args=()))
                self.t[-1].start()

        def heartbeat():
            while True:
                time.sleep(10)
                print('still_running .',time.time(),'threads:',active_count())
                self.dispatch({},lock,topic='heartbeat')

                #if active_count() > 15 and (self.last_reset-time.time())>300:
                #    for thrd in self.t:
                #       thrd.stop()
                #      start_threads()
                #    self.last_reset = time.time()
                #elif active_count() > 15 and (self.last_reset-time.time())<300:
                #    print('***********something is wrong*********')
		
                timeout_limit = 15.0
                if active_count() < 25:
                    if time.time()-self.last_bitfin_sig > timeout_limit:
                        self.t.append(Thread(target=bitfin,args=()))
                        self.t[-1].start()
                        print('****Bitfinex Thread Restarted****')
                    elif time.time()-self.last_btcm_sig > timeout_limit:
                        self.t.append(Thread(target=btcm,args=()))
                        print('****BTCM Thread Restarted****')
                    elif time.time()-self.last_polon_sig > timeout_limit:
                        self.t.append(Thread(target=polon,args=()))
                        self.t[-1].start()
                        print('****Poloniex Thread Restarted****')
                    elif time.time()-self.last_bitstmp_sig > timeout_limit:
                        self.t.append(Thread(target=btstmp,args=()))
                        self.t[-1].start()
                        print('****Bitstamp Thread Restarted****')
                    elif time.time()-self.last_kraken_sig > 5.0:
                        self.t.append(Thread(target=kraken,args=()))
                        self.t[-1].start()
                        print('****Kraken Thread Restarted****')
                    elif time.time()-self.last_gdax_sig > 5.0:
                        self.t.append(Thread(target=gdax,args=()))
                        self.t[-1].start()
                        print('****GDAX Thread Restarted****')

        start_threads()

if __name__=="__main__":
    get_q = Quotes()
    quotes = get_q.get_all_quotes({})
