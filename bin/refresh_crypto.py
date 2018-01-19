import sys
sys.path.append('.')
sys.path.append('/cryptowatch')
from app import db
from app.models import CryptoPrice
from app import app
import asyncio
from aiohttp import ClientSession
import datetime
import json
import time
# import argparse


def process_data(data):
    volume_total = {}
    latest_price = {}
    final_data = {}
    try:
        crypto_type = data['Meta Data']['2. Digital Currency Code'].lower()
    except KeyError:
        print('[ERROR] Data returned by API is incorrect')
        return
    for k, v in data['Time Series (Digital Currency Intraday)'].items():
        price = round(float(v['1a. price (USD)']), 4)
        volume = round(float(v['2. volume']), 4)
        date = k.split()[0]
        if date not in volume_total:
            volume_total[date] = 0
        volume_total[date] += volume
        temp = int(time.mktime(datetime.datetime.strptime(k, "%Y-%m-%d %H:%M:%S").timetuple()))
        if latest_price.get(date, (temp, price))[0] <= temp:
            latest_price[date] = (temp, price)
        if crypto_type not in final_data:
            final_data[crypto_type] = {}
        final_data[crypto_type][date] = [latest_price[date][1], round(volume_total[date], 4)]
    for k, v in final_data.items():
        for k1, v1 in v.items():
            row = db.session.query(CryptoPrice).filter(CryptoPrice.price_date == k1).filter(CryptoPrice.crypto_type == k).first()
            if not row:
                row = CryptoPrice(price_date=k1, price=v1[0], crypto_type=k, tx_volume=v1[1])
            else:
                if row.price == v1[0] and row.tx_volume == v1[1]:
                    print('[INFO] Data already present in DB. Ignoring...')
                    continue
            row.price = v1[0]
            row.tx_volume = v1[1]
            print('[INFO] Adding row to db: {}'.format(row))
            db.session.add(row)
            db.session.commit()

async def fetch(url, session):
    async with session.get(url) as response:
        status_code = response.status
        if status_code == 200:
            return await response.json()
        else:
            print('[ERROR] cyrpto api returned an error: {}'.format(status_code))
            return None

async def run_request(urls):
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for data in responses:
            if data is not None:
                process_data(data)

def generate_urls():
    crypto_list = ('btc', 'doge', 'eth', 'ltc')
    crypto_api = app.config.get('REALTIME_CRYPTO_PRICE_API')
    api_key = app.config.get('CRYPTO_API_KEY')
    urls = []
    for crypto_type in crypto_list:
        api_url = crypto_api + '&symbol=' + crypto_type.upper() + '&market=USD&apikey=' + api_key
        urls.append(api_url)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run_request(urls))
    loop.run_until_complete(future)


def main():
    # parser = argparse.ArgumentParser(description='Update crypto price at a given interval')
    # parser.add_argument('--interval', type=int, default=30, help='Interval in seconds')
    # args = parser.parse_args()
    # interval = args.interval
    # while True:
    print('Running price update script')
    generate_urls()
    # print('sleeping for interval seconds')
    # time.sleep(interval)


if __name__ == '__main__':
    main()
