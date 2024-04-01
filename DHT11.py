import time
import Jetson.GPIO as GPIO


def precise_delay(duration):
    my_time = time.perf_counter()
    while (time.perf_counter() - my_time) < duration:
        pass


class DHT11:
    def __init__(self, pin):
        self.DHT_PIN = pin
        self.data = []

    def read_data(self):
        GPIO.setmode(GPIO.BOARD)
        # 设置为输出模式
        GPIO.setup(self.DHT_PIN, GPIO.OUT)
        # 发送起始信号
        GPIO.output(self.DHT_PIN, GPIO.LOW)
        precise_delay(0.02)
        GPIO.output(self.DHT_PIN, GPIO.HIGH)
        # 设置为输入模式
        GPIO.setup(self.DHT_PIN, GPIO.IN)

        # 等待低电平结束
        start_time = time.time()
        while GPIO.input(self.DHT_PIN) == GPIO.LOW:
            if time.time() - start_time > 0.1:
                print("等待低电平结束超时")
                break

        # 等待高电平结束
        start_time = time.time()
        while GPIO.input(self.DHT_PIN) == GPIO.HIGH:
            if time.time() - start_time > 0.1:
                print("等待高电平结束超时")
                break

        # 接收数据
        self.data = []
        for i in range(40):
            # 等待数据位的高电平开始
            start_time = time.time()
            while GPIO.input(self.DHT_PIN) == GPIO.LOW:
                if time.time() - start_time > 0.1:
                    print("等待数据位高电平开始超时")
                    break

            # 等待数据位的高电平结束
            end_time = time.time()
            while GPIO.input(self.DHT_PIN) == GPIO.HIGH:
                if time.time() - start_time > 0.1:
                    print("等待数据位高电平结束超时")
                    break

            # 将数据位的高电平持续时间转换为数据值
            if time.time() - end_time > 0.00005:  # 判断高电平持续时间是否超过50微秒
                self.data.append(1)
            else:
                self.data.append(0)

        # 根据dht11的信号原理获取所需的值（下同理）
        humidityHigh_Bit = self.data[0:8]  # 湿度高 8 位
        humidityLow_Bit = self.data[8:16]  # 湿度低 8 位
        temperatureHigh_Bit = self.data[16:24]  # 温度高 8 位
        temperatureLow_Bit = self.data[24:32]  # 温度低 8 位
        checkBit = self.data[32:40]  # 校验位
        humidityHigh = 0
        humidityLow = 0
        temperatureHigh = 0
        temperatureLow = 0
        check = 0
        # 将二进制数转换为十进制数
        for i in range(0, 8):
            humidityHigh += humidityHigh_Bit[i] * (2 ** (7 - i))
            humidityLow += humidityLow_Bit[i] * (2 ** (7 - i))
            temperatureHigh += temperatureHigh_Bit[i] * (2 ** (7 - i))
            temperatureLow += temperatureLow_Bit[i] * (2 ** (7 - i))
            check += checkBit[i] * (2 ** (7 - i))
        # 获取温度值
        temperature = temperatureHigh + temperatureLow * 0.1
        # 获取湿度度值
        humidity = humidityHigh + humidityLow * 0.1
        checkNum = temperatureHigh + humidityHigh + temperatureLow + humidityLow  # 计算前32位数的值

        if checkNum != check:  # 检查前32位的值是否与校验位相等
            print("temperature, humidity")  # 相等输出温度和湿度
            print(temperature)  # 相等输出温度和湿度
            print(humidity)  # 相等输出温度和湿度
            print("Temperature is ", temperature, "C\nHumidity is ", humidity, "%")  # 打印温湿度数据
            GPIO.cleanup()
            return temperature, humidity
        else:
            print("dht11 check was wrong")
            GPIO.cleanup()
            return None, None


if __name__ == '__main__':
    dht_sensor = DHT11(36)
    temperature, humidity = dht_sensor.read_data()
    print("Temperature is ", temperature, "C\nHumidity is ", humidity, "%")  # 打印温湿度数据

