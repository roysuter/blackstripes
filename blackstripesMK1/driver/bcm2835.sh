//install bcm2835 V1.88
// The library homepage  http://www.airspayce.com/mikem/bcm2835/
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.88.tar.gz
tar zxvf bcm2835-1.88.tar.gz
cd bcm2835-1.88
./configure
sudo make check
sudo make install
