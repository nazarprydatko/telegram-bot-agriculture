#!/bin/bash
source venv/bin/activate
nohup python main.py > logs/bot.log 2>&1 &
echo "Bot started in background."
