import redis
import socket
import select

r = redis.Redis(host='localhost', port=6379, db=0)


def work_with_redis(command_for_redis):
    command_parts = command_for_redis.split()
    if command_parts[0] == 'W':
        try:
            r.set(command_parts[1], command_parts[2])
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    elif command_parts[0] == 'R':
        try:
            value = r.get(command_parts[1])
            if value is not None:
                return value.decode()
            else:
                return False
        except Exception as e:
            print(f"Redis get error: {e}")
            return False
    else:
        return False


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        if not data:
            return False
        command = data.decode().strip()
        print(f"Client sent: {command}")
        result = work_with_redis(command)
        if result is True:
            client_socket.send("OK".encode())
        elif result is False:
            client_socket.send("NO".encode())
        else:
            client_socket.send(result.encode())
        return True
    except Exception as e:
        print(f"Client handling error: {e}")
        return False


# Создаем объект сокета сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()                         # Получаем имя хоста локальной машины
port = 12345                                            # Устанавливаем порт сервера
server_socket.bind((hostname, port))                    # Привязываем сокет сервера к хосту и порту
server_socket.listen(5)                                 # Начинаем прослушивание входящих подключений
server_socket.setblocking(0)                            # Устанавливаем неблокирующий режим

print("Server running")

# Список сокетов для мониторинга с помощью select
sockets_list = [server_socket]
clients = {}

while True:
    # Используем select для мониторинга сокетов
    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Функция select.select из модуля select позволяет отслеживать несколько сокетов одновременно,
    # чтобы определить, какие из них готовы к чтению, записи или имеют исключения

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # Принимаем новое подключение
            client_socket, client_address = server_socket.accept()
            client_socket.setblocking(0)                # Устанавливаем неблокирующий режим для клиента
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted new connection from {client_address}")
        else:
            # Обрабатываем данные от существующего клиента
            if not handle_client(notified_socket):
                print(f"Closed connection from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                notified_socket.close()
                del clients[notified_socket]

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        notified_socket.close()
        del clients[notified_socket]