#//install bcm2835 V1.44
#// The library homepage  http://www.airspayce.com/mikem/bcm2835/
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.44.tar.gz
tar zxvf bcm2835-1.44.tar.gz
cd bcm2835-1.44
./configure
sudo make check
sudo make install
