# -*- coding: UTF-8 -*-

from utils import *
from queue import Queue, Empty
from threading import Thread
import socket, selectors

def process(message, msg_queue):
	msg = bytes_to_dict(message)
	if 'type' in msg:
		if msg['type'] == MessageType.MESSAGE:
			print(msg['from'], msg['text'], sep = ': ')
			answer = {'type': MessageType.INFO, 'to': msg['from'], 'info': f'{msg["to"]} received your message.'}
			msg_queue.put(answer)
		elif msg['type'] == MessageType.INFO:
			print(msg['info'])
	else:
		print(msg)

def process_msgs(msg_queue, sel):
	running = True
	while running:
		for key, mask in sel.select(timeout = None):
			sock = key.fileobj
			context = key.data
			if mask & selectors.EVENT_READ:
				recv_data = sock.recv(1024)
				context.inb, msgs = split_bytes(context.inb, recv_data)
				for msg in msgs:
					process(msg, msg_queue)
			if mask & selectors.EVENT_WRITE:
				if context.outb == b'':
					try:
						msg = msg_queue.get_nowait()
						if msg['type'] == MessageType.EXIT:
							running = False
							sel.unregister(sock)
							sock.close()
						else:
							context.outb = dict_to_bytes(msg)
						msg_queue.task_done()
					except Empty:
						pass
				else:
					sent = sock.send(context.outb)
					context.outb = context.outb[sent:]
	sel.close()

def start_receiving():
	msg_queue = Queue()
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setblocking(False)
	sock.connect_ex((address, PORT))
	
	sel = selectors.DefaultSelector()
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	data = SocketData()
	sel.register(sock, events, data=data)
	
	receiving_thread = Thread(target = process_msgs, args = (msg_queue, sel))
	receiving_thread.start()
	
	return msg_queue

if __name__ == '__main__':
	address = input('Input server address: ')
	name = input('Input your name: ')
	
	print('To send a message input its text and addressee.\nInput "exit" to exit.')
	
	msg_queue = start_receiving()
	
	greetings = {'type': MessageType.GREETINGS, 'name': name}
	msg_queue.put(greetings)
	
	text = input()
	while text != 'exit':
		addressee = input()
		message = {'type': MessageType.MESSAGE, 'from': name, 'to': addressee, 'text': text}
		msg_queue.put(message)
		text = input()
	
	msg_queue.put({'type': MessageType.EXIT})
	msg_queue.join()
