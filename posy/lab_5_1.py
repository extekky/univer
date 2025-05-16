from scapy.all import sniff
import json
import time
import sys

# Глобальный словарь для хранения времени последнего перехвата
last_seen = {}


def custom_serializer(some_object):
    if isinstance(some_object, bytes):
        return some_object.decode(errors='ignore')
    else:
        return str(some_object)


def packet_to_dict(packet):     # Добываем здесь нужную нам информацию из пойманного пакета
                                # и формируем таблицу (словарь) ключ-значение
    packet_dict = {}

    # Нужны уровни L2 (Link) и L3 (IP)
    if packet.haslayer("Ether") and packet.haslayer("IP"):
        eth = packet.getlayer("Ether") 
        ip = packet.getlayer("IP")

        current_time = time.time()
        key = ip.src

        if key in last_seen:
            age = current_time - last_seen[key]  # Возраст записи

            if age <= 5:    # Учитываем только записи возрастом до 5 секунд
                packet_dict[key] = {
                    'mac': eth.src,
                    'age': age
                }
        else:
            age = 0  # Если ee не было, зачит она только родилась
            packet_dict[key] = {
                'mac': eth.src,
                'age': age
            }

        last_seen[key] = current_time

    return packet_dict


def packet_handler(packet):
    packet_info = packet_to_dict(packet)
    if packet_info is not None:
        packet_info_json = json.dumps(packet_info, indent=4, default=custom_serializer)

    # default=custom_serializer - это параметр, используемый в функции json.dumps() для обработки
    # объектов, которые не могут быть сериализованы стандартным способом. Функция json.dumps() преобразует
    # объекты Python в JSON-строки. Однако, если она сталкивается с объектом, который не знает,
    # как сериализовать (например, объекты, не являющиеся встроенными типами Python, такими как dict,
    # list, str, int и т.д.), она вызывает ошибку TypeError.

    print(packet_info_json)


def start_sniffing(interface):
    sniff(iface=interface, prn=packet_handler, store=False)

    # Параметр prn указывает функцию-обработчик, которая будет
    # вызываться для каждого захваченного пакета. Этот параметр
    # позволяет вам определить, что делать с каждым пакетом, когда он захватывается.


if __name__ == "__main__":
    interface = "wlp2s0"  # Название моего интерфейса (WiFi)
    start_sniffing(interface)
