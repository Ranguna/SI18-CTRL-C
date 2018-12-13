from subprocess import Popen, PIPE, call
from Crypto.PublicKey import RSA
import aes
import hashez
import base64
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
	# print _
	# print path.isfile(file_name)
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
	try:
		keypair = load_keypair(file_name, passwd)

		return (keypair.publickey(), aes.AESCipher(passwd).encrypt(keypair.exportKey()))
	except Exception as err:
		raise Exception("Error while loading keypair: "+err.message)

def dec_privkey(privkey, passwd):
	return RSA.importKey(aes.AESCipher(passwd).decrypt(privkey))

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
		gen_keypair(keyfile, passwd) #!sht: pode falhar caso nao consiga gravar o ficheiro
		self.load_file(keyfile, passwd)

	def load_file(self, keyfile, passwd):
		(self.publicKey, self.encPrivateKey) = load_enckeypair(keyfile, passwd)

	def encrypt(self, data):
		if not self.publicKey:
			raise Exception("Empty keypair.")

		data = data + ":" + hashez.insipid(data).encode("hex")
		print(self.publicKey.size(), len(data	))
		return base64.b64encode(self.publicKey.encrypt(data, 0)[0])

	def decrypt(self, data, passwd):
		if not self.encPrivateKey:
			raise Exception("Empty keypair")

		# from hex
		data = base64.b64decode(data)
		
		try:
			data = dec_privkey(self.encPrivateKey, passwd).decrypt(data)
		except Exception as e:
			raise Exception("Key missmatch.")

		data = data.split(":")
		if len(data) != 2:
			raise Exception("Plaintext missmatch.")

		if hashez.insipid(data[0]).encode("hex") != data[1]:
			raise Exception("Plaintext missmatch.")

		return data[0]

if __name__ == "__main__":
	keypair2 = KeyPair(".temp.pem", "124", True)
	keypair = KeyPair(".temp.pem", "123", True)
	print keypair.publicKey.size()/8
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
