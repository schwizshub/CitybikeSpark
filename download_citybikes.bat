@echo off
REM ========================================
REM  CityBikes Data Downloader
REM ========================================

SETLOCAL

SET CODE_PATH=c:\Git\CitybikeSpark
SET DATA_PATH=c:\Data\Citybike
SET SCRIPT_PATH=%CODE_PATH%\citybikes_downloader.py
SET LOG_PATH=%DATA_PATH%\logs
SET TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
SET TIMESTAMP=%TIMESTAMP: =0%
SET LOG_FILE=%LOG_PATH%\download_%TIMESTAMP%.log

REM Créer les répertoires
IF NOT EXIST "%DATA_PATH%" mkdir "%DATA_PATH%"
IF NOT EXIST "%DATA_PATH%\networks" mkdir "%DATA_PATH%\networks"
IF NOT EXIST "%DATA_PATH%\stations" mkdir "%DATA_PATH%\stations"
IF NOT EXIST "%DATA_PATH%\analysis" mkdir "%DATA_PATH%\analysis"
IF NOT EXIST "%LOG_PATH%" mkdir "%LOG_PATH%"

REM Vérifier le script
IF NOT EXIST "%SCRIPT_PATH%" (
    echo ERROR: Script not found at %SCRIPT_PATH%
    pause
    exit /b 1
)

echo ========================================
echo  CityBikes Download Started
echo  Time: %date% %time%
echo  Log: %LOG_FILE%
echo ========================================
echo.

REM Changer de répertoire
cd /d "%CODE_PATH%"

REM Exécuter avec log
echo [%date% %time%] Download started > "%LOG_FILE%"
python "%SCRIPT_PATH%" >> "%LOG_FILE%" 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Download failed! Check: %LOG_FILE%
    echo [%date% %time%] Download FAILED >> "%LOG_FILE%"
    exit /b %ERRORLEVEL%
) ELSE (
    echo.
    echo [SUCCESS] Download completed!
    echo [%date% %time%] Download SUCCESS >> "%LOG_FILE%"
    type "%LOG_FILE%"
)

ENDLOCAL
