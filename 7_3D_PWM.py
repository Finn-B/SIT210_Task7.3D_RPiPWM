import RPi.GPIO as GPIO
import time

# USE GPIO NUMBERS NOT PIN NUMBERS
GPIO.setmode(GPIO.BCM)

# PIN DEFINITION
led = 18
trig = 23
echo = 24

# VARIABLES
Range_in_cm = 35
distance_cutoff = 10


# FUNCTIONS
def calc_pwm(n, n2, n3):
    pwm = 100 - (0 + ((100 - 0) / (n2 - 10)) * (n - n3))
    if (pwm <= 0):
        pwm = 0
    if (pwm >= 100):
        pwm = 100
    return pwm


# GPIO SETUP
GPIO.setup(trig, GPIO.OUT)
GPIO.output(trig, GPIO.LOW)

GPIO.setup(echo, GPIO.IN)

GPIO.setup(led, GPIO.OUT)
pwm = GPIO.PWM(led, 100)

time.sleep(2)


# MAIN LOOP
duty_cycle = 0
pwm.start(duty_cycle)
try:
    while 1:
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = round((pulse_duration * 17150), 2)
        duty_cycle = int(calc_pwm(distance, Range_in_cm, distance_cutoff))
        pwm.start(duty_cycle)

        print("-----------")
        print("Duty Cycle: ", duty_cycle, " %")
        print("Distance: ", distance, "cm")
        print("-----------")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
