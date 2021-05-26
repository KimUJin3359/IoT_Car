from Raspi_PWM_Servo_Driver import PWM

pwm = PWM(0x6F)
pwm.setPWMFreq(60)
pwm.setPWM(0, 0, 350)
