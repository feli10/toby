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
        self.motor = MotorDriver()
        self.sensor_red = UltrasonicSensor(config.SENSOR_RED_TRIG, config.SENSOR_RED_ECHO, "Sensor Red (Front)")
        self.sensor_blue = UltrasonicSensor(config.SENSOR_BLUE_TRIG, config.SENSOR_BLUE_ECHO, "Sensor Blue (Rear)")
        self.running = True

        # Register signal handler
        signal.signal(signal.SIGINT, self.handle_exit)

        GPIO.setmode(GPIO.BCM)

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
            dist_front = self.sensor_red.get_distance()
            dist_back = self.sensor_blue.get_distance()

            print(f"Front: {dist_front} cm | Rear: {dist_back} cm")

            # --- Simple avoidance logic ---
            if (dist_front and dist_front < config.SAFE_FRONT_DISTANCE) and (dist_back and dist_back < config.SAFE_BACK_DISTANCE):
                print("Stuck! Stopping...")
                self.motor.stop_all()
                time.sleep(0.2)

            elif dist_front and dist_front < config.SAFE_FRONT_DISTANCE:
                print("Object ahead! Reversing...")
                self.motor.set_speed('A', -config.DRIVE_SPEED)
                self.motor.set_speed('B', -config.DRIVE_SPEED)
                time.sleep(0.6)
                self.motor.stop_all()
                time.sleep(0.2)

            elif dist_back and dist_back < config.SAFE_BACK_DISTANCE:
                print("Object behind! Moving forward...")
                self.motor.set_speed('A', config.DRIVE_SPEED)
                self.motor.set_speed('B', config.DRIVE_SPEED)
                time.sleep(0.6)
                self.motor.stop_all()
                time.sleep(0.2)

            else:
                print("Path clear. Moving forward...")
                self.motor.set_speed('A', config.DRIVE_SPEED)
                self.motor.set_speed('B', config.DRIVE_SPEED)

            time.sleep(0.1)


if __name__ == "__main__":
    toby = Toby()
    toby.run()