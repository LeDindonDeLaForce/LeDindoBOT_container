#!/bin/sh
whoami
cd /home/ledindobot/
cp -r /BOT_DIR/* .
cp /BOT_DIR/.env .
python3.9 -m pipenv run python bot.py
exit 2
