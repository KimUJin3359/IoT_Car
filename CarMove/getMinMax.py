from Raspi_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x6F)
pwm.setPWMFreq(60)

while True:
    value = int(input(' > '))
    if value < 150 or value > 600 : continue
    pwm.setPWM(0, 0, value)
