import RPi.GPIO as GPIO
import subprocess
import time
import signal
import config

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

process = None   # Will hold the subprocess
running = False  # Keeps track of state

print("Button launcher ready. Press the button to start/stop the main script.")

try:
    while True:
        if GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:
            time.sleep(0.05)  # Debounce delay
            if GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:  # still pressed
                if not running:
                    print("Starting main script...")
                    process = subprocess.Popen(["python3", config.SCRIPT_PATH])
                    running = True
                else:
                    print("Stopping main script...")
                    process.send_signal(signal.SIGINT)  # Graceful stop
                    process.wait()
                    process = None
                    running = False

                # Wait for button release
                while GPIO.input(config.BUTTON_PIN) == GPIO.HIGH:
                    time.sleep(0.05)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    if process and running:
        process.send_signal(signal.SIGINT)
        process.wait()
finally:
    GPIO.cleanup()