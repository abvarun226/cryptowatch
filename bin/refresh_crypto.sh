#!/bin/bash

while [ 1 ];do
    /usr/local/bin/python /cryptowatch/bin/refresh_crypto.py
    echo "Sleeping for ${REFRESH_INTERVAL}"
    sleep ${REFRESH_INTERVAL}
done
