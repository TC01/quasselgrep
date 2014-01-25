from __future__ import print_function
import sys
import socket

from util import salt_and_hash, getdata, escape

def start(options, search, program):
	if not hasattr(options, 'hostname'):
		print("Error: You must supply a hostname.")
		return
	if not hasattr(options, 'password'):
		print("Error: You must supply a password")
		return

	port = options.port if hasattr(options, 'port') else 9001

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((options.hostname, port))

	sock.send(b'HI\n')

	response = getdata(sock)[0]

	if response[:5] != 'SALT=':
		print('Error: Did not understand server response.')
		return

	salt = response[5:]
	options.password = salt_and_hash(salt, options.password)
	command = b''
	for option in program.parser.option_list:
		opt_name = option.dest
		if not opt_name or not hasattr(options, opt_name):
			continue
		if not opt_name in program.valid_options:
			continue
		if getattr(options, opt_name) is None:
			continue

		command += ('%s=%s\n' % (opt_name, escape(str(getattr(options, opt_name))))).encode('utf-8')

	command += ('SEARCH=%s\n' % (search)).encode('utf-8')
	sock.sendall(command)

	while True:
		data = sock.recv(1024).decode('utf-8')
		if not data:
			break
		sys.stdout.write(data)

