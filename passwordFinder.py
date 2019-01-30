# pip install msoffcrypto-tool

import msoffcrypto
import os
import requests
import string
import sys
import time

try:
    import config
except ImportError:
	config = {}

# Set up string things
charset = string.letters + string.digits
nextchar = {}
for i, c in enumerate(charset[:-1]):
	nextchar[c] = charset[i + 1]
print nextchar

# Set up other things
logfile = open('output.log', 'a')
password = ""
if os.path.isfile('passwordprogress.log'):
	with open('passwordprogress.log', 'r') as f:
	    password = f.readline()

count = 0
starttime = time.time()
filename = sys.argv[1]
file = msoffcrypto.OfficeFile(open(filename, "rb"))

def incrementString(s):
	if s == "":
		return charset[0]
	if s[-1] == charset[-1]:
		return incrementString(s[:-1]) + charset[0]
	return s[:-1] + nextchar[s[-1]]

def tryPassword(p):
	try:
		file.load_key(password=p)
		return True
	except AssertionError:
		return False
	except Exception as e:
		logfile.write("Error trying password {}: {}\n".format(p, str(e)))
		logfile.flush()
		os.fsync(logfile.fileno())
		return False

def foundPassword():
	print "Password is " + password
	logfile.write("Password is " + password);
	logfile.flush()
	os.fsync(logfile.fileno())

	if config.MAILGUN_URL:
		requests.post(
			config.MAILGUN_URL,
			auth=("api", config.MAILGUN_KEY),
			data={
				"from": config.MAILGUN_EMAIL,
				"to": "Joseph Lee <z.joseph.lee.z@gmail.com>",
				"subject": "Found password for file {}".format(filename),
				"html": "<html><pre><code>" + password + "</code></pre></html>"})

def saveProgress():
	with open('passwordprogress.log', 'w') as f:
	    f.write(password)
	    f.close()
	logfile.write("Got to password {} ({} this run, {} s elapsed)".format(password, count, time.time() - starttime));
	logfile.flush()
	os.fsync(logfile.fileno())

if __name__ == "__main__":
	while True:
		found = tryPassword(password)
		if found:
			foundPassword()
			break
		else:
			count += 1

			# linode is ~4k/s, so pause every 10s, save every 5 min
			if count % 40000 == 0:
				time.sleep(0.5)
			if count % 1200000 == 0:
				saveProgress()
			password = incrementString(password)
	print "done"