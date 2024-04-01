import serial

myCOM = "/dev/ttyUSB0"
myBaud = 115200


class AirCondition:
    def __init__(self):
        self.status = False
        self.temperature = 25
        print("初始化空调成功")

    def setStatus(self, key, value):
        self.status = key
        self.temperature = value

    def openAirCondition(self):
        self.status = True
        # 打开串口
        ser = serial.Serial(port=myCOM, baudrate=myBaud)

        # 将十六进制字符串转换为字节对象
        data_bytes = bytes.fromhex(hex_open)

        # 串口发送数据，并输出发送的字节数。
        write_len = ser.write(data_bytes)
        print("串口发出{}个字节。".format(write_len))

        # 关闭串口
        ser.close()

    def closeAirCondition(self):
        self.status = False
        ser = serial.Serial(port=myCOM, baudrate=myBaud)
        data_bytes = bytes.fromhex(hex_close)
        write_len = ser.write(data_bytes)
        print("串口发出{}个字节。".format(write_len))
        ser.close()

    def setTemperature(self, temp):
        if temp > 30:
            print("[错误]温度过高")
        elif temp < 18:
            print("[错误]温度过低")
        else:
            self.status = True
            self.temperature = temp
            ser = serial.Serial(port=myCOM, baudrate=myBaud)
            data_bytes = bytes.fromhex(AirCondition_temperature[temp - 18])
            write_len = ser.write(data_bytes)
            print("串口发出{}个字节。".format(write_len))
            ser.close()

    def getStatus(self):
        if self.status:
            print("当前空调状态为%s,设定的温度是%d" % (self.status, self.temperature))
        else:
            print("空调已关机为%s,上次设定的温度是%d" % (self.status, self.temperature))

    # # 等待接收数据
    # response = ser.read(200)  # 假设要接收 10 个字节的数据
    # print("接收到的数据:", response)# # 等待接收数据
    # # response = ser.read(200)  # 假设要接收 10 个字节的数据
    # # print("接收到的数据:", response)


hex_open = "68 08 00 FF 12 00 11 16"  # 发送第一组数据 [关空调]
hex_close = "68 08 00 FF 12 01 12 16"  # 发送第二组数据 [开空调]
hex_data3 = "68 08 00 FF 12 02 13 16"  # 发送第三组数据
hex_data4 = "68 08 00 FF 12 03 14 16"  # 发送第四组数据
hex_data5 = "68 08 00 FF 12 04 15 16"  # 发送第五组数据
hex_data6 = "68 08 00 FF 12 05 16 16"  # 发送第六组数据
hex_data7 = "68 08 00 FF 12 06 17 16"  # 发送第七组数据

AirCondition_temperature = [
    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 "
    "43 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 18度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 19度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 "
    "43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 20度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 "
    "43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 21度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 43 43 43 43 "
    "43 43 43 43 CA 01 43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 22度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 CA 01 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 23度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 "
    "43 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 24度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 25度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 "
    "43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 26度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 27度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 "
    "43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 28度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 "
    "43 43 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16",  # 29度

    "68 03 01 FF 22 A6 04 A6 04 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 "
    "43 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 "
    "CA 01 43 43 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 "
    "43 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 8C 05 A6 04 A6 04 43 CA 01 43 "
    "43 43 CA 01 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 43 43 43 43 CA 01 43 CA 01 43 43 43 CA "
    "01 43 CA 01 43 43 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 CA 01 43 43 43 CA 01 43 43 43 43 43 43 "
    "43 43 43 43 43 43 43 CA 01 43 43 43 CA 01 43 CA 01 43 43 43 43 43 43 43 43 43 43 43 CA 01 43 43 43 43 43 "
    "CA 01 43 CA 01 43 CA 01 43 CA 01 43 A0 16"  # 30度
]
