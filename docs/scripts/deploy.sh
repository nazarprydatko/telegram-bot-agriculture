#!/bin/bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
pkill -f main.py
nohup python main.py > logs/bot.log 2>&1 &
echo "Deployment complete and bot restarted."
