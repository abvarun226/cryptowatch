import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgres://fake_user:fake_passwd@fake_host:5432/fake_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False

    REALTIME_CRYPTO_PRICE_API = os.environ.get('REALTIME_CRYPTO_PRICE_API') or \
        'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_INTRADAY'

    CRYPTO_API_KEY = os.environ.get('CRYPTO_API_KEY') or 'fake-api'
