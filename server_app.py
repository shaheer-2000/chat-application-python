# DO NOT MERGE THIS
import tkinter as tk
from tkinter import messagebox
from server import ServerSocket
import logging

# window = tk.Tk()
# greeting = tk.Label(text="Hello World")
# tk.Button(text="Listen", width=25, height=5).pack()
# tk.Entry(width=50).pack()
# greeting.pack()
# window.mainloop()

class Application:
	def __init__(self):
		self.window = tk.Tk()

	def ent_widget(self):
		ent_widget = tk.Entry(width=50)
		ent_widget.pack()
		return ent_widget

	def btn_widget(self, text):
		btn_widget = tk.Button(text=text, width=50, height=5)
		btn_widget.pack()
		return btn_widget

	def ent_closure(self, ent, event_handler):
		print("test", ent.get())
		return event_handler

	def submit_conn(self, ent_ip: str, ent_port: str):
		if ent_ip.isnumeric() and ent_port.isnumeric():
			# TODO: regex for valid port and ip
			self.server = ServerSocket(logging, {
				"host": ent_ip,
				"port": ent_port
			})
			messagebox.showinfo("Connected", "Server socket is listening for connections")
		else:
			messagebox.showerror("Invalid IP or PORT", "Please enter correct IP and PORT")

	def send_msg(self, msg):
		self.server.send_handler()
		print(msg.strip())

	def build(self):
		ent_ip = self.ent_widget()

		ent_port = self.ent_widget()
		btn_conn = self.btn_widget("Listen")
		btn_conn.bind("<Button-1>", lambda e: self.submit_conn(ent_ip.get(), ent_port.get()))

		txt_chatbox = tk.Text(self.window)
		txt_chatbox.pack()
		btn_send = self.btn_widget("Send")
		btn_send.bind("<Button-1>", lambda e: self.send_msg(txt_chatbox.get("1.0", tk.END)))

	def start(self):
		self.window.mainloop()

app = Application()
app.build()
app.start()