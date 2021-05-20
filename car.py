# -*- coding: utf-8 -*-
'''
- Raspberry pi 4 model B 를 컨트롤러로 사용하여 ssh로 연결된 호스트컴퓨터(pc)에서 콘솔에 명령어를 입력함으로써 차량을 제어할 수 있다.
- 구현해야할 기본 명령은 '앞으로/ 뒤로/ 정지/ 빠르게/ 느리게/ 오른쪽/ 왼쪽/ 중앙' 이다.
- wifi통해 네트워크 연결되도록 한다.
'''

# 모듈 로드
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

# 모터 초기설정
mh = Raspi_MotorHAT(addr = 0x6f)
motor1 = mh.getMotor(2) # M2단자에 모터연결
speed = 125 # 모터 속도 0~255
motor1.setSpeed(speed)

# 서보 초기설정
servo = mh._pwm
servo.setPWMFreq(60)
servoCH = 0 # 서보 연결된 핀
servoMin = 350
servoMax = 450

# 앞으로
def go():
    motor1.run(Raspi_MotorHAT.FORWARD)

# 뒤로
def back():
    motor1.run(Raspi_MotorHAT.BACKWARD)

# 모터 정지
def stop():
    motor1.run(Raspi_MotorHAT.RELEASE)

# 빠르게
def speed_up():
    global speed
    if speed >= 235:
        speed = 255    
    else:
        speed + 20 # 최대 255, 20단위로 증가
    motor1.setSpeed(speed)

# 느리게
def speed_down():
    global speed
    if speed <= 20:
        speed = 0
    else:
        speed - 20 # 최하 0
    motor1.setSpeed(speed)


# 우회전
def steer_right():
    servo.setPWM(0, 0, servoMax)

# 좌회전
def steer_left():
    servo.setPWM(0, 0, servoMin)

# 핸들 중앙
def steer_center():
    servo.setPWM(0, 0, 400)

def main():
    command = ['go', 'back', 'stop', 'fast', 'slow', 'right', 'left', 'center']
    func = [go, back, stop, speed_up, speed_down, steer_right, steer_left, steer_center]

    try:
        while True:
            word = input("명령['go', 'back', 'stop', 'fast', 'slow', 'right', 'left', 'center'] : ")
            if word in command:
                func[command.index(word)]() # word에 해당하는 index의 func 실행

    except KeyboardInterrupt:
        print('\n사용자의 요청으로 종료합니다...')
    except:
        print('\n확인되지 않은 오류입니다...')
    finally:
        motor1.run(Raspi_MotorHAT.RELEASE)
    
if __name__ == '__main__':
    main()
