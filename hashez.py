import os
import hashlib

def salted(text, salt=10, rounds = 10000):
	if type(salt) == int:
		salt = os.urandom(salt).encode("hex")
	
	return hashlib.pbkdf2_hmac("sha256", text.encode("hex"), salt, rounds).encode("hex")+":"+salt
		
def verify(original_text, hash, rounds = 10000):
	[_, salt] = hash.split(":")[0:3]
	
	return salted(original_text, salt, rounds) == hash

if __name__ == "__main__":
	print verify("test123", salted("test12"))
	print verify("test12", salted("test12"))
	print verify("test12", salted("test12","asd"))
	print verify("test12", salted("test12","asd", 10),10)
	print verify("test12", salted("test12", rounds = 10),10)