set DIR=%~dp0
set DIR=%DIR:~0,-1%

pip install virtualenv
python -m venv venv
call %DIR%\venv\Scripts\activate.bat
pip install -r %DIR%\requirements.txt

set NAME=termer
set ENTRY_POINT=%DIR%\main.py
set TMP=%DIR%\tmp
set TMP_APP=%TMP%\application
set TMP_WP=%TMP%\build
set TMP_OUT=%TMP_APP%\main\*
set BLD_DIR=%DIR%\build
set BLD_DBG=%BLD_DIR%\%NAME%_debug.zip
set BLD_PRD=%BLD_DIR%\%NAME%.zip
set CUSTOM_TKINTER="%DIR%/venv/Lib/site-packages/customtkinter;customtkinter/"

mkdir %BLD_DIR%
del /s /q %BLD_DIR%

pyinstaller --noconfirm --onedir --distpath %TMP_APP% --workpath %TMP_WP% --specpath %TMP% --add-data %CUSTOM_TKINTER% %ENTRY_POINT% --clean --console 
7z a -tzip %BLD_DBG% %TMP_OUT%

pyinstaller --noconfirm --onedir --distpath %TMP_APP% --workpath %TMP_WP% --specpath %TMP% --add-data %CUSTOM_TKINTER% %ENTRY_POINT% --clean --noconsole 
7z a -tzip %BLD_PRD% %TMP_OUT%

rmdir /s /q %TMP%

call venv\Scripts\deactivate.bat
