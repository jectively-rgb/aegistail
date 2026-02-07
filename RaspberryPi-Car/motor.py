# motor.py
import RPi.GPIO as GPIO
import time

# 핀 번호 설정 (기존 코드 그대로 유지)
L_IN1, L_IN2, L_PWM1 = 20, 21, 0
L_IN3, L_IN4, L_PWM2 = 22, 23, 1
R_IN1, R_IN2, R_PWM1 = 24, 25, 12
R_IN3, R_IN4, R_PWM2 = 26, 27, 13

# PWM 객체 변수 (초기화 전)
pwm_L1 = pwm_L2 = pwm_R1 = pwm_R2 = None

def init():
    """모터 제어를 위한 초기 설정 함수"""
    global pwm_L1, pwm_L2, pwm_R1, pwm_R2
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # 모든 핀을 출력(OUT)으로 설정
    pins = [L_IN1, L_IN2, L_PWM1, L_IN3, L_IN4, L_PWM2, 
            R_IN1, R_IN2, R_PWM1, R_IN3, R_IN4, R_PWM2]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    # PWM 시작 (주파수 100Hz)
    pwm_L1 = GPIO.PWM(L_PWM1, 100)
    pwm_L2 = GPIO.PWM(L_PWM2, 100)
    pwm_R1 = GPIO.PWM(R_PWM1, 100)
    pwm_R2 = GPIO.PWM(R_PWM2, 100)
    
    pwm_L1.start(0)
    pwm_L2.start(0)
    pwm_R1.start(0)
    pwm_R2.start(0)

def ahead(speed=80):
    GPIO.output(L_IN1, GPIO.LOW); GPIO.output(L_IN2, GPIO.HIGH)
    pwm_L1.ChangeDutyCycle(speed)
    # ... (나머지 L_IN3, R_IN1, R_IN3 로직들 복사)
    print("Moving Ahead")

def stop():
    pwm_L1.ChangeDutyCycle(0)
    pwm_L2.ChangeDutyCycle(0)
    pwm_R1.ChangeDutyCycle(0)
    pwm_R2.ChangeDutyCycle(0)
    print("Stopped")

def cleanup():
    GPIO.cleanup()