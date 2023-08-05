from setuptools import setup

long_descr = ''
with open('README.md', 'r') as fh:
	long_descr = fh.read()

setup(
	name = 'console-chat-dsima',
	version = '0.0.1',
	description = 'Console chat.',
	classifiers = [
		'Programming Language :: Python :: 3.8',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux'
	],
	py_modules = [
		'chat-client',
		'chat-server',
		'utils'
	],
	package_dir = {'': 'src'},
	long_description = long_descr,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/danilasimanok/ConsoleChat',
	author = 'Danila Simanok',
	author_email = 'danilasimanok@gmail.com'
)
