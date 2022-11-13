#!/bin/sh
cd /home/ledindobot/
cp -r /BOT_DIR/* .
cp /BOT_DIR/.env .
python3.10 -m pipenv run python bot.py
exit 2
