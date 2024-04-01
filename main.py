import time

import FingerIdentity
import myNLP
import RGBLED
import subprocess
from AliyunIoTClient import AliyunIoTClient
from InfraredCodelist import AirCondition
from DHT11 import DHT11
from paddlespeech.cli.asr.infer import ASRExecutor
from FingerIdentity import Finger

# 定义连接服务器的参数
productKey = "jjpbLelFxW2"
deviceName = "ubuntutest"
deviceSecret = "df15f34d7d8d0dc9bb50f30d6e269ff9"
regionId = "cn-shanghai"

# 创建服务器器对象并连接
myClient = AliyunIoTClient(productKey, deviceName, deviceSecret, regionId)
myClient.connect()

# 初始化空调对象
myAirCondition = AirCondition()

# 初始温湿度传感器
dht_sensor = DHT11(36)

# 初始化对象
ACStatus = bool
ACTemperature = int
temperature = float
humidity = float
switch = bool
metadata = int
voiceToText = str
textToCommand = str
textToVoice = str
yunCommand = str  # 云端下发的指令
light_flag = 0
f_flag = 0
FingerPrint = FingerIdentity.Finger()
FingerPrint.init()

# main函数


while 1:
    if f_flag == 0:
        f_flag = FingerPrint.search()
    else:
        file = open("example.txt", "w")
        print("[Home]欢迎回家")
        text = "欢迎回家"
        # 将文本写入文件
        file.write(text)
        # 关闭文件
        file.close()
        # 语音播报
        subprocess.run("python3.6 texttowave.py", shell=True)
        print(yunCommand)
        if light_flag == 1:
            RGBLED.on_light()
        else:
            RGBLED.out_light()

        # 获取温湿度
        temperature, humidity = dht_sensor.read_data()
        if temperature is not None and humidity is not None:
            print("温度为", temperature, "摄氏度")
            print("湿度为", humidity, "%")
        else:
            print("无法读取温度和湿度数据。")

        # 获取空调状态
        ACTemperature = myAirCondition.temperature
        ACStatus = myAirCondition.status
        # 打印空调状态
        myAirCondition.getStatus()
        # 上报消息
        myClient.send_message(ACStatus, ACTemperature, 100, 100, switch)

        yunCommand = myClient.yunCommand

        if yunCommand == "开始录音":
            # py3.6.9
            subprocess.run("python3.6 audioRecord.py", shell=True)
            asr = ASRExecutor()
            voiceToText = asr(audio_file="output.wav")
            print("[ASR]识别结果", voiceToText)

            metadata, textToCommand = myNLP.check_command(voiceToText)

            if textToCommand == "开灯":
                light_flag = 1
                file.close()
            elif textToCommand == "关灯":
                light_flag = 0
                file.close()
            elif textToCommand == "开空调":
                if not myAirCondition.status:
                    myAirCondition.openAirCondition()
                    print("[AC]空调开启成功，当前设置温度为", ACTemperature)
                    # 要写入的文本内容
                    text = "空调开启成功，当前设置温度为".format(ACTemperature)
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)

                else:
                    print("[Error]空调已经开机了")
                    text = "空调已经开机了"
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "关空调":
                if myAirCondition.status:
                    myAirCondition.closeAirCondition()
                    print("[AC]空调关机成功")
                    text = "空调关机成功"
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)
                else:
                    print("[Error]空调已经关机了")
                    text = "空调已经关机了"
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "调高空调温度":
                if myAirCondition.status:
                    # 获取空调当前温度
                    ACTemperature = myAirCondition.temperature
                    if ACTemperature == 30:
                        print("[Error]空调已到达最高温度")
                        text = "空调已达到最高温度"
                        # 将文本写入文件
                        file.write(text)
                        # 关闭文件
                        file.close()
                        # 语音播报
                        subprocess.run("python3.6 texttowave.py", shell=True)
                    else:
                        # 设定空调温度
                        myAirCondition.setTemperature(ACTemperature + 1)
                        print("[AC]空调温度上调一度，当前温度为", myAirCondition.temperature)
                        text = "空调温度上调一度当前温度为".format(myAirCondition.temperature)
                        # 将文本写入文件
                        file.write(text)
                        # 关闭文件
                        file.close()
                        # 语音播报
                        subprocess.run("python3.6 texttowave.py", shell=True)
                else:
                    print("[Error]空调已关机")
                    text = "空调已关机"
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "调低空调温度":
                if myAirCondition.status:
                    # 获取空调当前温度
                    ACTemperature = myAirCondition.temperature
                    if ACTemperature == 18:
                        print("[Error]空调已到达最低温度")
                        text = "空调已达到最低温度"
                        # 将文本写入文件
                        file.write(text)
                        # 关闭文件
                        file.close()
                        # 语音播报
                        subprocess.run("python3.6 texttowave.py", shell=True)
                    else:
                        # 设定空调温度
                        myAirCondition.setTemperature(ACTemperature - 1)
                        print("[AC]空调温度下调一度，当前温度为", myAirCondition.temperature)
                        text = "空调温度下调一度当前温度为".format(myAirCondition.temperature)
                        # 将文本写入文件
                        file.write(text)
                        # 关闭文件
                        file.close()
                        # 语音播报
                        subprocess.run("python3.6 texttowave.py", shell=True)
                else:
                    print("[Error]空调已关机")
                    text = "空调已关机"
                    # 将文本写入文件
                    file.write(text)
                    # 关闭文件
                    file.close()
                    # 语音播报
                    subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "获取湿度":
                temperature, humidity = dht_sensor.read_data()
                print("当前室内湿度为", humidity)
                text = "当前室内湿度为".format(humidity)
                # 将文本写入文件
                file.write(text)
                # 关闭文件
                file.close()
                # 语音播报
                subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "获取温度":
                temperature, humidity = dht_sensor.read_data()
                print("当前室内温度为", temperature)
                text = "当前室内温度为".format(temperature)
                # 将文本写入文件
                file.write(text)
                # 关闭文件
                file.close()
                # 语音播报
                subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)
            elif textToCommand == "温度过高":
                print("[error]设置温度过高无法执行命令")
                text = "设置温度过高，无法执行命令"
                # 将文本写入文件
                file.write(text)
                # 关闭文件
                file.close()
                # 语音播报
                subprocess.run("python3.6 texttowave.py", shell=True)
            elif textToCommand == "温度太低":
                print("[error]设置温度太低，无法执行命令")
                text = "设置温度太低无法执行命令"
                # 将文本写入文件
                file.write(text)
                # 关闭文件
                file.close()
                # 语音播报
                subprocess.run("python3.6 texttowave.py", shell=True)

            elif textToCommand == "设置空调温度为{}度".format(metadata):
                temperature_input = int(metadata)
                # 设定空调温度
                myAirCondition.setTemperature(temperature_input)
                # 获取空调状态
                ACTemperature = myAirCondition.temperature
                ACStatus = myAirCondition.status
                print("设置温度成功，为".format(metadata))
                text = "设置温度成功为".format(metadata)
                # 将文本写入文件
                file.write(text)
                # 关闭文件
                file.close()
                # 语音播报
                subprocess.run("python3.6 texttowave.py", shell=True)
                # 上报消息
                myClient.send_message(ACStatus, ACTemperature, temperature, humidity, switch)

        elif yunCommand == "有人来了":
            print("[ASR]识别结果", voiceToText)
        elif yunCommand =="录入指纹":
            print("[finger]开始录入指纹")
            FingerPrint.save()
        time.sleep(5)

myClient.loop_forever()
