import time
from datetime import datetime

def epochtime():
	return time.time()

def datetimetime():
	return datetime.now()

def epoch2datetime(t):
	return datetime.fromtimestamp(t)

def datetime2epoch(d):
	return (d - datetime(1970,1,1)).total_seconds()

def strftime(e, f="%a %d %b %y - %X.%f"):
	if type(e) == float:	
		return epoch2datetime(e).strftime(f).rstrip("0")
	return e.strftime(f).rstrip("0")

def strf2datetime(s, f="%a %d %b %y - %X.%f"):
	return datetime.strptime(s, f)

def strf2epoch(s, f="%a %d %b %y - %X.%f"):
	return datetime2epoch(datetime.strptime(s, f))

if __name__ == "__main__":
	epoch = epochtime()
	dt = datetimetime()
	print(epoch)
	print(dt)
	print(epoch2datetime(epoch))
	print(datetime2epoch(dt))

	print(strftime(epoch))
	print(strftime(dt))

	print(strf2datetime(strftime(dt)))
	print(strf2epoch(strftime(dt)))
	print(strf2datetime(strftime(epoch)))
	print(strf2epoch(strftime(epoch)))