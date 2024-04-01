import time
import Jetson.GPIO as GPIO

RED_PIN = 21
GREEN_PIN = 19
BLUE_PIN = 22

GPIO.setmode(GPIO.BOARD)
print("设置蓝灯")
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.output(BLUE_PIN, GPIO.HIGH)
i = 0


def blue():
    i = 0
    while i < 100000:
        print("打开蓝灯")
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
        i += 1


def red():
    j = 0
    while j < 500000:
        print("打开蓝灯")
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)
        j += 1


def on_light():
    print("开灯")
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(RED_PIN, GPIO.HIGH)


def out_light():
    print("关灯")
    GPIO.output(BLUE_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)

flag = 0
t = 0
while t < 2:
    if flag == 1:
        red()
        flag = 0
    else:
        blue()
        flag = 1
    t += 1

GPIO.cleanup()
