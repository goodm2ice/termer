Name "Termer @VERSION@ Debug"
OutFile "..\build\Termer @VERSION@ Debug Setup.exe"
InstallDir "$PROGRAMFILES\Termer\Debug\"
InstallDirRegKey HKLM SOFTWARE\NSIS_TermerDebug "Install_Dir"

Section "Termer @VERSION@ Debug"
    SectionIn RO
    SetOutPath $INSTDIR
    File /r "..\build\termer_debug\"
    WriteRegStr HKLM SOFTWARE\NSIS_TermerDebug "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TermerDebug" "DisplayName" " Termer @VERSION@ Debug (только удаление)"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TermerDebug" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteUninstaller "uninstall.exe"
SectionEnd

Section "Start Menu Shortcuts"
    CreateDirectory "$SMPROGRAMS\Termer"
    CreateDirectory "$SMPROGRAMS\Termer\Debug"

    CreateShortCut "$SMPROGRAMS\Termer\Debug\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    CreateShortCut "$SMPROGRAMS\Termer\Debug\Termer Debug.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
    CreateShortCut "$DESKTOP\Termer Debug.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
SectionEnd

UninstallText "Программа Termer Debug будет удалена с вашего компьютера. Нажмите Uninstall, чтобы продолжить." "Удаляем программу из:"

Section "Uninstall"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TermerDebug"
    DeleteRegKey HKLM SOFTWARE\NSIS_TermerDebug

    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\Termer\Debug"
    Delete "$DESKTOP\Termer Debug.lnk"
SectionEnd
