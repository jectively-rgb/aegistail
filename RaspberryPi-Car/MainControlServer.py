from flask import Flask, Response, request
import cv2
import motor
import camera_servo

app = Flask(__name__)

# 초기화
motor.init()
camera_servo.init()
camera_servo.center()

def get_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success: break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control')
def control():
    cmd = request.args.get('cmd')
    if cmd == 'forward': motor.ahead()
    elif cmd == 'back': motor.back()
    elif cmd == 'left': motor.left()
    elif cmd == 'right': motor.right()
    elif cmd == 'stop': motor.stop()
    elif cmd == 'cam_up': camera_servo.move_up()
    elif cmd == 'cam_down': camera_servo.move_down()
    elif cmd == 'cam_left': camera_servo.move_left()
    elif cmd == 'cam_right': camera_servo.move_right()
    return f"OK: {cmd}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)