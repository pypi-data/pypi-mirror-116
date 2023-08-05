# -*- coding: UTF-8 -*-

import json as _json
from enum import Enum as _Enum, auto as _auto

PORT = 60606

class MessageType(_Enum):
	GREETINGS = _auto()
	MESSAGE = _auto()
	EXIT = _auto()
	INFO = _auto()

class SocketData:
	def __init__(self):
		self.inb = b''
		self.outb = b''

class _MessageTypeEncoder(_json.JSONEncoder):
	def default(self, obj):
		if type(obj) == MessageType:
			return {'__enum__': str(obj)}
		else:
			super.default(self, obj)

def _as_MessageType(d):
	if '__enum__' in d:
		_, member = d['__enum__'].split('.')
		return getattr(MessageType, member)
	else:
		return d

def dict_to_bytes(dic):
	json = _json.dumps(dic, cls = _MessageTypeEncoder)
	return (json + '\0').encode('utf-8')

def bytes_to_dict(bytes):
	try:
		msg = bytes.decode('utf-8')
		dump = msg[0:-1]
		return _json.loads(dump, object_hook = _as_MessageType)
	except:
		return {}

def split_bytes(buff, recved):
	result = []
	index = recved.find(b'\x00')
	while index >= 0:
		message = buff + recved[:index + 1]
		result.append(message)
		buff = b''
		recved = recved[index + 1:]
		index = recved.find(b'\x00')
	buff += recved
	return (buff, result) 

if __name__ == '__main__':
	d1 = {'name': 'Danila', 'mood': 'depressed', 'age': 20, 'msgtp': MessageType.INFO}
	
	bytes = dict_to_bytes(d1)
	
	d2 = bytes_to_dict(bytes)
	
	print(d1 == d2, d1, d2, sep = '\n')
