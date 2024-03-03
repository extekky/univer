import sys
import json
import evdev


def readInputEvents(input_device):
    events = []
    try:
        for event in input_device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                event_dict = {
                    "type": "EV_KEY",
                    "code": event.code,
                    "state": event.value
                }
                events.append(event_dict)
                print(event_dict)
            if event.type == evdev.ecodes.EV_REL:
                event_dict = {
                    "type": "EV_REL",
                    "value": event.value
                }
                events.append(event_dict)
                print(event_dict)
    except KeyboardInterrupt:
        pass
    finally:
        input_device.close()
        return events


def main():
    if len(sys.argv) != 2:
        return "Usage: python3 <input_reader.py> <input_device>"

    input_device_path = sys.argv[1]
    try:
        input_device = evdev.InputDevice(input_device_path)
    except FileNotFoundError:
        return f"Error: Input device '{input_device_path}' not found"
    except PermissionError:
        return f"Error: Permission denied to access input device '{input_device_path}'"

    events = readInputEvents(input_device)
    return json.dumps(events, indent=4)


if __name__ == "__main__":
    print(main())

