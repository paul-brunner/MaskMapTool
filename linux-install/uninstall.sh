#!/bin/bash

echo "Removing MaskMapTool"

rm -rf /usr/bin/MaskMapTool
rm -rf /usr/share/applications/maskmaptool.desktop
rm -rf /usr/pixmaps/mask_icon.png

if [ $? -eq 0 ]; then
	echo "MaskMapTool has been uninstalled successfully"
else
	echo "MaskMapTool has not been uninstalled due to an error"
fi
