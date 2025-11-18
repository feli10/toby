# main.py
import RPi.GPIO as GPIO
import time
import config
import signal
import sys
from motor import MotorDriver
from sensors import UltrasonicSensor

class Toby:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.motor = MotorDriver()
        self.sensor_red = UltrasonicSensor(config.SENSOR_RED_TRIG, config.SENSOR_RED_ECHO, "Sensor Red (Front)")
        self.sensor_blue = UltrasonicSensor(config.SENSOR_BLUE_TRIG, config.SENSOR_BLUE_ECHO, "Sensor Blue (Rear)")
        self.running = True

        # Register signal handler
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, sig, frame):
        """Gracefully stop motors and cleanup GPIO"""
        print("\nStopping safely...")
        self.running = False
        self.motor.stop_all()
        self.motor.cleanup()
        GPIO.cleanup()
        sys.exit(0)

    def run(self):
        while self.running:
            dist_front_left = self.sensor_red.get_distance()
            dist_front_right = self.sensor_blue.get_distance()

            print(f"Front_Left: {dist_front_left} cm | Front_Right: {dist_front_right} cm")

            # --- Simple avoidance logic ---
            if (dist_front_left and dist_front_left < config.SAFE_FRONT_DISTANCE) and (dist_front_right and dist_front_right < config.SAFE_BACK_DISTANCE):
                print("Stuck! Stopping...")
                self.motor.stop_all()
                time.sleep(0.2)

            elif dist_front_left and dist_front_left < config.SAFE_FRONT_DISTANCE:
                print("Object to the left! Turning right...")
                self.motor.set_speed('A', 0)
                self.motor.set_speed('B', config.TURN_SPEED)
                time.sleep(0.6)
                self.motor.stop_all()
                time.sleep(0.2)

            elif dist_front_right and dist_front_right < config.SAFE_BACK_DISTANCE:
                print("Object to the right! Turning left...")
                self.motor.set_speed('A', 0)
                self.motor.set_speed('B', -config.TURN_SPEED)
                time.sleep(0.6)
                self.motor.stop_all()
                time.sleep(0.2)

            else:
                print("Path clear. Moving forward...")
                self.motor.set_speed('B', 0)
                self.motor.set_speed('A', config.DRIVE_SPEED)

            time.sleep(0.1)


if __name__ == "__main__":
    toby = Toby()
    toby.run()