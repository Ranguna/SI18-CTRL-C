import base64
import hashlib
import hashez
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
	def __init__(self, key):
		self.bs = 32
		self.key = hashlib.sha256(key.encode()).digest()

	def encrypt(self, raw):
		hash = hashez.insipid(raw)
		padded = self._pad(raw +":"+ hash)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(padded))

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		dechash = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
		
		if len(dechash.split(":")) == 2 :
			dec,hash = dechash.split(":")
		else:
			raise Exception("PlainText Missmatch")
			
		if hashez.insipid(dec) == hash:
			return dec
		else:
			raise Exception("PlainText Missmatch")

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]

if __name__ == '__main__':
	teste = "aabbccddeeffgg112233445566778899"
	Cipher = AESCipher(teste)
	enc = Cipher.encrypt("ola")
	print(enc)
	dec = Cipher.decrypt(enc)
	print(dec)
	file = open("fileE.txt","r")
	texto = file.read()
	print(texto)
	encT = Cipher.encrypt(texto)
	print(encT)
	decT = Cipher.decrypt(encT)
	print(decT)
	print(len(texto))
	print( AESCipher("123").decrypt(AESCipher("123").encrypt("asd")) == AESCipher("123").decrypt(AESCipher("123").encrypt("asd") ))