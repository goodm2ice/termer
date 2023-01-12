Name "Termer @VERSION@"
OutFile "..\build\Termer @VERSION@ Setup.exe"
InstallDir "$PROGRAMFILES\Termer\"
InstallDirRegKey HKLM SOFTWARE\NSIS_Termer "Install_Dir"

Section "Termer @VERSION@"
    SectionIn RO
    SetOutPath $INSTDIR
    File /r "..\build\termer\"
    WriteRegStr HKLM SOFTWARE\NSIS_Termer "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Termer" "DisplayName" " Termer @VERSION@ (только удаление)"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Termer" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
    CreateDirectory "$SMPROGRAMS\Termer"

    CreateShortCut "$SMPROGRAMS\Termer\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    CreateShortCut "$SMPROGRAMS\Termer\Termer.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
    CreateShortCut "$DESKTOP\Termer.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
    CreateShortCut "$QUICKLAUNCH\Termer.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
SectionEnd

UninstallText "Программа Termer будет удалена с вашего компьютера. Нажмите Uninstall, чтобы продолжить." "Удаляем программу из:"

Section "Uninstall"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Termer"
    DeleteRegKey HKLM SOFTWARE\NSIS_Termer

    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\Termer"
    Delete "$DESKTOP\Termer.lnk"
    Delete "$QUICKLAUNCH\Termer.lnk"
SectionEnd
