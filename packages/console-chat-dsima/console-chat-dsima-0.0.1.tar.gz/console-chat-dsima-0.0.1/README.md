# Console Chat Dsima

This project is a test task for Digital Design. It's written without using any third-party library.

## Installation

It works only on Linux operating systems.

To install it run `pip install console-chat-dsima`

## Usage

To start a server

1. run `python -m chat-server`;
2. input server address (*127.0.0.1*, as an example).

To chat

1. run `python -m chat-client`;
2. input server address;
3. input your name;
4. to send a message input it's text and addressee;
5. to exit the chat input *exit*.

To stop the server press *Control+C*.

## Examples

### Server

```
$ python3 -m chat-server
Input server address: 127.0.0.1
^CTraceback (most recent call last): <...>
KeyboardInterrupt

```

### Client 1

```
$ python3 -m chat-client
Input server address: 127.0.0.1
Input your name: Ivan
To send a message input its text and addressee.
Input "exit" to exit.
Hey, how do you do?
Maria
Maria received your message.
Maria: I'm fine.
Save my soul!
God
God did not receive your message.
exit

```

### Client 2

```
$ python3 -m chat-client
Input server address: 127.0.0.1
Input your name: Maria
To send a message input its text and addressee.
Input "exit" to exit.
Ivan: Hey, how do you do?
I'm fine.                     
Ivan
Ivan received your message.
exit

```
