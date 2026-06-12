#!/bin/bash

# icons
mkdir -p ~/{.icons,.local/share/icons/hicolor/symbolic/apps}
cp $(grep -L "symbolic" ./dist/icons/*.svg) ~/.icons/
cp ./dist/icons/*symbolic.svg ~/.local/share/icons/hicolor/symbolic/apps/

# binary
mkdir -p ~/.local/bin
cp ./dist/binary.sh ~/.local/bin/eggtimer
chmod +x ~/.local/bin/eggtimer

# app
mkdir -p ~/.local/lib/eggtimer
cp ./dist/{app.css,app.py,complete.wav} ~/.local/lib/eggtimer/
cp ./dist/eggtimer.desktop ~/.local/share/applications/

# account for "Checksum-based launcher trusts - new functionality added in Thunar 4.17.4"
launcher=~/.local/share/applications/eggtimer.desktop
chmod +x $launcher
if hash gio 2>/dev/null; then
  gio set -t string "$launcher" metadata::xfce-exe-checksum "$(sha256sum "$launcher" | awk '{print $1}')"
fi
