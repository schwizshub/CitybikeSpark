$action = New-ScheduledTaskAction -Execute "python.exe" `
    -Argument "c:\Data\Citybike\citybikes_downloader.py"

$trigger = New-ScheduledTaskTrigger -Daily -At "02:00AM"

Register-ScheduledTask -TaskName "CityBikes_Daily_Download" `
    -Action $action -Trigger $trigger -Description "Téléchargement quotidien des données CityBikes"
