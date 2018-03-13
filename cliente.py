import socket as skt
import sys
import hashlib as hl
import getpass
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(key,data):
	k = hl.sha512(key).digest()[0:16]
	iv = Random.new().read(AES.block_size) 
	cipher = AES.new(k,AES.MODE_CFB,iv) 
	edat = cipher.encrypt(data)
	cdata = iv + edat
	return cdata 

def decrypt(key,cdata): 
	k = hl.sha512(key).digest()[0:16]
	iv = cdata[0:16]
	ndata = cdata[16:] 
	decipher= AES.new(k,AES.MODE_CFB,iv) 
	data = decipher.decrypt(ndata) 
	return data



if len(sys.argv) == 4:
	host = sys.argv[1]
	port = int(sys.argv[2])
	user = sys.argv[3]
else:
	print 'Need to specify  <host> <port> <username> '
	sys.exit()


passwd = getpass.getpass() 

helo = 'HELOPROTOCOL'
lh = len(helo)
chelo = encrypt(user + passwd, helo.ljust(lh+16-(lh%16))) 

s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

s.connect((host,port))

s.send(chelo) 
auth = s.recv(32)
if auth[0:2] == 'WE': 
	print 'Correct Authentication!' 
else:
	print 'Error in Authentication!'
	s.close() 
	sys.exit() 

cmd =  '' 
cbuf = ' ' 
tbuf = ''
s.settimeout(5) 
while 1 :
	cmd = raw_input('<> ') 
	l = len(cmd) 
	if l > 1:
		ecmd = encrypt(user + passwd, cmd.ljust(l+16-(l%16))) 
		s.send(ecmd) 
		try:
			while 1:
				cbuf = s.recv(1024)
				tbuf = tbuf + cbuf
				if  len(cbuf) != 1024: 
					break;
			buf = decrypt(user + passwd, tbuf) 
			tbuf = ''
			print buf
			if 'BYE!' in buf:
				s.close()
				sys.exit()
		except skt.timeout:
			print 'No response after sending ' + '"' +  cmd + '"'
