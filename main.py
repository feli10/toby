import RPi.GPIO as GPIO
import time
import config
import signal
import sys
from motor import MotorDriver
from sensors import UltrasonicSensor
from control.navigation import Navigator

class Toby:
    """Main robot controller class integrating motors, sensors, and navigation."""
    
    def __init__(self):
        """Initialize Toby with motors, sensors, and navigation system."""
        GPIO.setmode(GPIO.BCM)
        self.motor = MotorDriver()
        self.sensor_red = UltrasonicSensor(config.SENSOR_RED_TRIG, config.SENSOR_RED_ECHO, "Sensor Red (Left)")
        self.sensor_blue = UltrasonicSensor(config.SENSOR_BLUE_TRIG, config.SENSOR_BLUE_ECHO, "Sensor Blue (Right)")
        self.navigator = Navigator(self.motor, self.sensor_red, self.sensor_blue)
        
        # Flag to control main loop execution
        self.running = True

        # Register signal handler for graceful shutdown (Ctrl+C)
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, sig, frame):
        """Gracefully stop motors and cleanup GPIO."""
        print("\nStopping safely...")
        
        self.running = False
        self.motor.stop_all()
        self.motor.cleanup()
        GPIO.cleanup()
        sys.exit(0)

    def run(self):
        """
        Run with simple obstacle avoidance (no destination).
        In this mode, Toby wanders freely while avoiding obstacles.
        """
        print("Starting autonomous navigation mode...")
        print("Toby will wander and avoid obstacles.")
        
        # Main navigation loop - runs until stopped
        while self.running:
            # Execute one navigation step (check sensors, avoid obstacles, move)
            self.navigator.navigate_step()
    
    def run_with_destination(self, x, y, timeout=60):
        """Run navigation with a specific destination."""
        print(f"Starting navigation to destination: ({x}, {y}) cm")
        
        self.navigator.set_destination(x, y)

        success = self.navigator.navigate_to_destination(timeout)
        
        # Report result
        if success:
            print("Successfully reached destination!")
        else:
            print("Failed to reach destination within timeout.")
        
        return success


if __name__ == "__main__":
    # Create Toby instance
    toby = Toby()
    
    # Option 1: Wander mode (no destination)
    # toby.run()
    
    # Option 2: Navigate to a specific destination
    # Coordinates are relative to starting position:
    # - x: positive = right, negative = left
    # - y: positive = forward, negative = backward
    # Destination is 100cm forward (y) and 50cm right (x)
    toby.run_with_destination(50, 100, timeout=120)