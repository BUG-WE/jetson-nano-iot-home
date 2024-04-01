import time
import Jetson.GPIO as GPIO

# 设置GPIO引脚
DHT_PIN = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DHT_PIN, GPIO.IN)


def read_dht11_data():
    data = []
    # 发送开始信号
    GPIO.setup(DHT_PIN, GPIO.OUT)
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(DHT_PIN, GPIO.HIGH)
    GPIO.setup(DHT_PIN, GPIO.IN)

    # 等待DHT11响应
    timeout = 10000
    while GPIO.input(DHT_PIN) == GPIO.LOW:
        timeout -= 1
        if timeout <= 0:
            return None
    timeout = 10000
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        timeout -= 1
        if timeout <= 0:
            return None

    # 读取数据
    bits = []
    bit_count = 0
    prev_state = GPIO.HIGH
    timeout = 10000
    while True:
        current_state = GPIO.input(DHT_PIN)
        timeout -= 1
        if timeout <= 0:
            return None
        if prev_state == GPIO.HIGH and current_state == GPIO.LOW:
            bit_count += 1
            if bit_count > 3:
                break
        if prev_state != current_state:
            bits.append(timeout)
        prev_state = current_state

    # 解析数据
    for i in range(0, len(bits), 2):
        if bits[i] < bits[i + 1]:
            data.append(0)
        else:
            data.append(1)

    return data


# 读取温湿度数据
data = read_dht11_data()
if data is not None and len(data) == 40:
    humidity = data[0] * 10 + data[1]
    temperature = data[2] * 10 + data[3]
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
else:
    print("Failed to retrieve data from DHT11 sensor.")

# 清理GPIO设置
GPIO.cleanup()
