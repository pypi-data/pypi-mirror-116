# -*- coding: UTF-8 -*-

from utils import *
import selectors
import socket
from queue import Queue
import syslog

class MemoryNode:
	def __init__(self, username, sock):
		self.username = username
		self.sock = sock
		self.msg_queue = Queue()
		self.current_msg = None

class Memory:
	
	def __init__(self):
		self.by_username = {}
		self.by_socket = {}
	
	def put_in_users_msgs(self, username, element):
		if username in self.by_username:
			node = self.by_username[username]
			node.msg_queue.put(element)
			return True
		else:
			return False
	
	def create_error_message(self, addresser, addressee):
		return {'type': MessageType.INFO, 'to': addresser, 'info': f'{addressee} did not receive your message.'}
	
	def process(self, message, sock):
		if 'type' in message:
			tp = message['type']
			if tp == MessageType.GREETINGS:
				username = message['name']
				node = MemoryNode(username, sock)
				self.by_username[username] = node
				self.by_socket[sock] = node
			elif tp == MessageType.INFO:
				addressee = message['to']
				self.put_in_users_msgs(addressee, message)
			elif tp == MessageType.MESSAGE:
				addresser = message['from']
				addressee = message['to']
				msg_put = self.put_in_users_msgs(addressee, message)
				if not msg_put:
					err_msg = self.create_error_message(addresser, addressee)
					self.put_in_users_msgs(addresser, err_msg)
	
	def process_closed_socket(self, sock):
		if sock in self.by_socket:
			node = self.by_socket[sock]
			if node.current_msg is not None:
				node.msg_queue.put(node.current_msg)
			while not node.msg_queue.empty():
				msg = node.msg_queue.get()
				if msg['type'] == MessageType.MESSAGE:
					addresser = msg['from']
					err_msg = self.create_error_message(addresser, msg['to'])
					self.put_in_users_msgs(addresser, err_msg)
			del self.by_username[node.username]
			del self.by_socket[node.sock]
	
	def message_delivered(self, sock):
		if sock in self.by_socket:
			node = self.by_socket[sock]
			node.current_msg = None
	
	def next_message(self, sock):
		if sock in self.by_socket:
			node = self.by_socket[sock]
			node.current_msg = None if node.msg_queue.empty() else node.msg_queue.get()
			return node.current_msg
		else:
			return None

def accept_wrapper(sock, sel):
	conn, addr = sock.accept()
	conn.setblocking(False)
	data = SocketData()
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	sel.register(conn, events, data=data)

def log_message(message):
	if ('type' in message) and (message['type'] == MessageType.MESSAGE):
		syslog.syslog(f'FROM {message["from"]} TO {message["to"]} MESSAGE {message["text"]}')

def service_connection(key, mask, mem):
	sock = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = sock.recv(1024)
		if recv_data:
			data.inb, msgs_bytes = split_bytes(data.inb, recv_data)
			for bytes in msgs_bytes:
				msg = bytes_to_dict(bytes)
				log_message(msg)
				mem.process(msg, sock)
		else:
			sel.unregister(sock)
			sock.close()
			mem.process_closed_socket(sock)
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			sent = sock.send(data.outb)
			data.outb = data.outb[sent:]
			if not data.outb:
				mem.message_delivered(sock)
		else:
			message = mem.next_message(sock)
			data.outb = b'' if message is None else dict_to_bytes(message)

if __name__ == '__main__':
	host = input('Input server address: ')
	
	sel = selectors.DefaultSelector()
	
	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind((host, PORT))
	listening_socket.listen()
	listening_socket.setblocking(False)
	
	sel.register(listening_socket, selectors.EVENT_READ, data=None)
	
	mem = Memory()
	
	syslog.openlog(ident = 'chat server')
	
	while True:
		events = sel.select(timeout = None)
		for key, mask in events:
			if key.data is None:
				accept_wrapper(key.fileobj, sel)
			else:
				service_connection(key, mask, mem)
