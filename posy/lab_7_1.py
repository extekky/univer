import socket
import select


def main():
    server_address = ('lolpok', 10000)
    buffer_size = 1024
    timeout = None

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)

        while True:
            try:
                # Отправляем запрос на сервер
                message = "Enter a command: "
                sock.sendto(message.encode(), server_address)

                # обработкa таймаута
                ready = select.select([sock], [], [], timeout)
                if ready[0]:
                    data, addr = sock.recvfrom(buffer_size)
                    response = data.decode().strip()

                    if response.startswith('T '):
                        _, t_value = response.split()
                        timeout = int(t_value)  # получаем значение
                        sock.settimeout(timeout)
                        print(f"Setting timeout to {timeout}")
                    elif response == 'Q':
                        print("Quitting")
                        break
                    else:
                        print(f"Response from {addr}: {response}")
                else:
                    print("Timeout expired, quitting")
                    break

            except socket.timeout:
                print("Timeout expired, quitting")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break


if __name__ == "__main__":
    main()
