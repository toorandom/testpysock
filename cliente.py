import socket as skt
import sys
import hashlib as hl
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
	auth = sys.argv[3]
	up = auth.split(':')
	user = up[0]
	passwd = up[1]
else:
	print 'Need to specify  <host> <port> <user:pass> '
	sys.exit()


s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

s.connect((host,port))
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
				cbuf = s.recv(100)
				if  len(cbuf) == 100: 
					tbuf = tbuf + cbuf
				else:
					tbuf = tbuf + cbuf
					break;
			
				buf = decrypt(user + passwd, tbuf) 
				print buf
				if 'BYE!' in buf:
					s.close()
					sys.exit()
		except skt.timeout:
			print 'No response after sending ' + '"' +  cmd + '"'
