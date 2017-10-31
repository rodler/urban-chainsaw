import sqlite3
import time
conn = sqlite3.connect('example.db')
c = conn.cursor()

def db_init(table_name):
    c.execute('''CREATE TABLE %s (timestamp real, symbol text, exchange text,
            bid real, ask real, bid_volume real, ask_volume real,exchange_rate real)'''%table_name)

def db_insert(table_name,timestamp,symbol,exchange,bid,ask,bid_volume,ask_volume,exchage_rate):

    c.execute("INSERT INTO %s VALUES (%s,'%s','%s',%s,%s,%s,%s,%s)"
            %(table_name,timestamp,symbol,exchange,bid,ask,bid_volume,ask_volume,exchage_rate))
    conn.commit()

def db_close():
    conn.close()

def db_test():
    c.execute('DROP table test')
    db_init('test')
    timestamp = time.time()
    db_insert('test',timestamp,'BTCUSD','Bitfinex',100.00,100.02,21.21,34.41,1.67)
    c.execute('SELECT * FROM test WHERE timestamp = %s'%timestamp)
    result = (c.fetchall())
    assert(result[0][0] == timestamp)
    c.execute('DROP table test')

if __name__=="__main__":
    db_test()
