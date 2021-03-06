#!/usr/bin/env python
#
#
# third-party-modules-into-nginx
# https://serversforhackers.com/compiling-third-party-modules-into-nginx
# https://www.howtoforge.com/tutorial/nginx-with-ngx_pagespeed-on-debian-8-jessie/
#
# install tornado
# Manual installation: Download tornado-4.2.1.tar.gz:
# tar xvzf tornado-4.2.1.tar.gz
# cd tornado-4.2.1
# python setup.py build
#  sudo python setup.py install
#
#  Tornado on raspberry :   http://buonageek.blogspot.ch/2013/07/raspberry-pi-python-tornado-nginx.html  
#  sudo apt-get update
#  sudo apt-get upgrade
#
#  2.  Install easy_install and pip (which are Python package managers)
#
#  sudo apt-get install python-pip python2.7-dev
#
#  3.  Update your easy_install (and pip) package definitions
#
#  sudo easy_install -U distribute
#
#  4.  Now install Tornado using pip
#
#  sudo pip install tornado
#
# notes to self
# http://didipkerabat.com/post/2724838963/nginx-file-upload-and-tornado-framework
# http://kevinworthington.com/nginx-for-mac-os-x-mavericks-in-2-minutes/
#
# Installing the SciPy Stack :  sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
#
#
#
# packages list and install:   apt-get install dpkg-dev build-essential zlib1g-dev libpcre3 libpcre3-dev unzip curl libcurl4-openssl-dev libossp-uuid-dev
#  How do I install the OpenSSL C++      sudo apt-get install libssl-dev      sudo apt-get install openssl
#
# NOTE: nginx-upload-module 2.2.0 is ONLY supported up to nginx versions 1.3.8 (dev) up to release-1.2.6  / 1.2.9 branch is unaffected.
#
# Nginx Source  http://nginx.org/
# Nginx version 1.2.9 download under    http://nginx.org/download/nginx-1.2.9.tar.gz
#
#
# nginx-upload-module  https://github.com/vkholodkov/nginx-upload-module/tree/2.2
# sudo wget https://github.com/vkholodkov/nginx-upload-module/archive/2.2.zip
# unzip 2.2.zip
# git clone -b 2.2 git://github.com/vkholodkov/nginx-upload-module.git nginx-upload-module-2.2m
#
# PCRE - Perl Compatible Regular Expressions   http://www.pcre.org/
# download under     http://sourceforge.net/projects/pcre/files/pcre/8.37/pcre-8.37.tar.gz
#
# sudo ./configure --prefix=/usr/local --with-http_ssl_module --with-pcre=../pcre-8.33 --add-module=/home/rolf/Documents/nginx-upload-module-2.2m
#
# sudo ./configure --prefix=/usr/local --with-http_ssl_module --with-pcre=/home/rolf/Documents/pcre-8.37 --add-module=/home/rolf/Documents/nginx-upload-module-2.2
#
# sudo make
# sudo make install
#
#
# sudo /usr/local/sbin/nginx -c /home/rolf/Documents/blackstripes/blackstripesMK2/webbased_preview/nginx.conf




import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import Image
import webbased_preview

import hashlib

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Blackstripes preview server.")

class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        imagename = self.get_argument('image.name', default=None)
        path = self.get_argument('image.path', default=None)

        m = hashlib.md5()
        m.update(path+"fullscreen zacht spul is beter")
        md5str = m.hexdigest()

        pr = webbased_preview.Cropper(path,md5str,self.version)
        self.write(pr.getJSON())

class UploadHandler_v1(UploadHandler):
    version = "v1"

class UploadHandler_v2(UploadHandler):
    version = "v2"

class ColorHandler(tornado.web.RequestHandler):

    def get(self,version,image_id):
        pr = webbased_preview.ColorOptions(image_id,version)
        self.write(pr.getJSON())

class PreviewHandler(tornado.web.RequestHandler):

    def get(self,version,image_id):
        pr = webbased_preview.Preview(image_id,version)
        self.write(pr.getJSON())

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/v1/images/upload", UploadHandler_v1),
        (r"/v2/images/upload", UploadHandler_v2),
        (r"/?(?P<version>[^\/]+)?/color/?(?P<image_id>[^\/]+)?", ColorHandler),
        (r"/?(?P<version>[^\/]+)?/preview/?(?P<image_id>[^\/]+)?", PreviewHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
