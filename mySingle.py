from AliyunIoTClient import AliyunIoTClient
from InfraredCodelist import AirCondition
from FingerIdentity import Finger

# 定义连接服务器的参数
productKey = "jjpbLelFxW2"
deviceName = "ubuntutest"
deviceSecret = "df15f34d7d8d0dc9bb50f30d6e269ff9"
regionId = "cn-shanghai"

# 定义各属性参数
ACTemperature = int
ACStatus = bool
LightStatus = bool

# 创建服务器器对象并连接
client = AliyunIoTClient(productKey, deviceName, deviceSecret, regionId)
client.connect()

# 初始化空调对象
myAirCondition = AirCondition()
myAirCondition.getStatus()


# 设置空调温度
def setACTemperature():
    global ACTemperature, ACStatus
    temperature_input = int(input("请输入希望设置的空调温度"))
    # 设定空调温度
    myAirCondition.setTemperature(temperature_input)
    # 获取空调状态
    ACTemperature = myAirCondition.temperature
    ACStatus = myAirCondition.status
    client.send_message(ACStatus, ACTemperature, 100, 123.3, 1)


# 调高空调温度
def upACTemperature():
    global ACTemperature, ACStatus
    if myAirCondition.status:
        # 获取空调当前温度
        ACTemperature = myAirCondition.temperature
        if ACTemperature == 30:
            print("[Error]空调已到达最高温度")
        else:
            # 设定空调温度
            myAirCondition.setTemperature(ACTemperature + 1)
            print("[AC]空调温度上调一度，当前温度为", myAirCondition.temperature)
    else:
        print("[Error]空调已关机")
    # 上报消息
    client.send_message(myAirCondition.status, myAirCondition.temperature, 100, 123.3, 1)


# 降低空调温度
def downACTemperature():
    global ACTemperature, ACStatus
    if myAirCondition.status:
        # 获取空调当前温度
        ACTemperature = myAirCondition.temperature
        if ACTemperature == 18:
            print("[Error]空调已到达最低温度")
        else:
            # 设定空调温度
            myAirCondition.setTemperature(ACTemperature - 1)
            print("[AC]空调温度下调一度，当前温度为", myAirCondition.temperature)
    else:
        print("[Error]空调已关机")
    # 上报消息
    client.send_message(myAirCondition.status, myAirCondition.temperature, 100, 123.3, 1)


# 打开空调
def openAC():
    if not myAirCondition.status:
        myAirCondition.openAirCondition()
        print("[AC]空调开启成功，当前设置温度为", )
    else:
        print("[Error]空调已经开机了")
    # 上报消息
    client.send_message(myAirCondition.status, myAirCondition.temperature, 100, 123.3, 1)


# 关闭空调
def closeAC():
    if myAirCondition.status:
        myAirCondition.closeAirCondition()
        print("[AC]空调关机成功")
    else:
        print("[Error]空调已经关机了")
    # 上报消息
    client.send_message(myAirCondition.status, myAirCondition.temperature, 100, 123.3, 1)


def function2():
    FingerPrint = Finger()
    FingerPrint.init()
    FingerPrint.close()
    print("执行功能2")


def switch_case(case):
    cases = {
        1: setACTemperature,    # 设置空调温度
        2: upACTemperature,     # 调高空调温度
        3: downACTemperature,   # 降低空调温度
        4: openAC,              # 打开空调
        5: closeAC,             # 关闭空调
        6: function2
    }
    # 根据用户输入的值在字典中查找对应的函数并执行
    cases.get(case, lambda: print("无效的选择。"))()


# 示例使用
user_input = int(input("请输入一个数字（1、2或3）："))

switch_case(user_input)
client.loop_forever()
