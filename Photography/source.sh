#!/bin/bash

# Bronmap op externe schijf
SOURCE="/Volumes/iSSD/WdKA/deFine Arts/"

# Doelmap op je bureaublad
DEST=~/Desktop/GevondenFotos
mkdir -p "$DEST"

echo "Zoeken naar afbeeldingen in: $SOURCE"

# Zoeken en kopiëren
find "$SOURCE" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.tif" -o -iname "*.tiff" \) -exec cp "{}" "$DEST" \; 2>/dev/null

# Volledige rechten aan jezelf geven
chmod -R u+rwx "$DEST"
chown -R "$(whoami)" "$DEST" 2>/dev/null

echo "Klaar! Afbeeldingen zijn gekopieerd naar: $DEST"
echo "Je hebt nu volledige rechten op de bestanden."