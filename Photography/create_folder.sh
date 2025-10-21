#!/bin/bash

# Pad naar de map waar je foto's staan
SOURCE_DIR=~/Desktop/GevondenFotos

# Ga naar de folder
cd "$SOURCE_DIR" || { echo "Folder niet gevonden"; exit 1; }

# Zorg dat je eigenaar bent en rechten hebt
chown -R "$(whoami)":staff "$SOURCE_DIR"
chmod -R u+rwx "$SOURCE_DIR"

# Loop door alle bestanden in de map
for file in *; do
    [ -f "$file" ] || continue

    # Probeer eerst de EXIF- of metadata-opnamedatum op te halen
    CREATED_DATE=$(mdls -raw -name kMDItemContentCreationDate "$file" 2>/dev/null | cut -d ' ' -f 1)

    # Als er geen metadata is, gebruik de bestands-aanmaakdatum
    if [ -z "$CREATED_DATE" ]; then
        CREATED_DATE=$(stat -f "%SB" -t "%Y-%m-%d" "$file" 2>/dev/null)
    else
        # Formatteer van bijv. 2024-06-13T12:45:32Z naar 2024-06-13
        CREATED_DATE=$(echo "$CREATED_DATE" | cut -d 'T' -f 1)
    fi

    # Vang lege of ongeldige datums af
    [ -z "$CREATED_DATE" ] && CREATED_DATE="Onbekend"

    # Maak een map voor de datum
    mkdir -p "$CREATED_DATE"
    chmod u+rwx "$CREATED_DATE"

    # Hernoem het bestand: YYYY-MM-DD_oudeNaam.ext
    BASENAME=$(basename "$file")
    EXT="${file##*.}"
    NEWNAME="${CREATED_DATE}_${BASENAME}"

    # Verplaats en hernoem
    mv "$file" "$CREATED_DATE/$NEWNAME"
done

echo "Alle foto's zijn gesorteerd en hernoemd op oorspronkelijke aanmaakdatum!"