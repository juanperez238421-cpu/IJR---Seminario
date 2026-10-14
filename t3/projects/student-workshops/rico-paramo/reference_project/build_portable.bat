@echo off
setlocal
cd /d "%~dp0"

if not exist .venv (
  py -3.12 -m venv .venv
  if errorlevel 1 goto :failed
)

call .venv\Scripts\activate.bat
python -m pip install -r requirements-build.lock.txt
if errorlevel 1 goto :failed

pyinstaller --noconfirm --clean --onefile --name PortableVisualShow main.py
if errorlevel 1 goto :failed

if not exist PORTABLE_BUILD mkdir PORTABLE_BUILD
copy /Y dist\PortableVisualShow.exe PORTABLE_BUILD\PortableVisualShow.exe
copy /Y config.json PORTABLE_BUILD\config.json
copy /Y launch.bat PORTABLE_BUILD\launch.bat
copy /Y README_PORTABLE.txt PORTABLE_BUILD\README_PORTABLE.txt

echo.
echo Build ready in PORTABLE_BUILD
pause
exit /b 0

:failed
echo Build failed. Use Python 3.12 and inspect the error above.
pause
exit /b 1
