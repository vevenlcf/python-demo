# -*- coding: utf-8 -*-
'''
# @Date    : 2018-9-14
# @Author  : vevenlcf
# @Link    : https://github.com/vevenlcf
# @Version : 1.0
'''
import time

from SocketServer import ThreadingTCPServer,TCPServer,StreamRequestHandler,UDPServer,ForkingTCPServer
# 定义请求处理类
class Handler(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        print 'Got connection from ',addr
        self.wfile.write('Thank you for connecting')
        time.sleep(60)

server = ThreadingTCPServer(('',1297), Handler)   # 实例化服务类对象(多线程、单线程、多进程)
server.serve_forever()  # 开启服务

