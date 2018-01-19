from app import db

class CryptoPrice(db.Model):
    __tablename__ = 'crypto_price'
    __table_args__ = ( db.UniqueConstraint('price_date', 'crypto_type', name='uniq_idx_1'), { } )
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    price_date = db.Column('price_date', db.Date, index=True)
    price = db.Column('price', db.Float)
    crypto_type = db.Column('crypto_type', db.String(10), index=True)
    tx_volume = db.Column('tx_volume', db.Float)

    def __repr__(self):
        return '<CryptoPrice {0} {1} {2}>'.format(self.price_date, self.crypto_type, self.price)
