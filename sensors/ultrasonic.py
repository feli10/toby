import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig, echo, name="Sensor"):
        self.trig = trig
        self.echo = echo
        self.name = name
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig, False)
        time.sleep(0.05)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        pulse_start = time.time()
        timeout = pulse_start + 0.04
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None

        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # in cm
        return round(distance, 2)