from Crypto.Hash import SHA

def getdata(socket):
	command = ''
	while True:
		data = socket.recv(1024).decode('utf-8')
		if not data:
			break
		command += data
		if data[-1] == '\n':
			break

	return command.split('\n')

def salt_and_hash(salt, password):
	h = SHA.new()
	h.update(password.encode('utf-8'))
	pwhash = h.hexdigest()

	return salt_hash(salt, pwhash)

def salt_hash(salt, pwhash):
	h = SHA.new()
	if isinstance(salt, str):
		salt = salt.encode('utf-8')
	if isinstance(pwhash, str):
		pwhash = pwhash.encode('utf-8')
	h.update(salt)
	h.update(pwhash)

	return h.hexdigest()

def escape(string):
	string = string.replace('\\', r'\\')
	string = string.replace('\n', r'\n')
	return string

