@echo off
REM ========================================
REM  CityBikes Data Downloader
REM  Automated download script
REM ========================================

SETLOCAL EnableDelayedExpansion

REM Définir les chemins
SET BASE_PATH=c:\Data\Citybike
SET SCRIPT_PATH=%BASE_PATH%\citybikes_downloader.py
SET LOG_PATH=%BASE_PATH%\logs
SET TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
SET TIMESTAMP=%TIMESTAMP: =0%

REM Créer le répertoire de base si nécessaire
IF NOT EXIST "%BASE_PATH%" (
    echo Creating base directory: %BASE_PATH%
    mkdir "%BASE_PATH%"
)

REM Créer le répertoire de logs si nécessaire
IF NOT EXIST "%LOG_PATH%" (
    echo Creating logs directory: %LOG_PATH%
    mkdir "%LOG_PATH%"
)

REM Vérifier que le script Python existe
IF NOT EXIST "%SCRIPT_PATH%" (
    echo ERROR: Python script not found at %SCRIPT_PATH%
    echo Please place citybikes_downloader.py in %BASE_PATH%
    pause
    exit /b 1
)

REM Afficher les informations
echo ========================================
echo  CityBikes Download Started
echo ========================================
echo Base Path: %BASE_PATH%
echo Script: %SCRIPT_PATH%
echo Log: %LOG_PATH%\download_%TIMESTAMP%.log
echo ========================================
echo.

REM Changer vers le répertoire de travail
cd /d "%BASE_PATH%"

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
