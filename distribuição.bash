
# Script para distribuir o aplicativo

#!/bin/bash

# Nome do seu aplicativo
APP_NAME="latest_release"
UPDATER_VERSION=$(cat updaterversion.txt)  # Atualiza isso a cada release!
VERSION=$(cat version.txt)  # Atualiza isso a cada release!
echo "Version: $VERSION"
echo "Updater Version: $UPDATER_VERSION"
echo "App Name: $APP_NAME"

# Limpa builds anteriores
rm -rf dist/ build/ release/ test/

# Gera o executável com PyInstaller
pyinstaller AutomacaoWhatsapp.spec 
(cd dist && zip -r "${APP_NAME}.zip" "AutomacaoWhatsapp")

# Gera o executável com PyInstaller
pyinstaller Updater.spec

(cd dist && zip -r "${APP_NAME}_Updater.zip" "Updater")
mv "dist/Updater" "dist/AutomacaoWhatsapp"

# Remove os arquivos temporários criados pelo PyInstaller
rm -rf build/

# Move o zip para uma pasta de releases (opcional)
# mkdir -p releases
# mv "${APP_NAME}_${VERSION}.zip" releases/