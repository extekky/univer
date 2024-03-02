import sys
import json
import evdev


def read_input_events(input_device):
    events = []
    for event in input_device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            events.append({'type': 'EV_KEY', 'code': event.code, 'value': event.value})
        elif event.type == evdev.ecodes.EV_REL:
            events.append({'type': 'EV_REL', 'code': event.code, 'value': event.value})
        if len(events) >= 10:
            return events


def main():
    if len(sys.argv) != 2:
        return "Usage: python3 <input_reader.py> <input_device>"

    input_device_path = sys.argv[1]
    try:
        input_device = evdev.InputDevice(input_device_path)
    except FileNotFoundError:
        return f"Error: Input device '{input_device_path}' not found"

    events = read_input_events(input_device)
    return json.dumps(events, indent=4)


if __name__ == "__main__":
    print(main())
