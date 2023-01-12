$DIR = $PWD | Select-Object -Expand Path

pip install virtualenv
python -m venv venv
Invoke-Expression -Command "$DIR\venv\Scripts\activate.ps1"
pip install -r "$DIR\requirements.txt"

$VERSION = 'v0.1.0'
$NAME = 'Termer'
$ENTRY_POINT = "$DIR\src\main.py"
$TMP = "$DIR\tmp"
$TMP_APP = "$TMP\application"
$TMP_WP = "$TMP\build"
$TMP_OUT = "$TMP_APP\main"
$BLD_DIR = "$DIR\build"
$BLD_DBG = "$BLD_DIR\$NAME" + "_debug"
$BLD_PRD = "$BLD_DIR\$NAME"
$CUSTOM_TKINTER = '"' + "$DIR/venv/Lib/site-packages/customtkinter;customtkinter/" + '"'

If (!(Test-Path -PathType Container $BLD_DIR)) {
    New-Item -Path $DIR -Name 'build' -ItemType 'directory'
} else {
    Remove-Item -Recurse -Force $BLD_DIR/*
}

If (!(Test-Path -PathType Container $TMP)) {
    New-Item -Path $DIR -Name 'tmp' -ItemType 'directory'
}

Function BuildProject {
    param (
        [String]$BUILD_DIR,
        [String]$INSTALLER_PATH,
        $SHOW_CONSOLE
    )
    $cmd = @($ENTRY_POINT, '--noconfirm', '--onedir', "--distpath $TMP_APP", "--workpath $TMP_WP", "--specpath $TMP", "--add-data $CUSTOM_TKINTER", '--clean')
    If ($SHOW_CONSOLE) {
        $cmd += '--console'
    } else {
        $cmd += '--window'
    }
    $cmd = $cmd -join ' '
    Invoke-Expression "pyinstaller $cmd"
    Move-Item -Path $TMP_OUT -Destination $BUILD_DIR
    7z a -tzip "$BUILD_DIR.zip" $BUILD_DIR
    ((Get-Content -Path $INSTALLER_PATH -Raw) -replace '@VERSION@', $VERSION) | Set-Content -Path "$TMP\make_installer.nsi"
    makensis "$TMP\make_installer.nsi"
    Remove-Item -Recurse -Force $BUILD_DIR
    Remove-Item "$TMP\make_installer.nsi"
}

BuildProject $BLD_DBG 'debug_installer_template.nsi' $true
BuildProject $BLD_PRD 'prod_installer_template.nsi' $false

Remove-Item -Recurse -Force $TMP
