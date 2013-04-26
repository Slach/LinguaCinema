## What is LinguaCinema

LinguaCinema it's cross-platform media file player for Windows, Linux,
MacOSX 10.7+ which have some specific features needed for language learning:

- download subtitles from http://OpenSubtitles.org in .srt format
- translate selected word when you left mouse click
- translate selection from subtitle text  when you right mouse click
- adding selected words (or phrases) to your personal Lingualeo.com dictionary

LinguaCinema powered by mplayer (mplayer2), wxPython, pysrt and 220V ;)

## Download Binaries from Google Code
- http://code.google.com/p/linguacinema/downloads/list

## Manual run on Debian\Ubuntu

    sudo aptitude install mplayer2
    git clone https://github.com/Slach/LinguaCinema.git
    cd LinguaCinema
    pip install -r pip-requirements.txt
    python LinguaCinema.py

## Manual run Windows

download and install python from http://python.org
run easy_install.exe pip

    git clone https://github.com/Slach/LinguaCinema.git
    cd LinguaCinema
    pip install -r pip-requirements.txt
    python LinguaCinema.py


## Manual run MacOSX

install Mac Ports or Homebrew

    sudo port install mplayer (maybe brew install mplayer)
    git clone https://github.com/Slach/LinguaCinema.git
    cd LinguaCinema
    pip install -r pip-requirements.txt
    python LinguaCinema.py
