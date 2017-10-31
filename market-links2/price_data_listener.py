import zmq
from forex_python.converter import CurrencyRates
import time

curr = CurrencyRates()

def parse_data(quote):
    exch_rate = quote['usdaud']
    if (quote['currency']=='btcusd'):
        print(quote['bid'],quote['ask'],quote['exchange'],time.time())
    else:
        print(float(quote['bid'])/exch_rate,float(quote['ask'])/exch_rate,quote['exchange'],time.time())


def run():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect ("tcp://localhost:%s" %(5557))
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        # print(socket.recv_pyobj()['exchange'])
        topic,data = socket.recv_pyobj()
        if topic == 'market-update':
            parse_data(data)
        elif topic == 'heartbeat':
            print('****heartbeat****')

if __name__=="__main__":
    run()
