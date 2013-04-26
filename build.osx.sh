#!/bin/bash
#sudo port install mplayer
lipo -thin i386 -output ~/python-i386 /usr/bin/python2.7
~/python-i386 ~/pyinstaller-2.0/pyinstaller.py --windowed --onefile pyinstaller.osx.spec
hdiutil create ./install/LinguaCinema.dmg -srcfolder ./dist/LinguaCinema.app -ov