import sys
sys.path.append('.')
from app import db
from app.models import CryptoPrice

for crypto_type in ('btc', 'doge', 'eth', 'ltc'):
    loop_start = True
    with open('data/' + crypto_type + '.csv', 'r') as fh:
        for line in fh:
            if loop_start:
                loop_start = False
                continue
            parts = line.strip().split(',')
            cdate = parts[0]
            tx_vol = parts[1]
            cprice = parts[4]
            row = db.session.query(CryptoPrice).filter(CryptoPrice.price_date == cdate).filter(CryptoPrice.crypto_type == crypto_type).first()
            if not row:
                row = CryptoPrice(price_date=cdate, price=cprice, crypto_type=crypto_type, tx_volume=tx_vol)
            row.price = cprice
            row.tx_volume = tx_vol
            db.session.add(row)
            db.session.commit()
