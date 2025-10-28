import RPi.GPIO as GPIO
import time

# BCM pin mapping (match the table above)
A_IN1 = 17
A_IN2 = 27
A_EN  = 12  # ENA (PWM) - Motor A speed

B_IN1 = 22
B_IN2 = 16
B_EN  = 13  # ENB (PWM) - Motor B speed

PWM_FREQ = 800  # Hz

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup direction pins
for p in (A_IN1, A_IN2, B_IN1, B_IN2):
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.LOW)

# Setup EN pins for PWM
GPIO.setup(A_EN, GPIO.OUT)
GPIO.setup(B_EN, GPIO.OUT)
pwm_a = GPIO.PWM(A_EN, PWM_FREQ)
pwm_b = GPIO.PWM(B_EN, PWM_FREQ)
pwm_a.start(0)
pwm_b.start(0)

def set_motor_direction(in1, in2, speed):
    """Helper: set direction pins based on signed speed value."""
    if speed > 0:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    elif speed < 0:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    else:
        # both low -> coast / stop (behavior depends on driver; some drivers brake if both HIGH)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)

def motor_a(speed):
    """speed: -100..100"""
    set_motor_direction(A_IN1, A_IN2, speed)
    pwm_a.ChangeDutyCycle(min(abs(speed), 100))

def motor_b(speed):
    """speed: -100..100"""
    set_motor_direction(B_IN1, B_IN2, speed)
    pwm_b.ChangeDutyCycle(min(abs(speed), 100))

try:
    # demo: ramp up A forward and B backward
    for s in range(0, 101, 10):
        motor_a(s)
        motor_b(-s)
        time.sleep(0.3)

    time.sleep(1)
    motor_a(0) #CHANGE THIS
    motor_b(0) #CHANGE THIS

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()