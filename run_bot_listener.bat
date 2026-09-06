@echo off
cd /d C:\Users\mitez\tn_politics_agent
C:\Users\mitez\AppData\Local\Programs\Python\Python313\python.exe -c "from alerts.interactive_bot import run_bot_listener; run_bot_listener(poll_seconds=None)" >> bot_listener.log 2>&1
