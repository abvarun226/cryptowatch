# Crypto Watch

A dashboard for cryptocurrency rates


Crypto Data API
===============
API : https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_INTRADAY&symbol=BTC&market=USD&apikey=DEMO

Get the API key from this site, https://www.alphavantage.co


How to build
============
Build the docker image, using this command,
```
sudo docker build -t cryptowatch:testing .
```

How to setup
============
During the initial setup, run `./inf/setup_password.sh.example` script (Replace *<PASSWORD>* and *<ALPHAVANTAGE_API_KEY>* with actually passwords).

This will setup postgres database along with initial seed data.
```
bash ./inf/setup_password.sh
```

And then start the cryptowatch container. Use the appropriate postgres DB password and alphavantage API key.
```
sudo docker run --link crypto_postgres:postgres --restart=always -p 80:80 -e REFRESH_INTERVAL=30 -e DATABASE_URI='postgres://crypto:<PASSWORD>@postgres:5432/cryptowatch' -e CRYPTO_API_KEY='<ALPHAVANTAGE_API_KEY>' -d --name cryptowatch cryptowatch:testing
```

Make sure that no other process is using port 80 on your host.

Website will be available on this address, http://localhost
