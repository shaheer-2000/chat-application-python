import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

def send_handler(s):
	try:
		while True:
			text = input()
			if text == "[END]":
				break
			s.sendall(text.encode())
	except ConnectionResetError:
		pass

def recv_handler(s):
	try:
		while True:
			data = s.recv(1024)
			print(f"Received {data!r}")
	except ConnectionResetError:
		pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

threading.Thread(target=send_handler, args=(s, )).start()
threading.Thread(target=recv_handler, args=(s, )).start()