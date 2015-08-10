#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# third-party-modules-into-nginx
# https://serversforhackers.com/compiling-third-party-modules-into-nginx
# https://www.howtoforge.com/tutorial/nginx-with-ngx_pagespeed-on-debian-8-jessie/

# install tornado
# Manual installation: Download tornado-4.2.1.tar.gz:
# tar xvzf tornado-4.2.1.tar.gz
# cd tornado-4.2.1
# python setup.py build
#  sudo python setup.py install


# notes to self
# http://didipkerabat.com/post/2724838963/nginx-file-upload-and-tornado-framework
# http://kevinworthington.com/nginx-for-mac-os-x-mavericks-in-2-minutes/

# NOTE: nginx-upload-module 2.2.0 is ONLY supported up to nginx versions 1.3.8 (dev) up to release-1.2.6  / 1.2.9 branch is unaffected.

# Nginx Source  http://nginx.org/
# nginx-upload-module  https://github.com/vkholodkov/nginx-upload-module/tree/2.2
# sudo wget https://github.com/vkholodkov/nginx-upload-module/archive/2.2.zip
# unzip 2.2.zip
# git clone -b 2.2 git://github.com/vkholodkov/nginx-upload-module.git nginx-upload-module-2.2m

# PCRE - Perl Compatible Regular Expressions   http://www.pcre.org/

# sudo ./configure --prefix=/usr/local --with-http_ssl_module --with-pcre=../pcre-8.33 --add-module=/home/rolf/Documents/nginx-upload-module-2.2m

# sudo ./configure --prefix=/usr/local --with-http_ssl_module --with-pcre=/home/rolf/Documents/pcre-8.37 --add-module=/home/rolf/Documents/nginx-upload-module-2.2

# make
# make install


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
