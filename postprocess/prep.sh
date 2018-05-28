git clone https://github.com/nreimers/truecaser.git
cd ./truecaser
wget https://github.com/nreimers/truecaser/releases/download/v1.0/english_distributions.obj.zip
unzip ./english_distributions.obj.zip
rm ./english_distributions.obj.zip
cd ../
echo "[Note] If using python 3, Add 'from six.moves import xrange' to ./truecaser/Truecaser.py"
