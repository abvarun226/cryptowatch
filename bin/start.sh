#!/bin/bash

# browserify react jsx components
node node_modules/browserify/bin/cmd.js -d app/static/scripts/jsx/history.js -o app/static/scripts/js/history.js -t [ babelify --presets [ env react ] ]
node node_modules/browserify/bin/cmd.js -d app/static/scripts/jsx/index.js -o app/static/scripts/js/index.js -t [ babelify --presets [ env react ] ]

FLASK_APP=crypto.py
flask run --port=5000
