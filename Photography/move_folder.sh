#!/bin/bash

#Bronmap waar de foto's nu staan
SOURCE_DIR=~/Desktop/GevondenFotos

#Doelmap (iCloud Foto's)
DEST_DIR="/Users/thomasboom/Library/Mobile Documents/com~apple~CloudDocs/Foto's"

# Controleer of bronmap bestaat
cd "$SOURCE_DIR" || { echo "Bronmap niet gevonden: $SOURCE_DIR"; exit 1; }

echo "Foto's verplaatsen naar iCloud-map op jaartalbasis..."
echo

# Zorg dat je eigenaar bent en rechten hebt
chown -R "$(whoami)":staff "$SOURCE_DIR"
chmod -R u+rwx "$SOURCE_DIR"
chmod -R u+rwx "$DEST_DIR"

# Zoek alle bestanden (ook in submappen)
find "$SOURCE_DIR" -type f | while read -r file; do
    # Sla het script zelf over
    [[ "$file" == *"sort_to_icloud.sh"* ]] && continue

    # Bestandsnaam zonder pad
    BASENAME=$(basename "$file")

    # Probeer een jaartal (1900–2099) uit de naam te halen
    YEAR=$(echo "$BASENAME" | grep -Eo '19[0-9]{2}|20[0-9]{2}' | head -n 1)

    # Als geen jaartal gevonden → map "Onbekend"
    [ -z "$YEAR" ] && YEAR="Onbekend"

    # Maak jaartalmap aan in iCloud als die nog niet bestaat
    mkdir -p "$DEST_DIR/$YEAR"
    chmod u+rwx "$DEST_DIR/$YEAR"

    # Als er al een bestand met dezelfde naam bestaat, voeg suffix toe
    TARGET_PATH="$DEST_DIR/$YEAR/$BASENAME"
    if [ -e "$TARGET_PATH" ]; then
        BASENAME_NOEXT="${BASENAME%.*}"
        EXT="${BASENAME##*.}"
        TARGET_PATH="$DEST_DIR/$YEAR/${BASENAME_NOEXT}_copy.$EXT"
    fi

    # Verplaats bestand
    mv "$file" "$TARGET_PATH"

    echo "📦 $BASENAME → $YEAR/"
done

echo
echo "Klaar! Alle foto's zijn verplaatst naar:"
echo "$DEST_DIR"
