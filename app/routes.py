from app import app
from app import db
from app.models import CryptoPrice

from flask import jsonify, request, render_template

import requests
import time


def custom_jsonify(params, status_code):
    response = jsonify(params)
    response.status_code = status_code
    return response


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/v1/current_price')
def v1_current_price():
    curr_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    rows = db.session.query(CryptoPrice).filter(CryptoPrice.price_date == curr_date).all()
    result = {}
    for row in rows:
        result[row.crypto_type] = round(row.price, 4)
    return jsonify(result)


@app.route('/v1/history', methods=['GET'])
def v1_history():
    supported_crypto_type = ('btc', 'doge', 'eth', 'ltc')
    crypto_type = request.args.get('type', 'all')
    num_days = request.args.get('num_days', 7)

    try:
        num_days = int(num_days)
    except ValueError:
        status = '[ERROR] Unsupported num_days: {}'.format(num_days)
        return custom_jsonify({'status': status, 'status_code': '400', 'data': []}, 400)

    crypto_type = crypto_type.lower()
    start_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - (num_days * 24 * 60 * 60)))
    rows = []
    if crypto_type in supported_crypto_type:
        rows = db.session.query(CryptoPrice).filter(CryptoPrice.price_date > start_date).filter(CryptoPrice.crypto_type == crypto_type).all()
    elif crypto_type == 'all':
        rows = db.session.query(CryptoPrice).filter(CryptoPrice.price_date > start_date).all()
    else:
        status = '[ERROR] Unsupported crypto_type: {}'.format(crypto_type)
        return custom_jsonify({'status': status, 'status_code': '400', 'data': []}, 400)

    result = []
    for row in rows:
        temp = {
            'date': str(row.price_date),
            'crypto_type': row.crypto_type,
            'price': row.price,
            'tx_volume': row.tx_volume
        }
        result.append(temp)
    return jsonify(
        {
            'status': 'Success',
            'status_code': 200,
            'data': result
        }
    )
