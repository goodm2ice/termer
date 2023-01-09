#!/bin/sh
pip install virtualenv
python -m venv venv
$PWD/venv/Scripts/activate
pip install -r $PWD/requirements.txt

NAME=termer
ENTRY_POINT=$PWD/main.py
TMP=$PWD/tmp
TMP_APP=$TMP/application
TMP_WP=$TMP/build
TMP_OUT=$TMP_APP/main/*
BLD_DIR=$PWD/build
BLD_DBG=$BLD_DIR/$NAME_debug.zip
BLD_PRD=$BLD_DIR/$NAME.zip
CUSTOM_TKINTER="$PWD/venv/Lib/site-packages/customtkinter;customtkinter/"

mkdir $PWD/build
rm -rf $PWD/build/*

pyinstaller --noconfirm --onedir --distpath $TMP_APP --workpath $TMP_WP --specpath $TMP --add-data $CUSTOM_TKINTER $ENTRY_POINT --clean --console
zip $BLD_DBG $TMP_OUT

pyinstaller --noconfirm --onedir --distpath $TMP_APP --workpath $TMP_WP --specpath $TMP --add-data $CUSTOM_TKINTER $ENTRY_POINT --clean --noconsole
zip $BLD_PRD $TMP_OUT
