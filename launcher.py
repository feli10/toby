import RPi.GPIO as GPIO
import subprocess
import time
import signal
import config

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

process = None   # Will hold the subprocess running main.py
running = False  # Tracks whether the main script is currently running

print("Button launcher ready. Press the button to start/stop the main script.")

try:
    # Main button monitoring loop
    while True:
        # Check if button is pressed (pin goes HIGH)
        if GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.05)

            if GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:
                if not running:
                    # Start the main script as a subprocess
                    print("Starting main script...")
                    process = subprocess.Popen(["python3", config.SCRIPT_PATH])
                    running = True
                else:
                    # Stop the running script gracefully
                    print("Stopping main script...")
                    process.send_signal(signal.SIGINT) 
                    process.wait() 
                    process = None
                    running = False

                # Wait for button to be released before accepting next press
                while GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:
                    time.sleep(0.05)

        time.sleep(0.1)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Exiting...")
    if process and running:
        process.send_signal(signal.SIGINT)
        process.wait()
finally:
    # Always clean up GPIO resources on exit
    GPIO.cleanup()