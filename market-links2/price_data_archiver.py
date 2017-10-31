import zmq
from db_connector import db_init,db_insert
from db_connector import c as cursor
import time

def write_data(quote):
    exch_rate = quote['usdaud']
    print(quote['bid'],quote['ask'],quote['exchange'])
    bid = quote['bid']
    ask = quote['ask']
    exchange = quote['exchange']
    symbol = quote['currency']
    timestamp = time.time()
    table_name = 'btc_quotes'
    db_insert(table_name,timestamp,symbol,exchange,bid,ask,0,0,exch_rate)


def run():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect ("tcp://localhost:%s" %(5557))
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        # print(socket.recv_pyobj()['exchange'])
        topic,data = socket.recv_pyobj()
        if topic == 'market-update':
            write_data(data)

        elif topic == 'heartbeat':
            print('****heartbeat****')

def test_db():
    cursor.execute('SELECT * from btc_quotes')
    print(cursor.fetchall())

if __name__=="__main__":
    # db_init('btc_quotes')
    run()
    #test_db()
