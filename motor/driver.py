import RPi.GPIO as GPIO
import config

class MotorDriver:
    """Controls two DC motors (A and B) with PWM speed control and direction."""
    
    def __init__(self):
        """Initialize motor driver and configure GPIO pins for PWM control."""
        # Setup Motor A Pins
        GPIO.setup(config.MOTOR_A_IN1, GPIO.OUT)
        GPIO.setup(config.MOTOR_A_IN2, GPIO.OUT)
        GPIO.setup(config.MOTOR_A_EN, GPIO.OUT)  

        # Setup Motor B Pins
        GPIO.setup(config.MOTOR_B_IN1, GPIO.OUT)
        GPIO.setup(config.MOTOR_B_IN2, GPIO.OUT)
        GPIO.setup(config.MOTOR_B_EN, GPIO.OUT)  

        # Create PWM instances for speed control
        self.pwm_a = GPIO.PWM(config.MOTOR_A_EN, config.PWM_FREQ)
        self.pwm_b = GPIO.PWM(config.MOTOR_B_EN, config.PWM_FREQ)

        # Start PWM with 0% duty cycle (motors stopped)
        self.pwm_a.start(0)
        self.pwm_b.start(0)

    def set_speed(self, motor, speed):
        """Set motor speed and direction."""
        # Select the appropriate pins based on motor selection
        if motor == 'A':
            in1, in2, pwm = config.MOTOR_A_IN1, config.MOTOR_A_IN2, self.pwm_a
        elif motor == 'B':
            in1, in2, pwm = config.MOTOR_B_IN1, config.MOTOR_B_IN2, self.pwm_b
        else:
            raise ValueError("Motor must be 'A' or 'B'")

        # Clamp speed to valid range [-100, 100]
        speed = max(-100, min(100, speed))

        # Set direction pins based on speed sign
        if speed > 0:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)

        # Set PWM duty cycle (speed magnitude)
        pwm.ChangeDutyCycle(abs(speed))

    def stop_all(self):
        """Stop both motors immediately by setting speed to 0."""
        self.set_speed('A', 0)
        self.set_speed('B', 0)

    def cleanup(self):
        """Stop PWM signals and cleanup GPIO resources."""

        self.stop_all()

        self.pwm_a.stop()
        self.pwm_b.stop()

        GPIO.cleanup()