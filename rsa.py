from subprocess import Popen, PIPE, call
import base64
import re
from os import path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

s_gen_keypair_pass = 'openssl genrsa -aes256 -passout pass:%s -out %s %d'
s_gen_keypair = 'openssl genrsa -aes256 -out %s %d'

s_load_keypair_pass = 'openssl rsa -in %s -passin pass:%s'
s_load_keypair = 'openssl rsa -in %s'

def gen_keypair(file_name, passwd = None, bits = 2048):
	# verify arguments for injections
	if re.match(r"^[\w\.\/]*$", file_name) == None:
			raise Exception("Invalid file name.")

	p = None
	if passwd != None:
		# call((s_gen_keypair_pass%(passwd, file_name, bits)).split(" "))
		p = Popen((s_gen_keypair_pass%(passwd.encode("hex"), file_name, bits)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	else: 
		p = Popen((s_gen_keypair%(file_name, bits)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	_ = p.stdout.read()
	return path.isfile(file_name)

def load_keypair(file_name, passwd):
	if re.match(r"^[\w\.\/]*$", file_name) == None:
			raise Exception("Invalid file name.")

	if not path.isfile(file_name):
		raise Exception("File %s not found."%file_name)

	p = None
	if passwd != None:
		p = Popen((s_load_keypair_pass%(file_name, passwd.encode("hex"))).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	else: 
		p = Popen((s_gen_keypair%(file_name)).split(" "), stdout=PIPE, stderr=PIPE, stdin=PIPE)
	
	output = p.stdout.read()

	if output == '':
		raise Exception("Wrong password or invalid key.")

	return serialization.load_pem_private_key(output, password=None, backend= default_backend())

def load_enckeypair(file_name, passwd):
	try:
		keypair = load_keypair(file_name, passwd)

		return (
			keypair.public_key(),
			keypair.private_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PrivateFormat.PKCS8,
				encryption_algorithm=serialization.BestAvailableEncryption(passwd)
			)
		)
	except Exception as err:
		raise Exception("Error while loading keypair: "+err.message)

def dec_privkey(privkey, passwd):
	return serialization.load_pem_private_key(privkey, password=passwd, backend=default_backend())

class KeyPair:
	def __init__(self, keyfile = None, passwd = None, generate = False):
		self.publicKey = None
		self.encPrivateKey = None
		if keyfile != None and passwd != None and not generate:
			self.load_file(keyfile, passwd)
		elif keyfile != None and passwd != None and generate:
			self.generate(keyfile, passwd)
		else:
			raise Exception("Invalid arguments for keypair")
			
	def generate(self, keyfile, passwd):
		gen_keypair(keyfile, passwd)
		self.load_file(keyfile, passwd)

	def load_file(self, keyfile, passwd):
		(self.publicKey, self.encPrivateKey) = load_enckeypair(keyfile, passwd)
		
	def max_len(self):
		return self.publicKey.key_size/8 - 2*32 -2
		# return int(floor((floor((ceil(self.publicKey.size()/8/3)/4)*4)*3 - 65)/4)*3)

	def encrypt(self, data):
		if not self.publicKey:
			raise Exception("Empty keypair.")

		return base64.b64encode(
			self.publicKey.encrypt(
				data,
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm=hashes.SHA256(),
					label=None
				)
			)
		)

	def decrypt(self, data, passwd):
		if not self.encPrivateKey:
			raise Exception("Empty keypair")

		return dec_privkey(self.encPrivateKey, passwd).decrypt(
			base64.b64decode(data),
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)

if __name__ == "__main__":
	keypair2 = KeyPair(".temp.pem", "124", True)
	keypair = KeyPair(".temp.pem", "123", True)
	print keypair.max_len
	print keypair.decrypt(keypair.encrypt("1"*keypair.max_len()),"123")
	try:
		print "first"
		print keypair.decrypt(keypair.encrypt("test"),"123")
	except Exception as e:
		print "Error on first command %s"%e.message
	try:
		print "second"
		print keypair2.decrypt(keypair.encrypt("test"),"1234")
	except Exception as e:
		print e
	try:
		print "third"
		print keypair.decrypt(keypair.encrypt("test"),"1234")
	except Exception as e:
		print e
	try:
		print "fourth"
		print keypair.decrypt(keypair.encrypt("1"*(keypair.max_len()+1)),"123")
	except Exception as e:
		print e
