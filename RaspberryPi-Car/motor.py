import RPi.GPIO as GPIO

# 핀 설정 (제공해주신 기존 코드 기준)
L_IN1, L_IN2, L_PWM1 = 20, 21, 0
L_IN3, L_IN4, L_PWM2 = 22, 23, 1
R_IN1, R_IN2, R_PWM1 = 24, 25, 12
R_IN3, R_IN4, R_PWM2 = 26, 27, 13

# PWM 객체를 저장할 전역 변수
pwm_list = []

def init():
    global pwm_list
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # 모든 핀을 출력(OUTPUT) 모드로 설정
    pins = [L_IN1, L_IN2, L_PWM1, L_IN3, L_IN4, L_PWM2, 
            R_IN1, R_IN2, R_PWM1, R_IN3, R_IN4, R_PWM2]
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW) # 초기값은 모두 LOW

    # PWM 설정 (100Hz)
    pwm_L1 = GPIO.PWM(L_PWM1, 100)
    pwm_L2 = GPIO.PWM(L_PWM2, 100)
    pwm_R1 = GPIO.PWM(R_PWM1, 100)
    pwm_R2 = GPIO.PWM(R_PWM2, 100)
    
    pwm_list = [pwm_L1, pwm_L2, pwm_R1, pwm_R2]
    
    # 속도 0으로 시작
    for p in pwm_list:
        p.start(0)

def set_speed(speed):
    """모든 모터의 속도(Duty Cycle)를 한 번에 조절"""
    for p in pwm_list:
        p.ChangeDutyCycle(speed)

def ahead():
    """전진 (기존 코드의 ahead 로직)"""
    # 왼쪽 바퀴들
    GPIO.output(L_IN1, GPIO.LOW);  GPIO.output(L_IN2, GPIO.HIGH)
    GPIO.output(L_IN3, GPIO.HIGH); GPIO.output(L_IN4, GPIO.LOW)
    # 오른쪽 바퀴들
    GPIO.output(R_IN1, GPIO.HIGH); GPIO.output(R_IN2, GPIO.LOW)
    GPIO.output(R_IN3, GPIO.LOW);  GPIO.output(R_IN4, GPIO.HIGH)
    set_speed(80)

def back():
    """후진 (기존 코드의 rear 로직)"""
    # 왼쪽 바퀴들 역전
    GPIO.output(L_IN1, GPIO.HIGH); GPIO.output(L_IN2, GPIO.LOW)
    GPIO.output(L_IN3, GPIO.LOW);  GPIO.output(L_IN4, GPIO.HIGH)
    # 오른쪽 바퀴들 역전
    GPIO.output(R_IN1, GPIO.LOW);  GPIO.output(R_IN2, GPIO.HIGH)
    GPIO.output(R_IN3, GPIO.HIGH); GPIO.output(R_IN4, GPIO.LOW)
    set_speed(80)

def left():
    """좌회전 (기존 코드의 left 로직)"""
    GPIO.output(L_IN1, GPIO.HIGH); GPIO.output(L_IN2, GPIO.LOW)
    GPIO.output(L_IN3, GPIO.LOW);  GPIO.output(L_IN4, GPIO.HIGH)
    GPIO.output(R_IN1, GPIO.HIGH); GPIO.output(R_IN2, GPIO.LOW)
    GPIO.output(R_IN3, GPIO.LOW);  GPIO.output(R_IN4, GPIO.HIGH)
    set_speed(80)

def right():
    """우회전 (기존 코드의 right 로직)"""
    GPIO.output(L_IN1, GPIO.LOW);  GPIO.output(L_IN2, GPIO.HIGH)
    GPIO.output(L_IN3, GPIO.HIGH); GPIO.output(L_IN4, GPIO.LOW)
    GPIO.output(R_IN1, GPIO.LOW);  GPIO.output(R_IN2, GPIO.HIGH)
    GPIO.output(R_IN3, GPIO.HIGH); GPIO.output(R_IN4, GPIO.LOW)
    set_speed(80)

def stop():
    """모든 모터 정지"""
    set_speed(0)

def cleanup():
    """프로그램 종료 시 호출하여 GPIO 초기화"""
    stop()
    for p in pwm_list:
        p.stop()
    GPIO.cleanup()