import os
import pyttsx3
import myNLP
engine=pyttsx3.init()
engine.setProperty('rate', 150)
# engine.setProperty('voice','english+f2')
engine.setProperty('voice', "zh")

# 读取文本进行测试
filename = "example"
with open(filename, "rb") as file:
    lines = file.readlines()

for line in lines:
    line = line.decode('utf-8').strip()  # 使用适当的编码进行解码
    engine.say(“)
    engine.runAndWait()


