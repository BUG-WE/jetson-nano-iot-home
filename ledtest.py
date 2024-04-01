import time
import random
import RPi.GPIO as GPIO

LED_COUNT = 5        # LED灯的个数
LED_PIN = 12          # DI端接GPIO12

# 初始化RPi GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

# # 设置PWM频率和占空比
# pwm_frequency = 1000  # PWM频率
# duty_cycle = 0.5      # 占空比
#
# # 创建PWM对象
# pwm = GPIO.PWM(LED_PIN, pwm_frequency)

# 改变所有LED灯的亮度
def change_brightness(duty_cycle, wait_ms=20):
    pwm.ChangeDutyCycle(duty_cycle * 100)
    time.sleep(wait_ms / 1000.0)

# 随机点亮一个灯
def random_lights():
    for i in range(10):
        num = random.randint(0, LED_COUNT - 1)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        pwm.start(0)
        pwm.ChangeDutyCycle(0)
        pwm.ChangeFrequency(pwm_frequency)
        pwm.ChangeDutyCycle(duty_cycle * 100)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)

# 流水灯
def water_lights(color):
    count = 0
    while True:
        for i in range(LED_COUNT):
            pwm.start(0)
            pwm.ChangeDutyCycle(0)
            pwm.ChangeFrequency(pwm_frequency)
            pwm.ChangeDutyCycle(duty_cycle * 100)
            time.sleep(0.1)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.5)
        count += 1
        if count >= 5:
            pwm.ChangeDutyCycle(0)
            break

# # 呼吸灯
# def breathing(color):
#     pwm.start(0)
#     pwm.ChangeDutyCycle(0)
#     pwm.ChangeFrequency(pwm_frequency)
#     pwm.ChangeDutyCycle(duty_cycle * 100)
#     time.sleep(1)
#     brightness = 0
#     increment = 0.01
#     count = 0
#     while True:
#         brightness += increment
#         pwm.ChangeDutyCycle(brightness * 100)
#         time.sleep(0.01)
#         if brightness <= 0 or brightness >= duty_cycle:
#             increment = -increment
#             count += 1
#         if count == 7:
#             pwm.ChangeDutyCycle(0)
#             break

try:
    random_lights()
    water_lights((0, 1, 0))
    breathing((0, 1, 1))
except:
    pass

# 清理GPIO引脚
# pwm.stop()
GPIO.cleanup()
