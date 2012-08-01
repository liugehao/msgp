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
import json
import re
from random import random
import datetime
from math import floor
#import xml.etree.ElementTree as xml
from docutils.core import publish_string
import mako
from mako.template import Template
from mako.lookup import TemplateLookup
mako.runtime.UNDEFINED = ''
from mako.exceptions import TemplateLookupException

import sys, socket
reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [

                    (r"/", IndexHandler),

                    ]
        settings = dict(
            blog_title=u"Mine ",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/user/login",
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        #print 'rpc'
        #self.rpc = ServerProxy("http://localhost:8080")    
        #self.db = None
        # Have one global connection to the blog DB across all handlers


        

        

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.re = re.compile('^\d{4}-\d{1,2}-\d{1,2}$')
        
        
    lookup = TemplateLookup(["./templates"], input_encoding='utf-8', output_encoding = "utf-8")

    def render(self, template_name, **kwargs):
        """ Redefine the render """
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.application.reverse_url,
            LANGUAGES=settings.LANGUAGES,
            STATIC_URL=settings.STATIC_URL,
            THEME_URL=settings.THEME_URL
        )
        t = self.lookup.get_template(template_name)

        
        args.update(kwargs)

        html = t.render(**args)
        self.finish(html)
    
    

        
    """
    @property
    def db(self):
        if not hasattr(self.application, 'db'):
            self.application.db = momoko.AsyncClient({
                'host': settings.host,
                'port': settings.port,
                'database': settings.database,
                'user': settings.user,
                'password': settings.password,
                'min_conn': settings.min_conn,
                'max_conn': settings.max_conn,
                'cleanup_timeout': settings.cleanup_timeout
            })
        return self.application.db
    """

    #@property
    def get_current_user(self):
        if self.get_secure_cookie("uid"):
            return self.get_secure_cookie("uid")
        return None


    


class IndexHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        host = self.get_argument('host','192.168.14.53')
        port = 10006
        data = self.get_argument('path','/home/l/autogit')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.write("host:%s" % host)
        self.write("path:%s" % data)
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
        byteswritten = 0 
        while byteswritten < len(data):
            startpos = byteswritten
            endpos = min(byteswritten + 1024, len(data))
            print byteswritten,startpos,endpos
            byteswritten += s.send(data[startpos:endpos])
            self.write("Wrote %d bytes \r" % byteswritten)
            self.flush()
        s.shutdown(1)
        time.sleep(3)
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
        self.write( "all data sent.\r")
        self.flush()
        while 1:
            buf = s.recv(1024)
            if not len(buf):
                break
            self.write(buf)
            if buf.endswith('end'):
                break
        self.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))        
    def post(self):
        pass

if __name__ == "__main__":
    #tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "translations"))
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    loop = tornado.ioloop.IOLoop.instance()
    #tornado.autoreload.start(loop)
    loop.start()


