#!/bin/bash

# Cleanup
rm -rf app/static/scripts/js/*
rm -rf app/static/bower_components
rm -rf ./node_modules

find . -name '__pycache__' -type d -exec rm -rf {} \;

# install dependencies to build
pip install --upgrade pip
pip install -r inf/requirements.txt
yarn
yarn global add bower
bower --allow-root install

# browserify react jsx components
node node_modules/browserify/bin/cmd.js -d app/static/scripts/jsx/history.js -o app/static/scripts/js/history.js -t [ babelify --presets [ env react ] ]
node node_modules/browserify/bin/cmd.js -d app/static/scripts/jsx/index.js -o app/static/scripts/js/index.js -t [ babelify --presets [ env react ] ]
