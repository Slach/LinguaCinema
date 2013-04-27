#need cygwin for correctly work
call pyinstaller.bat --windowed pyinstaller.win32.spec
cd dist/LinguaCinema.win32
pwd
rm -rfv LinguaCinemaInstall*
chmod 0755 bin/win32/mplayer2.exe
7z a -mx9 -r LinguaCinemaInstall.7z
rm -rfv ../../install/*
mv -fv LinguaCinemaInstall.7z ../../install/
cd ../../install/
cp -rvf ../7z/* ./
cat 7z.sfx 7z.conf LinguaCinemaInstall.7z >> LinguaCinemaInstall.exe
rm -rfv 7z.sfx 7z.conf LinguaCinemaInstall.7z
