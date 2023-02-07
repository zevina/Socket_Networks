import socket
from threading import Thread
from datetime import datetime


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 55555
sep_token = "<SEP>"

s = socket.socket()
print(f"[...] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send =  input()
    # способ выхода из программы
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"[{date_now}] {name}{sep_token}{to_send}"
    s.send(to_send.encode())

# закрыть сокет клиента
s.close()