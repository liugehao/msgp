#!/usr/bin/env python
#-*- coding:utf-8 -*-
host ='0.0.0.0'
port = 10006

import socket, traceback, os, time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

while 1:
    try:
        clientsock, clientaddr = s.accept()
        
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exec()
    try:
        configFile = open('./config', 'r')
        projs = configFile.readlines()
        configFile.close()

        if clientaddr[0] != projs[0].replace("\n",""):
            clientsock.sendall('拒绝此IP连接 end')
            continue
        print "got connection from ",clientsock.getpeername()
        while 1:
            data = clientsock.recv(4096)
            if not len(data):
                break
            print data
            if data in [x.replace("\n", "") for x in projs]:
                writebashfile = open('/tmp/gitpull','w')
                writebashfile.write("cd %s\ngit pull" % data)
                writebashfile.close()
                time.sleep(5)
                result = os.popen("bash /tmp/gitpull").read() + 'end'
                clientsock.sendall(result)
            else:
                clientsock.sendall('没有代码库 end')
                    
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exec()
    """
    try:
        clientsock.close()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exec()
    """
