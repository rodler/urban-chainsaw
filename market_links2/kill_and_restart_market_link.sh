cd ~/btc-trader/market-links
kill $(ps aux | grep "python data_source.py" | awk '{ print $2 }')
/home/ubuntu/.virtualenvs/tribo/bin/python data_source.py >> data_source.log
