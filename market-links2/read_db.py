from db_connector import db_init,db_insert
from db_connector import c as cursor

def test_db():
    cursor.execute('SELECT bid from btc_quotes where exchange="kraken"')
    print(cursor.fetchall())

if __name__=="__main__":
    # db_init('btc_quotes')
    #run()
    test_db()
