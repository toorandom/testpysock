import hashlib as hl
import sys

if len(sys.argv) < 4:
	print 'Need to specify <usr> <pass> <filename>'
	sys.exit() 

user = sys.argv[1]
passwd = sys.argv[2]
filename = sys.argv[3]

fl = open(filename ,'a')

if not fl:
	print 'Filename ' + filename + 'does not exist'


phash = hl.sha256(passwd).hexdigest() 

ln = user + ':' + phash + '\n'

fl.write(ln)

fl.close() 


