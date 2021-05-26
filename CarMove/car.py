from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSql
import atexit
import time

import RPi.GPIO as GPIO
from sense_hat import SenseHat
import picamera
import datetime

class pollingThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName("13.209.64.111")
        db.setDatabaseName("IoT_data")
        db.setUserName("ujin")
        db.setPassword("ujin")
        ok = db.open()
        print(ok)

        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.myMotor.setSpeed(100)
        self.speed_value = 100

        self.pwm=PWM(0x6F)
        self.pwm.setPWMFreq(60)

        #self.sense=SenseHat()

        self.BUZZER = 5
        self.RIGHT_LED_F = 23
        self.LEFT_LED_F = 24
        self.RIGHT_LED_R = 8
        self.LEFT_LED_R = 7
        self.ECHO = 21
        self.TRIG = 20

        self.timeF = 0
        self.camera = picamera.PiCamera()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.BUZZER, GPIO.OUT)
        GPIO.setup(self.RIGHT_LED_F, GPIO.OUT)
        GPIO.setup(self.LEFT_LED_F, GPIO.OUT)
        GPIO.setup(self.RIGHT_LED_R, GPIO.OUT)
        GPIO.setup(self.LEFT_LED_R, GPIO.OUT)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        while True:
            if (self.timeF == 10):
                now = datetime.datetime.now()
                self.camera.capture('./img/' + now.strftime('%Y%m%d%H%M%S') + '.jpg')
                self.timeF = 0
            time.sleep(0.1)
            self.getQuery()
            # self.setQuery()
            self.timeF += 1

    def setQuery(self):
        GPIO.output(self.TRIG, True)

        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(self.ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(self.ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        print(distance)
        '''
        # pressure = self.sense.get_pressure()
        # temp = self.sense.get_temperature()
        # humidity = self.sense.get_humidity()

        # p = round((pressure - 1000) / 100, 3)
        # t = round(temp / 100, 3)
        # h = round(humidity / 100, 3)

        self.query = QtSql.QSqlQuery()
        self.query.prepare("insert into sensing (time, num1, num2, num3, meta_string, is_finish) values (:time, :num1, :num2, :num3, :meta, :finish)")
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time", time)
        self.query.bindValue(":num1", self.sensor.distance)
        self.query.bindValue(":num2", "")
        self.query.bindValue(":num3", "")
        self.query.bindValue(":meta", "")
        self.query.bindValue(":finish", 0)
        self.query.exec()

        # a = int((p * 1271) % 256)
        # b = int((t * 1271) % 256)
        # c = int((h * 1271) % 256)
        # self.sense.clear(a,b,c)
        '''

    def getQuery(self):
        query = QtSql.QSqlQuery("select * from command order by time desc limit 1")
        query.next()

        cmdTime = query.record().value(0)
        cmdType = query.record().value(1)
        cmdArg = query.record().value(2)
        is_finish = query.record().value(3)

        if is_finish == 0:
            query = QtSql.QSqlQuery("update command set is_finish=1 where is_finish=0");
            if cmdType == "go" : self.go()
            if cmdType == "back" : self.back()
            if cmdType == "left" : self.left()
            if cmdType == "right" : self.right()
            if cmdType == "mid" : self.mid()
            if cmdType == "stop" : self.stop()
            if cmdType == "speed" : 
                self.speed_value = int(cmdArg)
                self.speed()
            if cmdType == "buzz" : self.buzz()

    def buzz(self):
        GPIO.output(self.BUZZER, True)
        time.sleep(0.5)
        GPIO.output(self.BUZZER, False) 

    def speed(self):
        print("MOTOR SPEED SET")
        self.myMotor.setSpeed(self.speed_value)

    def go(self):
        print("MOTOR GO")
        self.myMotor.setSpeed(self.speed_value)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)

    def back(self):
        print("MOTOR BACK")
        self.myMotor.setSpeed(self.speed_value)
        self.myMotor.run(Raspi_MotorHAT.BACKWARD)

    def stop(self):
        print("MOTOR STOP")
        self.myMotor.run(Raspi_MotorHAT.RELEASE)

    def left(self):
        print("MOTOR LEFT")
        self.pwm.setPWM(0, 0, 230)
        GPIO.output(self.LEFT_LED_F, True)
        GPIO.output(self.RIGHT_LED_F, False)
        GPIO.output(self.LEFT_LED_R, True)
        GPIO.output(self.RIGHT_LED_R, False)

    def mid(self):
        print("MOTOR MID")
        self.pwm.setPWM(0, 0, 325)
        GPIO.output(self.LEFT_LED_F, False)
        GPIO.output(self.RIGHT_LED_F, False)
        GPIO.output(self.LEFT_LED_R, False)
        GPIO.output(self.RIGHT_LED_R, False)

    def right(self):
        print("MOTOR RIGHT")
        self.pwm.setPWM(0, 0, 390)
        GPIO.output(self.LEFT_LED_F, False)
        GPIO.output(self.RIGHT_LED_F, True)
        GPIO.output(self.LEFT_LED_R, False)
        GPIO.output(self.RIGHT_LED_R, True)

th = pollingThread()
th.start()

app = QApplication([])

while True:
    pass
