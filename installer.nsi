!define APP_NAME "AutomacaoWhatsApp"
!define APP_VERSION "1.0"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

SetCompressor lzma

Name "${APP_NAME} ${APP_VERSION}"
OutFile "installer.exe"
InstallDir ${INSTALL_DIR}

Page directory
Page instfiles

Section ""
    SetOutPath $INSTDIR
    File /r "dist\automacao-whatsapp\*"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\automacao-whatsapp.exe"
SectionEnd