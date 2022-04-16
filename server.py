from cmath import log
import logging
import threading
import time
import socket
import signal
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432
DEFAULT_TIMEOUT = 0.5

class ServerSocket:
	def __init__(self, logging, socket_config = {}):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(socket_config["timeout"] if "timeout" in socket_config else DEFAULT_TIMEOUT)
		self.sock.bind((socket_config["host"] if "host" in socket_config else DEFAULT_HOST, socket_config["port"] if "port" in socket_config else DEFAULT_PORT))
		self.logging = logging
		signal.signal(signal.SIGINT, self.sigint_handler)
		self.connections = []

	def listen(self):
		self.sock.listen()

	def log_main(self, msg):
		self.logging.info(f"[MAIN]\t: {msg}")

	def log_thread(self, msg):
		self.logging.info(f"[THREAD]\t: {msg}")

	def connection_handler(self, conn, addr):
		try:
			self.log_thread(f"Connected to {addr}")
			self.connections.append(conn)
			while True:
				data = conn.recv(1024)
				if data == b"[END]":
					conn.close()
					raise Exception()
				conn.sendall(data)
		except:
			if conn:
				conn.close()
			self.log_thread(f"Connection to {addr} has been closed")

	def fork_connection(self, conn, addr):
		threading.Thread(target=self.connection_handler, args=(conn, addr)).start()

	def sigint_handler(self, signum, frame):
		self.log_main("Closing all connection clients' connection")
		for conn in self.connections:
			conn.close()
		self.log_main("Closing socket connection")
		if self.sock:
			self.sock.close()
		self.log_main("Socket connection closed")
		sys.exit(0)

	def start(self):
		self.listen()

		while True:
			try:
				conn, addr = self.sock.accept()
				self.log_main(f"Accepted connection request from {addr}")
				self.fork_connection(conn, addr)
				self.log_main("Started a new connection thread")
			except socket.timeout:
				pass
			except KeyboardInterrupt:
				self.log_main("Closing socket connection")
				if self.sock:
					self.sock.close()
				
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
server = ServerSocket(logging)
server.start()