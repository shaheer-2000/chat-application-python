# TODO: Refactor to OOP and cleanup code

from tkinter import *
import threading
from server import ServerSocket

root = Tk()

root.title("Server Application")
ip_label = Label(root, text="IP Addr:")
ip_entry = Entry(root, width=20)
port_label = Label(root, text="Port")
port_entry = Entry(root, width=10)

ip_label.grid(row=0, column=0, padx=2, pady=5, sticky=W)
ip_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=W)
port_label.grid(row=1, column=0, padx=2, pady=5, sticky=W)
port_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=W)

server_socket = ServerSocket()

def get_addrinfo():
	ip = ip_entry.get()
	port = port_entry.get()

	print(ip, port)
	
	server_socket.serve(ip, int(port))
	threading.Thread(target=server_socket.accept_conns).start()

send_entry = Entry(root, width=20)
send_entry.grid(row=5, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=W)

msg_box = Text(root, height=10, width=20, state=DISABLED)
msg_box.grid(row=3, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=W, columnspan=5)

def send_msg():
	msg = send_entry.get()
	if len(msg):
		server_socket.set_send_msg(msg)
		msg_box.config(state=NORMAL)
		msg_box.insert(END, "[SERVER]: " + msg + "\n")
		msg_box.config(state=DISABLED)
		send_entry.delete(0, END)

stop = False

def rcv_msg():
	global stop
	while True:
		if stop:
			break

		msg = server_socket.get_recv_msg()
		if msg is not None and len(msg):
			print(msg)
			
			msg_box.config(state=NORMAL)
			msg_box.insert(END, "[CLIENT]: " + msg.decode() + "\n")
			msg_box.config(state=DISABLED)

connect_btn = Button(root, text="Listen", command=get_addrinfo)
connect_btn.grid(row=1, column=2, padx=2, pady=5, ipadx=10, ipady=5, sticky=E)

send_btn = Button(root, text="Send", padx=20, pady=5, command=send_msg)
send_btn.grid(row=5, column=2)

threading.Thread(target=rcv_msg).start()

root.mainloop()
stop = True
print("test")
server_socket.close_socket()
