import RPi.GPIO as GPIO
import time

# GPIO pins
TRIG = 23
ECHO = 24

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Ensure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Send 10µs pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # Distance in cm (speed of sound: 34300 cm/s)
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)  # measure every second
except KeyboardInterrupt:
    print("Measurement stopped by user")
finally:
    GPIO.cleanup()
