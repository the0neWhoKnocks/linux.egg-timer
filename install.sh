#!/bin/bash

# icons
mkdir -p ~/.local/share/icons/hicolor/symbolic/apps
cp ./dist/icons/*.svg ~/.local/share/icons/hicolor/symbolic/apps/

# binary
mkdir -p ~/.local/bin
cp ./dist/binary.sh ~/.local/bin/eggtimer

# app
mkdir -p ~/.local/lib/eggtimer
cp ./dist/{app.css,app.py,complete.wav} ~/.local/lib/eggtimer/
cp ./dist/eggtimer.desktop ~/.local/share/applications/
