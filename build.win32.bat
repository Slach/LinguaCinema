#need cygwin for correctly work
call pyinstaller.bat LinguaCinema.win32.spec
cd dist/LinguaCinema
pwd
rm -rf LinguaCinemaInstall*
7z a -mx9 -r LinguaCinemaInstall.7z
rm -rfv ../../install/*
mv -fv LinguaCinemaInstall.7z ../../install/
cd ../../install/
cp -rvf ../7z/* ./
cat 7z.sfx 7z.conf LinguaCinemaInstall.7z >> LinguaCinemaInstall.exe
rm -rfv 7z.sfx 7z.conf LinguaCinemaInstall.7z
