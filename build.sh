#!/bin/sh
pip install virtualenv
python -m venv venv
$PWD/venv/Scripts/activate
pip install -r $PWD/requirements.txt

VERSION='v0.2.1'
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

buildProject() {
    BUILD_DIR=$1
    INSTALLER_PATH=$2
    SHOW_CONSOLE=$3
    PARAMS=()
    if $SHOW_CONSOLE; then
        $PARAMS+=( --console )
    else
        $PARAMS+=( --window )
    fi
    pyinstaller --noconfirm --onedir --distpath $TMP_APP --workpath $TMP_WP --specpath $TMP --add-data $CUSTOM_TKINTER $ENTRY_POINT --clean "${PARAMS[@]}"
    mv $TMP_OUT $BUILD_DIR
    zip $BUILD_DIR "$BUILD_DIR.zip"
    cp $INSTALLER_PATH "$TMP\make_installer.nsi"
    sed -i -e "s/@VERSION@/$VERSION/g" "$TMP\make_installer.nsi"
    makensis "$TMP\make_installer.nsi"
    rm -rf $BUILD_DIR
    rm "$TMP\make_installer.nsi"
}

buildProject $BLD_DBG 'debug_installer_template.nsi' true
buildProject $BLD_PRD 'prod_installer_template.nsi' false

rm -rf $TMP
