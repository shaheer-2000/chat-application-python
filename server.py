"""Run a basic server instance."""

import socket
import threading
import signal
import sys


class ServerSocket:

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

	def serve(self, hostname, port):
		self.socket.bind((hostname, port))
		# set backlog to 1, to allow atmost 1 unaccepted connection
		self.socket.listen(1)

	def _connection_handler(self, conn, addr):
		self.connections[str(addr)] = conn
		print(conn, addr)
		threading.Thread(target=self._recv_handler, args=(conn, addr)).start()
		threading.Thread(target=self._send_handler, args=(conn, addr)).start()

	def _recv_handler(self, conn: socket, addr):
		while True:
			if self.shutdown or type(conn) is socket.SocketType:
				break
			
			recv_data = None
			try:
				self.socket.settimeout(1)
				recv_data = conn.recv(1024)
			except TimeoutError:
				if self.shutdown:
					break
			except OSError:
				if self.shutdown:
					break

			if recv_data is not None and len(recv_data):
				# producer/consumer behaviour by tkinter
				print(recv_data)
				self.recv_queue.append(recv_data)

	def _send_handler(self, conn: socket, addr):
		while True:
			if self.shutdown or type(conn) is socket.SocketType:
				break

			if self.send_queue:
				if self.send_queue[0] == "[END]":
					break

				send_data = self.send_queue.pop(0)
				send_data = send_data.encode()

				# producer/consumer behaviour by tkinter
				print(send_data)
				conn.sendall(send_data)

	def get_recv_msg(self):
		if len(self.recv_queue):
			return self.recv_queue.pop(0)

	def set_send_msg(self, data):
		self.send_queue.append(data)

	def accept_conns(self):
		while True:
			try:
				conn, addr = self.socket.accept()
				self._connection_handler(conn, addr)
			except TimeoutError:
				if self.shutdown:
					for conn in self.connections:
						self.connections[conn].close()
					print("Server closing")
					# self.socket.shutdown(socket.SHUT_RD)
					self.socket.close()
					break
				continue
			except OSError:
				if self.shutdown:
					if self.socket and self.socket is socket.SocketType:
						self.socket.close()
					break

	def close_socket(self):
		self.shutdown = True
		for conn in self.connections:
			self.connections[conn].close()
		print("Server closing")
		# self.socket.shutdown(socket.SHUT_RD)
		if self.socket and self.socket is socket.SocketType:
			self.socket.close()

# server_socket = ServerSocket()
# server_socket.serve("0.0.0.0", 8000)
# threading.Thread(target=server_socket.accept_conns).start()

# while True:
# 	try:
# 		e = input()
# 		server_socket.set_send_msg(e)
# 		print(server_socket.get_recv_msg())
# 		if e == "[END]":
# 			break
# 	except:
# 		break