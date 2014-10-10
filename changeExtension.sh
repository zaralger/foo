#!/bin/bash

EXTENSION_SOURCE="cbr"
EXTENSION_DEST="zip"
FOLDER="$1"

echo $FOLDER"coucou."$EXTENSION_SOURCE

for file in "$FOLDER"*".$EXTENSION_SOURCE"
do
	echo $file
	mv $file `echo $file | sed "s%\(.*\.\)$EXTENSION_SOURCE%\1$EXTENSION_DEST%"` 
done



