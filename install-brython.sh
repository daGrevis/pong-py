wget https://github.com/brython-dev/brython/releases/download/3.1.0/Brython3.1.0-20150301-090019.tar.gz -O- | tar -xz
rm -rf {brython.js,Lib,libs}
mv Brython3.1.0-20150301-090019/{brython.js,Lib,libs} .
rm -r Brython3.1.0-20150301-090019
