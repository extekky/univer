from scapy.all import *
import socket

# Адрес и порт сервера QOTD
server = "djxmmx.net"
port = 17

def main():
    # Получение IP-адреса сервера
    server_ip = socket.gethostbyname(server)
    
    # Создание UDP-пакета
    packet = IP(dst=server_ip)/UDP(dport=port)/Raw(load="")
    
    # Отправка пакета и ожидание ответа
    ans, unans = sr(packet, timeout=2, multi=True)
    
    # Обработка ответа
    for snd, rcv in ans:
        # Извлечение и декодирование строки ответа
        quote = rcv[Raw].load.decode('utf-8')
        print(quote)

if __name__ == "__main__":
    main()
