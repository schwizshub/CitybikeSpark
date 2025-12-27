@echo off
cd /d "c:\Data\Citybike\"
python citybikes_downloader.py >> logs\download_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log 2>&1
``_
