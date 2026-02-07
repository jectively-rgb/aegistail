#!/usr/bin/python
import cv2
import numpy
import socket
import time
import struct
from scapy.all import *

# 전송 대상(조종기/휴대폰)의 IP 주소와 패킷 크기를 저장할 변수
IPData = [0, 1] 

def Echo(packet):
    """
    ICMP(Ping) 패킷을 감지했을 때 실행되는 콜백 함수
    상대방이 나에게 Ping을 보내면 그 소스 IP를 자동으로 추출함
    """
    IP = (packet['IP'].src)       # 패킷을 보낸 기기의 IP 주소
    Bigx = len(packet[Raw])       # 데이터 길이를 확인 (필요시 특정 기기 식별용)
    global IPData
    IPData[0] = IP
    IPData[1] = Bigx
    print ("source IP:", IPData[0])
    print("Packet size：", IPData[1])

def Stop(packet):
    """
    sniff(패킷 감지)를 언제 멈출지 결정하는 함수
    True를 반환하면 IP를 찾은 즉시 감지를 중단함
    """
    return True

# --- [단계 1] 상대방 IP 자동 찾기 ---
# 상대방 IP를 아직 모르거나 특정 기본값일 때 루프 실행
while(IPData[0] == 0) or (IPData[0] == '10.0.0.1'):
    print("wait..")
    # 무선 랜(wlan0)에서 ICMP-Echo(Ping) 신호가 올 때까지 대기(Sniffing)
    sniff(iface="wlan0", filter="icmp[icmptype] = icmp-echo", count=0, prn=Echo, stop_filter=Stop)
    print("IP = ", IPData[0])

print ("Found Source IP:", IPData[0])
HOST = IPData[0]  # 찾은 IP를 목적지 호스트로 설정
PORT = 5051       # 전송 포트 (MainControl과 동일)
WIDTH = 320       # 프레임 너비
HEIGHT = 240      # 프레임 높이

# --- [단계 2] 영상 전송 설정 ---
# UDP 소켓 생성 (실시간 전송을 위해 신뢰성보다 속도가 빠른 UDP 사용)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # 브로드캐스트 허용
server.connect((HOST, PORT))

print('now starting to send frames...')

# 카메라 캡처 장치 준비 (0번 카메라)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

try:
    while True:
        try:
            time.sleep(0.01) # 전송 부하를 줄이기 위한 미세 지연
            success, frame = capture.read()
            
            if success and frame is not None:
                # 프레임을 JPEG 포맷으로 압축 (95% 품질)
                # 원본 이미지는 용량이 너무 커서 네트워크 전송이 불가능하기 때문
                result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                
                # 시리얼라이즈된 데이터를 전송
                server.sendall(imgencode)
                
        except Exception as e:
            print(f"Frame Error: {e}")
            continue
except Exception as e:
    # 에러 발생 시 종료 신호를 보내고 자원 해제
    server.sendall(struct.pack('b', 1))
    print(f"Global Error: {e}")
    capture.release()
    server.close()