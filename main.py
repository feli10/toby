# main.py
import RPi.GPIO as GPIO
import time
import config
from motor import MotorDriver
from sensors import UltrasonicSensor

def main():
    GPIO.setmode(GPIO.BCM)
    motor = MotorDriver()

    # Initialize sensors
    sensor_red = UltrasonicSensor(config.SENSOR_RED_TRIG, config.SENSOR_RED_ECHO, "Sensor Red (Front)")
    sensor_blue = UltrasonicSensor(config.SENSOR_BLUE_TRIG, config.SENSOR_BLUE_ECHO, "Sensor Blue (Rear)")

    try:
        while True:
            # Get distances
            dist_front = sensor_red.get_distance()
            dist_back = sensor_blue.get_distance()

            # Show readings
            print(f"Front: {dist_front} cm | Rear: {dist_back} cm")

            # --- Simple avoidance logic ---
            if (dist_front and dist_front < config.SAFE_FRONT_DISTANCE) and (dist_back and dist_back < config.SAFE_BACK_DISTANCE):
                print("Stuck! Stopping...")
                motor.stop_all()
                time.sleep(0.2)

            elif dist_front and dist_front < config.SAFE_FRONT_DISTANCE:
                print("Object ahead! Reversing...")
                motor.set_speed('A', -60)
                motor.set_speed('B', -60)
                time.sleep(0.6)
                motor.stop_all()
                time.sleep(0.2)

            elif dist_back and dist_back < config.SAFE_BACK_DISTANCE:
                print("Object behind! Moving forward...")
                motor.set_speed('A', 60)
                motor.set_speed('B', 60)
                time.sleep(0.6)
                motor.stop_all()
                time.sleep(0.2)

            else:
                print("Path clear. Moving forward...")
                motor.set_speed('A', 60)
                motor.set_speed('B', 60)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        motor.cleanup()

if __name__ == "__main__":
    main()