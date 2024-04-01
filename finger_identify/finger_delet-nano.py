# -*- coding:utf-8 -*-
import binascii
import serial
import time

# 配置串口
ser = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=57600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

head = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00'
link = b'\x07\x13\x00\x00\x00\x00\x00\x1B'
readflash = b'\x03\x16\x00\x1A'
readmould = b'\x03\x1D\x00\x21'
readindex = b'\x04\x1F\x00\x00\x24'
readindex1 = b'\x04\x1F\x01\x00\x25'
cmd_search = b'\x03\x01\x00\x05'
cmd_upload = b'\x03\x0A\x00\x0E'
cmd_gen1 = b'\x04\x02\x01\x00\x08'
cmd_gen2 = b'\x04\x02\x02\x00\x09'
cmd_reg = b'\x03\x05\x00\x09'
cmd_save = b'\x06\x06\x01\x00'
cmd_dis = b'\x08\x04\x01\x00\x00\x01\x2C\x00\x3B'
cmd_deletchar = b'\x07\x0c\x00'


def sendcmd(cmd):
    ser.write(head)
    ser.write(cmd)
    time.sleep(0.35)


def init():
    sendcmd(link)
    sendcmd(readflash)
    sendcmd(readmould)
    sendcmd(readindex)
    ser.flushInput()
    sendcmd(readindex1)
    count = ser.inWaiting()
    recv = ser.read(count)
    recv = str(binascii.b2a_hex(recv))[0:44]
    # print(count)
    # print(recv)
    ser.flushInput()


def searchfig():
    time.sleep(0.1)
    sendcmd(cmd_search)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    hc = str(binascii.b2a_hex(hc))[21:22]
    while hc == '2':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        ser.flushInput()
        time.sleep(0.5)


def disfig():
    print('请按手指')
    searchfig()
    print('识别中')
    time.sleep(0.2)
    sendcmd(cmd_gen1)
    time.sleep(0.1)
    ser.flushInput()
    time.sleep(0.1)
    sendcmd(cmd_dis)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    # print(hc)
    disno = str(binascii.b2a_hex(hc))[21:22]
    disid = str(binascii.b2a_hex(hc))[25:26]
    # print(disno)
    # print(disid)
    print("识别结果：")
    time.sleep(0.1)
    if disno == '9':
        return "未找到匹配指纹"
    else:
        return disid


def waitfig():
    time.sleep(0.1)
    sendcmd(cmd_search)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    hc = str(binascii.b2a_hex(hc))[21:22]
    print('松开手指')
    while hc == '0':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        ser.flushInput()


def savefig(addr):
    print('请按手指')
    searchfig()
    sendcmd(cmd_gen1)
    print('请再按手指')
    time.sleep(3)
    searchfig()
    sendcmd(cmd_gen2)
    time.sleep(0.1)
    ser.flushInput()
    sendcmd(cmd_reg)
    time.sleep(0.1)
    count = ser.inWaiting()
    reg = ser.read(count)
    reg = str(binascii.b2a_hex(reg))[20:21]
    # print(reg)
    if reg == '0':
        add = cmd_save + bytearray([addr, 0, addr + 0xe])
        sendcmd(add)
        print('存入成功')
    else:
        print('存入失败')
    ser.flushInput()


def deletfig(addr):
    deletchar = cmd_deletchar + bytearray([addr, 0, 1, 0, addr + 0x15])
    sendcmd(deletchar)
    time.sleep(0.5)
    count = ser.inWaiting()
    reg = ser.read(count)
    ser.flushInput()
    with open("finger.txt", "r") as r:
        lines = r.readlines()
    with open("finger.txt", "w") as w:
        for l in lines:
            if str(addr) not in l:
                w.write(l)
        w.close()
        r.close()
    print('删除命令执行完成')


time.sleep(1)
# 初始化指纹识别模块
init()
print('初始化成功')
time.sleep(0.1)
print('请输入需要删除的指纹编号:')
n = input()
# 删除ID为2的指纹
deletfig(int(n))
ser.close()
