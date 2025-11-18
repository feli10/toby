import config
import serial
import time

class ArduinoInterface:
    def __init__(self, port=config.ARDUINO_PORT, baudrate=config.ARDUINO_BAUD):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # wait for Arduino reset

    def start_monitoring(self):
        """Tell Arduino to begin monitoring capacity."""
        self.ser.write(b"START\n")

    def display_message(self, msg):
        """Override LCD display."""
        self.ser.write(f"DISPLAY:{msg}\n".encode())

    def read_line(self):
        """Read a line from Arduino, if available."""
        if self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return None