import RPi.GPIO as GPIO
import time

# 핀 번호 설정 (기존 코드 기준)
SERVO_PIN_TILT = 6  # 상하 제어 (기존 servoPin2)
SERVO_PIN_PAN = 7   # 좌우 제어 (기존 servoPin3)

# 현재 각도 저장 변수 (초기값 90도)
current_tilt = 90
current_pan = 90

def init():
    """서보 모터 초기 설정"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN_TILT, GPIO.OUT)
    GPIO.setup(SERVO_PIN_PAN, GPIO.OUT)
    print("Camera Servo Initialized")

def send_servo_pulse(pin, angle):
    """특정 핀에 각도 신호를 보냄 (기존 servoPulse 로직)"""
    # 각도 제한 (0~180도)
    angle = max(0, min(180, angle))
    
    # 펄스 폭 계산
    pulsewidth = (angle * 11) + 500
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(pulsewidth / 1000000.0)
    GPIO.output(pin, GPIO.LOW)
    # 서보 모터 안정화를 위한 주기 대기 (20ms 주기)
    time.sleep(20.0 / 1000 - pulsewidth / 1000000.0)

def cam_up():
    global current_tilt
    current_tilt -= 2 # 한 번 호출 시 2도씩 이동
    if current_tilt < 0: current_tilt = 0
    send_servo_pulse(SERVO_PIN_TILT, current_tilt)

def cam_down():
    global current_tilt
    current_tilt += 2
    if current_tilt > 180: current_tilt = 180
    send_servo_pulse(SERVO_PIN_TILT, current_tilt)

def cam_left():
    global current_pan
    current_pan += 2
    if current_pan > 180: current_pan = 180
    send_servo_pulse(SERVO_PIN_PAN, current_pan)

def cam_right():
    global current_pan
    current_pan -= 2
    if current_pan < 0: current_pan = 0
    send_servo_pulse(SERVO_PIN_PAN, current_pan)

def cam_center():
    """카메라를 정면(90도, 90도)으로 복귀"""
    global current_tilt, current_pan
    current_tilt = 90
    current_pan = 90
    send_servo_pulse(SERVO_PIN_TILT, current_tilt)
    send_servo_pulse(SERVO_PIN_PAN, current_pan)