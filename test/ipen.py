import serial
import InfraredCodelist

# 初始化空调对象
myAirCondition = InfraredCodelist.AirCondition()
myAirCondition.getStatus()
# 打开 COM5，将波特率配置为115200.
ser = serial.Serial(port="COM5", baudrate=115200)

# 将十六进制字符串转换为字节对象
data_bytes = bytes.fromhex(InfraredCodelist.AirCondition_temperature[0])

# 串口发送数据，并输出发送的字节数。
write_len = ser.write(data_bytes)
print("串口发出{}个字节。".format(write_len))



ser.close()
