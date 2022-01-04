import socket
import threading
import tkinter
from tkinter import scrolledtext
from tkinter import simpledialog

host = '127.0.0.1'
port = 9090

class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring('Nickname', 'Please choose a nickname', parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk
        self.win.configure(bg='lightgray')

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg='lightgray')
        self.chat_label.config(font=('Arial', 12))
        self.chat_label.pack(padx=20, pady=5)

        self.textarea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textarea.pack(padx=20, pady=5)
        self.textarea.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg='lightgray')
        self.msg_label.config(font=('Arial', 12))
        self.msg_label.pack(padx=20, pady=5)

        self.inputarea = tkinter.Text(self.win, height=3)
        self.inputarea.pack(padx=20, pady=5)

        self.senbtn = tkinter.Button(self.win, text='Send', command=self.write)
        self.senbtn.config(font=('Arial', 12))
        self.senbtn.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW', self.stop)

        self.win.mainloop()

    def write(self):
        message = f'{self.nickname}: {self.inputarea.get("1.0", "end")}'
        self.sock.send(message.encode('utf-8'))
        self.inputarea.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.textarea.config(state='normal')
                        self.textarea.insert('end', message)
                        self.textarea.yview('end')
                        self.textarea.config('disabled')
            except ConnectionAbortedError:
                break
            except:
                print('Error 666')
                self.sock.close()
                break

client = Client(host, port)