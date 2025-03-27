!define APP_NAME "AutomacaoWhatsApp"
!define APP_VERSION "1.0.0"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

SetCompressor lzma

Name "${APP_NAME} ${APP_VERSION}"
OutFile "AutomacaoWhatsApp-Installer.exe"
InstallDir ${INSTALL_DIR}

Page directory
Page instfiles

Section "Instalar"
    ; Cria o diretório de instalação
    SetOutPath $INSTDIR

    ; Copia o executável gerado pelo PyInstaller
    File /r "dist/automacao-whatsapp/*"

    ; Copia o Python Embedded
    File /r "python-embedded\*"

    ; Copia outros arquivos necessários
    File /r "data\*"
    File "version.txt"

    ; Cria um atalho no desktop
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\automacao-whatsapp.exe"

    ; Cria um atalho no menu iniciar
    CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\automacao-whatsapp.exe"
SectionEnd

Section "Desinstalar"
    ; Remove os arquivos instalados
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"

    ; Remove os atalhos
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}.lnk"
SectionEnd