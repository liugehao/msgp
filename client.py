#!/usr/bin/env python
#-*- coding:utf-8 -*-

host = 'localhost'
port = 10006

import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

data = "x" * 104857


def senddata(data):
    byteswritten = 0 
    while byteswritten < len(data):
        startpos = byteswritten
        endpos = min(byteswritten + 1024, len(data))
        print byteswritten,startpos,endpos
        byteswritten += s.send(data[startpos:endpos])
        sys.stdout.write("Wrote %d bytes \r" % byteswritten)
        sys.stdout.flush()
        print "Wrote %d bytes \r" % byteswritten
    #s.shutdown(1)
    
    print "all data sent."
    while 1:
        buf = s.recv(1024)
        if not len(buf):
            break
        sys.stdout.write(buf)
        sys.stdout.flush()
        if buf.endswith('end'):
            break

while 1:
    data = raw_input("cmd:")
    senddata(data)
