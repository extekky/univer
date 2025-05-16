from scapy.all import *

server = "test.rebex.net"
port = 21


def main():
    server_ip = socket.gethostbyname(server)  # lolpok

    # Установление TCP-соединения с сервером
    syn = IP(dst=server_ip) / TCP(dport=port, flags='S')
    syn_ack = sr1(syn)

    ack = IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A')
    send(ack)

    # Прием приветственного сообщения
    welcome_message = sr1(IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A'), timeout=2)
    print(welcome_message[Raw].load.decode('utf-8'))

    # Отправка запроса SYST
    syst_cmd = IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='PA') / Raw(load='SYST\r\n')
    send(syst_cmd)

    # Получение ответа на запрос SYST
    syst_response = sr1(IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack + len('SYST\r\n'), ack=syn_ack[TCP].seq + 1, flags='A'), timeout=2)
    response_text = syst_response[Raw].load.decode('utf-8')
    print("Server system info:", response_text.strip())

    # Закрытие соединения
    fin = IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack + len('SYST\r\n'), ack=syn_ack[TCP].seq + 1, flags='FA')
    fin_ack = sr1(fin)

    last_ack = IP(dst=server_ip) / TCP(dport=port, sport=syn_ack[TCP].dport, seq=fin_ack[TCP].ack, ack=fin_ack[TCP].seq + 1, flags='A')
    send(last_ack)


if __name__ == "__main__":
    main()
