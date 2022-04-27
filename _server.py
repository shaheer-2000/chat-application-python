import logging
import threading
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
		self.logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
		signal.signal(signal.SIGINT, self.sigint_handler)
		self.connections = {}

	def listen(self):
		self.sock.listen()

	def log_main(self, msg):
		self.logging.info(f"[MAIN]\t: {msg}")

	def log_thread(self, msg):
		self.logging.info(f"[THREAD]\t: {msg}")

	def recv_handler(self, conn, addr):
		try:
			while True:
				data = conn.recv(1024)
				self.log_thread(f"[RECV -> {addr}] | {data}")
				if data == b"[END]":
					conn.close()
					raise Exception()
		except:
			if conn:
				conn.close()
			self.log_thread(f"Connection to {addr} has been closed")

	def send(self, addr, data):
		if addr not in self.connections:
			raise Exception()

		conn = self.connections[addr]
		if conn and data and len(data) > 0:
			conn.sendall(data)
			self.log_thread(f"[SENT -> {addr}] | {data}")

	def send_handler(self, addr):
		try:
			while True:
				msg = input()
				self.send(addr, msg.encode())
		except EOFError:
			pass

	def connection_handler(self, conn, addr):
		self.log_thread(f"Connected to {addr}")
		self.connections[addr] = conn
		threading.Thread(target=self.recv_handler, args=(conn, addr)).start()
		threading.Thread(target=self.send_handler, args=(addr,)).start()

	def fork_connection(self, conn, addr):
		threading.Thread(target=self.connection_handler, args=(conn, addr)).start()

	def sigint_handler(self, signum, frame):
		self.log_main("Closing all connection clients' connection")
		for conn in list(self.connections.values()):
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
				# self.fork_connection(conn, addr)
				self.connection_handler(conn, addr)
				self.log_main("Started a new connection thread")
			except socket.timeout:
				pass
			except KeyboardInterrupt:
				self.log_main("Closing socket connection")
				if self.sock:
					self.sock.close()

server = ServerSocket(logging)
server.start()
