import RPi.GPIO as GPIO
import time

PAN_PIN = 7   # 좌우
TILT_PIN = 6  # 상하

current_pan = 90
current_tilt = 90

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PAN_PIN, GPIO.OUT)
    GPIO.setup(TILT_PIN, GPIO.OUT)

def set_angle(pin, angle):
    angle = max(0, min(180, angle))
    pulse = (angle * 11) + 500
    GPIO.output(pin, True)
    time.sleep(pulse / 1000000.0)
    GPIO.output(pin, False)
    time.sleep(0.02)

def move_up():
    global current_tilt
    current_tilt = max(0, current_tilt - 10)
    set_angle(TILT_PIN, current_tilt)

def move_down():
    global current_tilt
    current_tilt = min(180, current_tilt + 10)
    set_angle(TILT_PIN, current_tilt)

def move_left():
    global current_pan
    current_pan = min(180, current_pan + 10)
    set_angle(PAN_PIN, current_pan)

def move_right():
    global current_pan
    current_pan = max(0, current_pan - 10)
    set_angle(PAN_PIN, current_pan)

def center():
    global current_pan, current_tilt
    current_pan, current_tilt = 90, 90
    for _ in range(5):
        set_angle(PAN_PIN, 90)
        set_angle(TILT_PIN, 90)