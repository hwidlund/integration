@ ECHO OFF
REM run integrated gis data update script
echo Running data integration script runupdate.py...
C:\Python27\ArcGIS10.3\Python.exe G:\mypath\scripts\runupdate.py G:\mypath\config G:\mypath\logs G:\mypath\outputdata
if %errorlevel% neq 0 (
    echo Runupdate.py error %errorlevel%: check logs
    pause
    )
exit