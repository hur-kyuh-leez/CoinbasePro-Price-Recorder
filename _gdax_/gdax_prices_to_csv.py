"""Basic GDAX recorder, only records in CSV files"""

from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
import gdax
import time
import csv

# GDAX(Coinbase Pro) does not require keys for price data
public_client = gdax.PublicClient()

#input format ex)'ETH-USD'
def get_ticker_data(product_id):
    data = public_client.get_product_ticker(product_id=product_id)
    unix_GMT_time = (round(time.time() * 1000))  # one way to get GMT time
    trade_id = data['trade_id']
    price = data['price']
    size = data['size']
    bid = data['bid']
    ask = data['ask']
    volume = data['volume']
    return unix_GMT_time, trade_id, price, size, bid, ask, volume


def write_in_csv(product_id):
    with open('_gdax_/csv_data/%s.csv' % product_id, 'a') as f:
        wr = csv.writer(f)
        wr.writerow(get_ticker_data(product_id))


def cordecode():
    unix_GMT_time = (round(time.time() * 1000))
    print(unix_GMT_time)
    write_in_csv('BTC-USD')
    write_in_csv('ETH-USD')
    write_in_csv('BCH-USD')
    write_in_csv('LTC-USD')


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(cordecode, 'interval', seconds=10, max_instances=10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass



if __name__ == '__main__':
    main()







