#!/bin/bash

# Nome do seu aplicativo
APP_NAME="Automacao Whatsapp"
VERSION="1.0.0"  # Atualize isso a cada release!

# Limpa builds anteriores
rm -rf dist/ build/

# Gera o executável com PyInstaller
pyinstaller AutomacaoWhatsapp.spec 

# Compacta a pasta dist
zip -r "${APP_NAME}_${VERSION}.zip" dist/

# Move o zip para uma pasta de releases (opcional)
mkdir -p releases
mv "${APP_NAME}_${VERSION}.zip" releases/