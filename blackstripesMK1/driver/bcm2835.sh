#
#
#//install bcm2835 V1.45
#// The library homepage  http://www.airspayce.com/mikem/bcm2835/
#//scp bcm2835.sh pi@10.0.1.18:/home/pi/GPIO_C_driver
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.44.tar.gz
tar zxvf bcm2835-1.45.tar.gz
cd bcm2835-1.45
./configure
sudo make check
sudo make install
