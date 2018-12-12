import os
import hashlib

def salted(text, salt=10, rounds = 10000):
	if type(salt) == int:
		salt = os.urandom(salt).encode("hex")
	
	return hashlib.pbkdf2_hmac("sha256", text.encode("hex"), salt, rounds).encode("hex")+":"+salt

def insipid(text):
<<<<<<< HEAD
	return hashlib.sha256(text).digest().encode("hex")
=======
	return hashlib.sha256(text).digest()
>>>>>>> 5681c573c984b80b2dc1b5b4465777271e3ebf19

def verify(original_text, hash, rounds = 10000):
	[_, salt] = hash.split(":")[0:3]
	
	return salted(original_text, salt, rounds) == hash

if __name__ == "__main__":
	# verification of wrong plaintext
	print verify("test123", salted("test12"))
	# simple hashing and verifying
	print verify("test12", salted("test12"))
	# hasing and verifying with custom salt
	print verify("test12", salted("test12","asd"))
	# same with custom rounds
	print verify("test12", salted("test12","asd", 10),10)
	# default salt and custom rounds
	print verify("test12", salted("test12", rounds = 10),10)