#!/usr/bin/env python
#coding=utf-8

import tornado.auth
import tornado.httpserver 
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import tornado.locale
import tornado.wsgi
from tornado import gen

import os
import re


import sys, socket
reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime, logging
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                    (r"/", IndexHandler)
                    ]
        settings = dict(
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.logger = logging.getLogger()
        hdlr = logging.FileHandler('./tor.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.NOTSET)
        #print 'rpc'
        #self.rpc = ServerProxy("http://localhost:8080")    
        #self.db = None


    

class IndexHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        try:
            f = open('./tor.config', 'r')
            
            gitpullservers = eval(f.read())
            f.close()
        except:
            self.write(u"读取 tor.config 出错！")
        self.write("""<form id=form1 method=post><input type=hidden id=host name=host><input type=hidden id=path name=path></form><script>function post(host,path){
        if(!confirm('确定要pull '+host +' '+path+'?')){return;};document.getElementById('path').value=path;document.getElementById('host').value=host;document.getElementById('form1').submit();}</script>""")
        for host, paths in gitpullservers:
            self.write("%s <br>" % host)
            for path in paths:
                self.write("""<a href='javascript:post("%s","%s")' >%s </a>&nbsp;&nbsp;""" % (host, path, path))
            self.write("""<hr>""")

    def post(self):
        logger = self.application.logger
        host = self.get_argument('host','192.168.14.53')
        port = 10006
        data = self.get_argument('path','/home/l/autogit')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        byteswritten = 0 
        while byteswritten < len(data):
            startpos = byteswritten
            endpos = min(byteswritten + 1024, len(data))
            byteswritten += s.send(data[startpos:endpos])
            self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ："))
            self.write("向服务器 %s 目录 %s 发送pull命令 <br>" % (host, data ))
            logger.info("向服务器 %s 目录 %s 发送pull命令" % (host, data ))
            self.flush()
            
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ：更新命令已发出。<br>"))
        self.flush()
        
        result = False
        while 1:
            if not result:
                self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ：服务器返回信息：<br>"))
                logger.info("%s 服务器 %s 返回信息：" % (host, data))
                result = True
            buf = s.recv(1024)
            if not len(buf):
                break
            self.write(buf.replace("\n","<br>"))
            logger.info(buf)
            if buf.endswith('end'):
                break


if __name__ == "__main__":
    #tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    loop = tornado.ioloop.IOLoop.instance()
    #tornado.autoreload.start(loop)
    loop.start()


