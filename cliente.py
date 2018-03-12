import socket as skt
import sys

if len(sys.argv) == 4:
	host = sys.argv[1]
	port = int(sys.argv[2])
	auth = sys.argv[3]
	up = auth.split(':')
	user = up[0]
	passw = up[1]
else:
	print 'Need to specify  <host> <port> <user:pass>'
	sys.exit()


s = skt.socket(skt.AF_INET,skt.SOCK_STREAM)

s.connect((host,port))
cmd =  '' 
s.settimeout(5) 
while 1 :
	cmd = raw_input('<> ') 
	s.send(cmd) 
	try:
		buf = s.recv(2048)
		print buf
		if 'BYE!' in buf:
			s.close()
			sys.exit()
	except skt.timeout:
		print 'No response after sending ' + '"' +  cmd + '"'
