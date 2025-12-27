@echo off
REM ========================================
REM  CityBikes Data Downloader
REM  Code: c:\Git\CitybikeSpark
REM  Data: c:\Data\Citybike
REM ========================================

SETLOCAL EnableDelayedExpansion

REM Chemins séparés code/données
SET CODE_PATH=c:\Git\CitybikeSpark
SET DATA_PATH=c:\Data\Citybike
SET SCRIPT_PATH=%CODE_PATH%\citybikes_downloader.py
SET LOG_PATH=%DATA_PATH%\logs
SET TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
SET TIMESTAMP=%TIMESTAMP: =0%

REM Créer les répertoires de données si nécessaire
IF NOT EXIST "%DATA_PATH%" mkdir "%DATA_PATH%"
IF NOT EXIST "%DATA_PATH%\networks" mkdir "%DATA_PATH%\networks"
IF NOT EXIST "%DATA_PATH%\stations" mkdir "%DATA_PATH%\stations"
IF NOT EXIST "%DATA_PATH%\analysis" mkdir "%DATA_PATH%\analysis"
IF NOT EXIST "%LOG_PATH%" mkdir "%LOG_PATH%"

REM Vérifier que le script Python existe
IF NOT EXIST "%SCRIPT_PATH%" (
    echo ERROR: Python script not found at %SCRIPT_PATH%
    echo Please check your CODE_PATH in the batch file
    pause
    exit /b 1
)

REM Afficher les informations
echo ========================================
echo  CityBikes Download Started
echo ========================================
echo Code Path: %CODE_PATH%
echo Data Path: %DATA_PATH%
echo Script: %SCRIPT_PATH%
echo Log: %LOG_PATH%\download_%TIMESTAMP%.log
echo ========================================
echo.

REM IMPORTANT: Rester dans le répertoire du code (pour imports Python éventuels)
cd /d "%CODE_PATH%"

REM Exécuter le script Python avec logging
python "%SCRIPT_PATH%" 2>&1 | tee "%LOG_PATH%\download_%TIMESTAMP%.log"

REM Vérifier le code de retour
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  ERROR: Download failed!
    echo  Check log: %LOG_PATH%\download_%TIMESTAMP%.log
    echo ========================================
    exit /b %ERRORLEVEL%
) ELSE (
    echo.
    echo ========================================
    echo  SUCCESS: Download completed
    echo ========================================
)

ENDLOCAL
