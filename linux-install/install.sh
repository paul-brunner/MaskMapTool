#!/bin/bash

echo "Installing.."

cp -r MaskMapTool /usr/bin/
chmod +x /usr/bin/MaskMapTool
cp -r maskmaptool.desktop /usr/share/applications/
cp -r mask_icon.png /usr/share/pixmaps/

if [ $? -eq 0 ]; then
	echo "MaskMapTool has been installed successfully"
else
	echo "The installation was not successful"
fi
