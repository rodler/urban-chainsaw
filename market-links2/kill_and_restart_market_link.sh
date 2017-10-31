cd "~/btc-trader/market-links2"
kill $(ps aux | grep "python data_source.py" | awk '{ print $2 }')
python data_source.py >> data_source.log
