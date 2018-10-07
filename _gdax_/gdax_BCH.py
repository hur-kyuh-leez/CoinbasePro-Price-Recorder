from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
import gdax
import time
from pymongo import MongoClient

# MongoDB set up
client = MongoClient()
database = client['gdaxdb']

# Choosing Product
coin_name = 'BCH'
product_id = f'{coin_name}-USD'
collection = database[f'{coin_name}_USD_historical_data']

# Opening gdax Public Client
public_client = gdax.PublicClient()


def tick():
    date = round(time.time() * 1000)
    data = public_client.get_product_ticker(product_id=product_id)
    trades = public_client.get_product_order_book(product_id, level=2)
    price = float(data['price'])
    v_bid = sum([float(bid[1]) for bid in trades['bids']])
    v_ask = sum([float(ask[1]) for ask in trades['asks']])
    collection.insert({'date': date, 'price': price, 'v_bid': v_bid, 'v_ask': v_ask})
    print(date, price, v_bid, v_ask)


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10, max_instances=6872)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
