import socket as skt
import getpass
import os
import sys
import time
import hashlib as hl
from Crypto.Cipher import AES
from Crypto import Random


def encrypt(key,data):
        k = hl.sha512(key).digest()[0:16]
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(k,AES.MODE_CFB,iv)
        cdata = iv + cipher.encrypt(data)
        return cdata

def decrypt(key,cdata):
        k = hl.sha512(key).digest()[0:16]
        iv = cdata[0:16]
        ndata = cdata[16:]
        decipher= AES.new(k,AES.MODE_CFB,iv)
        data = decipher.decrypt(ndata)
	return data


if len(sys.argv) == 3:
        port = int(sys.argv[1])
#        auth = sys.argv[2]
#        up = auth.split(':')
        user = sys.argv[2]
#        passwd = up[1]
else:
        print 'Need to specify   <listenport> <user> '
        sys.exit()

passwd = getpass.getpass()
s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
s.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
s.bind(('0.0.0.0',port)) 
s.listen(10)
conn,addr = s.accept()

helo = 'HELOPROTOCOL'
lh = len(helo)
cauth = conn.recv(128) 
auth = decrypt(user + passwd, cauth) 

if auth[0:lh] != helo:
	print 'Invalid username from', addr
	conn.send('BYE!')
	conn.close()
	s.close() 
	sys.exit() 

print 'Correct auth from: ' , addr
conn.send('WELCOME!') 



while 1: 
	cdata = conn.recv(1024) 
	print len(cdata) 
	data = decrypt(user + passwd, cdata)
	print 'DATA: '+data
	if 'quit' in data:
		conn.send('BYE!')
		conn.close() 
		s.close() 
		sys.exit()
	pr = os.popen(data)
	ln = pr.readlines()
	buf = ''.join(ln)
	hbuf = hl.sha256(buf).hexdigest() 
	msg = 'OutputHash is: ' + hbuf + '\n'
	moment = time.ctime() + '\n\n'
	tmsg = msg + moment + buf
	tl = len(tmsg)
	ctbuf = encrypt(user + passwd, tmsg.ljust(tl + 16-(tl%16))) 
	conn.send(ctbuf) 
	pr.close()
	
