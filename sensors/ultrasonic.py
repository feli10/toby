import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    """Driver for HC-SR04 ultrasonic distance sensor.
    Measures distance by:
    1. Sending a 10μs pulse to TRIG pin
    2. Sensor emits 8 ultrasonic pulses at 40kHz
    3. Measuring time until echo received on ECHO pin
    4. Calculating distance from time (speed of sound = 343 m/s)
    """
    
    def __init__(self, trig, echo, name="Sensor"):
        """Initialize ultrasonic sensor."""
        self.trig = trig
        self.echo = echo
        self.name = name
        
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def get_distance(self):
        """Measure distance to nearest object."""

        GPIO.output(self.trig, False)
        time.sleep(0.05)

        # Send 10μs pulse to trigger sensor measurement
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        # Wait for echo pin to go HIGH (start of ultrasonic pulse transmission)
        pulse_start = time.time()
        timeout = pulse_start + 0.04  
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None

        # Wait for echo pin to go LOW (echo received)
        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None

        # Calculate distance from pulse duration
        pulse_duration = pulse_end - pulse_start
        
        # Distance = (Time × Speed of Sound) / 2
        # Speed of sound = 34300 cm/s
        # Divide by 2 because sound travels to object and back
        # 34300 / 2 = 17150
        distance = pulse_duration * 17150  # Result in cm
        
        return round(distance, 2)