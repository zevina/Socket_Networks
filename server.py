import socket
from threading import Thread

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 55555
sep_token = "<SEP>" # для разделения имени клиента и сообщения

# список всех подключенных клиентских сокетов
client_sockets = set()

s = socket.socket()
# сделать порт многоразовым
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[...] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Эта функция продолжает прослушивать сообщение от сокета `cs`
    Всякий раз, когда сообщение получено, транслирует его всем другим подключенным клиентам
    """
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            # если клиент отсоединился, то удалить его из списка
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(sep_token, ": ")

        for client_socket in client_sockets:
            # разослать полученное сообщение всем подключенным клиентам из списка
            client_socket.send(msg.encode())


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

# закрыть клиентские сокеты
for cs in client_sockets:
    cs.close()
# закрыть сокет сервера
s.close()