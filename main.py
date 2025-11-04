# main.py
import RPi.GPIO as GPIO
import time
from motor import MotorDriver

def main():
    GPIO.setmode(GPIO.BCM)
    motor = MotorDriver()

    try:
        print("Forward...")
        motor.set_speed('A', 60)
        motor.set_speed('B', 60)
        time.sleep(2)

        print("Reverse...")
        motor.set_speed('A', -60)
        motor.set_speed('B', -60)
        time.sleep(2)

        print("Turn left...")
        motor.set_speed('A', 50)
        motor.set_speed('B', -50)
        time.sleep(1)

        print("Turn right...")
        motor.set_speed('A', -50)
        motor.set_speed('B', 50)
        time.sleep(1)

        print("Stop.")
        motor.stop_all()
        time.sleep(1)

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        motor.cleanup()

if __name__ == "__main__":
    main()