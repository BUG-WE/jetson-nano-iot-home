data = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
        1, 1, 0, 1]

print("接收到的数据:", data)

# 根据dht11的信号原理获取所需的值（下同理）
humidity1bit = data[0:8]  # 湿度高 8 位
humidity2bit = data[8:16]  # 湿度低 8 位
temperature1bit = data[16:24]  # 温度高 8 位
temperature2bit = data[24:32]  # 温度低 8 位
checkBit = data[32:40]  # 校验位
humidity1 = 0
humidity2 = 0
temperature1 = 0
temperature2 = 0
check = 0
for i in range(0, 8):  # 循环8次，将二进制数转换为十进制数
    humidity1 += humidity1bit[i] * (2 ** (7 - i))
    humidity2 += humidity2bit[i] * (2 ** (7 - 1))
    temperature1 += temperature1bit[i] * (2 ** (7 - i))
    temperature2 += temperature2bit[i] * (2 ** (7 - i))
    check += checkBit[i] * (2 ** (7 - i))
temperature = temperature1 + temperature2 * 0.1  # 获取温度值（注意dht11的使用说明中明文写到整数位后是小数位故应乘0.1）
humidity = humidity1 + humidity2 * 0.1  # （网上大部分都没乘0.1，他们的运行结果是整数，足可见网上的帖子都是复制粘着的水文）
checkNum = temperature1 + humidity1 + temperature2 + humidity2  # 计算前32位数的值
if checkNum == check:  # 检查前32位的值是否与校验位相等
    print("temperature,humidity")  # 相等输出温度和湿度
    print(temperature)  # 相等输出温度和湿度
    print(humidity)  # 相等输出温度和湿度
    print("Temperature is ", temperature, "C\nHumidity is ", humidity, "%")  # 打印温湿度数据
else:
    print("dht11 check was wrong")

GPIO.cleanup()

GPIO.cleanup()
