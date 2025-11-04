import RPi.GPIO as GPIO
import time

# GPIO pins for Sensor 1
TRIG1 = 23
ECHO1 = 24

# GPIO pins for Sensor 2
TRIG2 = 5
ECHO2 = 6

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

def get_distance(TRIG, ECHO):
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout = pulse_start + 0.04  # 40 ms timeout
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # in cm
    distance = round(distance, 2)
    return distance

try:
    while True:
        # Sensor 1 fires
        dist1 = get_distance(TRIG1, ECHO1)
        if dist1 is not None:
            print(f"Sensor 1 Distance: {dist1} cm")
        else:
            print("Sensor 1: No reading")

        # Wait half a second before firing the next
        time.sleep(1)

        # Sensor 2 fires
        dist2 = get_distance(TRIG2, ECHO2)
        if dist2 is not None:
            print(f"Sensor 2 Distance: {dist2} cm")
        else:
            print("Sensor 2: No reading")

        print("------------------------")

        # Wait another half second before restarting loop
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()