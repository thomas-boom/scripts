#!/bin/bash

# Bronmap op externe schijf
SOURCE="edit this to folder that needs to be seperated"

# Doelmap op je bureaublad
DEST=~/Desktop/FoundPictures
mkdir -p "$DEST"

echo "Looking for images in: $SOURCE"

# Zoeken en kopiëren
find "$SOURCE" -type f \( -iname "*.RAF" -o -iname "*.ARW" \) -exec cp "{}" "$DEST" \; 2>/dev/null

# Volledige rechten aan jezelf geven
chmod -R u+rwx "$DEST"
chown -R "$(whoami)" "$DEST" 2>/dev/null

echo "All images are copied to folder: $DEST"
echo "Rights have been given to files."
