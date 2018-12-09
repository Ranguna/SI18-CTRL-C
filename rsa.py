from subprocess import Popen, PIPE, call
from Crypto.PublicKey import RSA
import aes
from os import path

s_gen_keypair_pass = 'openssl genrsa -aes256 -passout pass:%s -out %s %d'
s_gen_keypair = 'openssl genrsa -aes256 -out %s %d'

s_load_keypair_pass = 'openssl rsa -in %s -passin pass:%s'
s_load_keypair = 'openssl rsa -in %s'

def gen_keypair(file_name, passwd = None, bits = 2048):
	p = None
	if passwd != None:
		# call((s_gen_keypair_pass%(passwd, file_name, bits)).split(" "))
		p = Popen((s_gen_keypair_pass%(passwd, file_name, bits)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	else: 
		p = Popen((s_gen_keypair%(file_name, bits)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	_ = p.stdout.read()
	print _
	print path.isfile(file_name)
	return path.isfile(file_name)

def load_keypair(file_name, passwd):
	if not path.isfile(file_name):
		raise Exception("File %s not found."%file_name)

	p = None
	if passwd != None:
		p = Popen((s_load_keypair_pass%(file_name, passwd)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	else: 
		p = Popen((s_gen_keypair%(file_name)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p.stdout.read()
	if output == '':
		raise Exception("Wrong password or invalid key.")

	return RSA.importKey(output)

def load_enckeypair(file_name, passwd):
	keypair = load_keypair(file_name, passwd)

	return (keypair.publickey(), aes.AESCipher(passwd).encrypt(keypair.exportKey()))

def dec_privkey(privkey, passwd):
	return RSA.importKey(aes.AESCipher(passwd).decrypt(privkey))

