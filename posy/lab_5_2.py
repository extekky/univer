import json
import time
from collections import defaultdict
from scapy.all import sniff, IP, ICMP

# Структура для хранения данных о сессиях
sessions = defaultdict(lambda: {
    "id": "",
    "src": "",
    "dst": "",
    "nrequests": 0,
    "nresponses": 0,
    "rtt_times": []
})


# Обработчик пакетов
def handle_packet(packet):
    if packet.haslayer(ICMP):
        icmp = packet[ICMP]
        ip = packet[IP]

        if icmp.type == 8:  # Echo Request
            session_id = icmp.id
            if sessions[session_id]["id"] == "":
                sessions[session_id]["id"] = hex(session_id)
                sessions[session_id]["src"] = ip.src
                sessions[session_id]["dst"] = ip.dst
            sessions[session_id]["nrequests"] += 1
            sessions[session_id]["rtt_times"].append({
                "seq": icmp.seq,
                "time_sent": time.time(),
                "time_received": None
            })

        elif icmp.type == 0:  # Echo Reply
            session_id = icmp.id
            seq_num = icmp.seq
            for rtt in sessions[session_id]["rtt_times"]:
                if rtt["seq"] == seq_num and rtt["time_received"] is None:
                    rtt["time_received"] = time.time()
                    sessions[session_id]["nresponses"] += 1
                    break


def capture_packets(timeout=60):
    sniff(iface="wlp2s0", filter="icmp", prn=handle_packet, timeout=timeout)


# Функция для вычисления статистики и вывода результатов
def print_results():
    result = {}
    for session_id, data in sessions.items():
        rtt_times = [rtt["time_received"] - rtt["time_sent"] for rtt in data["rtt_times"] if
                     rtt["time_received"] is not None]
        if rtt_times:
            data["min-rtt"] = min(rtt_times)
            data["max-rtt"] = max(rtt_times)
        else:
            data["min-rtt"] = None
            data["max-rtt"] = None
        result[hex(session_id)] = data

        del data["rtt_times"]

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    try:
        capture_packets()
    except KeyboardInterrupt:
        pass
    print_results()
