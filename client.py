"""Run a basic client instance."""

import socket
import threading
import signal
import sys


class ClientSocket:

	def __init__(self):
		# used with socket#accept to timeout and capture SIGINT events
		socket.setdefaulttimeout(1)
		"""A pair (host, port) is used for the AF_INET address family, where host is
		a string representing either a hostname in internet domain notation like
		'daring.cwi.nl' or an IPv4 address like '100.50.200.5', and port is an
		integer."""
		"""https://beej.us/guide/bgnet/html/#two-types-of-internet-sockets.
		SOCK_STREAM, stream sockets or connection-oriented sockets"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.shutdown = False
		self.connections = {}
		self.recv_queue = []
		self.send_queue = []
		signal.signal(signal.SIGINT, self.sigint_handler)

	def sigint_handler(self, signum, frame):
		self.shutdown = True

	def connect(self, hostname, port):
		try:
			self.socket.connect((hostname, port))
			self._connection_handler()
		except TimeoutError:
			if self.shutdown:
				print("Client closing")
				# self.socket.shutdown(socket.SHUT_RD)
				self.socket.close()

	def _connection_handler(self):
		threading.Thread(target=self._recv_handler).start()
		threading.Thread(target=self._send_handler).start()

	def _recv_handler(self):
		i = 0
		while True:
			if self.shutdown or type(self.socket) is socket.SocketType:
				break
			
			recv_data = None
			try:
				self.socket.settimeout(1)
				recv_data = self.socket.recv(1024)
			except TimeoutError:
				if self.shutdown:
					break
			except OSError:
				if self.shutdown:
					break

			if recv_data is not None and len(recv_data):
				print(recv_data)
				# producer/consumer behaviour by tkinter
				self.recv_queue.append(recv_data)

	def _send_handler(self):
		while True:
			if self.shutdown or type(self.socket) is socket.SocketType:
				break

			if self.send_queue:
				if self.send_queue[0] == "[END]":
					break

				send_data = self.send_queue.pop(0)
				send_data = send_data.encode()

				# producer/consumer behaviour by tkinter
				try:
					self.socket.sendall(send_data)
				except TimeoutError:
					if self.shutdown:
						break

	def get_recv_msg(self):
		if len(self.recv_queue):
			return self.recv_queue.pop(0)

	def set_send_msg(self, data):
		self.send_queue.append(data)

	def close_socket(self):
		self.shutdown = True
		print("Client closing")
		# self.socket.shutdown(socket.SHUT_RD)
		self.socket.close()

# client_socket = ClientSocket()
# client_socket.connect("127.0.0.1", 8000)
# print("test")

# while True:
# 	try:
# 		e = input()
# 		client_socket.set_send_msg(e)
# 		print(client_socket.get_recv_msg())
# 		if e == "[END]":
# 			break
# 	except:
# 		break