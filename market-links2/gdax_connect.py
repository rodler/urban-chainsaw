from gdax.public_client import PublicClient

client = PublicClient()

def get_quotes(ticker):
    result = (client.get_product_ticker(ticker))
    return result

if __name__=="__main__":
    get_quotes('BTC-USD')
