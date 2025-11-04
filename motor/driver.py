# motor/driver.py
import RPi.GPIO as GPIO
import config

class MotorDriver:
    def __init__(self):
        # Setup motor pins
        GPIO.setup(config.MOTOR_A_IN1, GPIO.OUT)
        GPIO.setup(config.MOTOR_A_IN2, GPIO.OUT)
        GPIO.setup(config.MOTOR_A_EN, GPIO.OUT)

        GPIO.setup(config.MOTOR_B_IN1, GPIO.OUT)
        GPIO.setup(config.MOTOR_B_IN2, GPIO.OUT)
        GPIO.setup(config.MOTOR_B_EN, GPIO.OUT)

        # Create PWM instances
        self.pwm_a = GPIO.PWM(config.MOTOR_A_EN, config.PWM_FREQ)
        self.pwm_b = GPIO.PWM(config.MOTOR_B_EN, config.PWM_FREQ)

        self.pwm_a.start(0)
        self.pwm_b.start(0)

    def set_speed(self, motor, speed):
        """
        motor: 'A' or 'B'
        speed: -100 to +100 (% of power)
        Positive = forward, Negative = reverse
        """
        if motor == 'A':
            in1, in2, pwm = config.MOTOR_A_IN1, config.MOTOR_A_IN2, self.pwm_a
        elif motor == 'B':
            in1, in2, pwm = config.MOTOR_B_IN1, config.MOTOR_B_IN2, self.pwm_b
        else:
            raise ValueError("Motor must be 'A' or 'B'")

        # Limit speed range
        speed = max(-100, min(100, speed))

        if speed > 0:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        else:
            # Stop motor (coast)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)

        pwm.ChangeDutyCycle(abs(speed))

    def stop_all(self):
        """Stop both motors."""
        self.set_speed('A', 0)
        self.set_speed('B', 0)

    def cleanup(self):
        """Stop PWM and cleanup pins."""
        self.stop_all()
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()