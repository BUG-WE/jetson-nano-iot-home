import binascii
import serial
import time

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


class Finger:
    def __init__(self, port="/dev/ttyTHS1", baudrate=57600):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )

    def sendcmd(self, cmd):
        self.ser.write(head)
        self.ser.write(cmd)
        time.sleep(0.35)

    def init(self):
        self.sendcmd(link)
        self.sendcmd(readflash)
        self.sendcmd(readmould)
        self.sendcmd(readindex)
        self.ser.flushInput()
        self.sendcmd(readindex1)
        count = self.ser.inWaiting()
        recv = self.ser.read(count)
        recv = str(binascii.b2a_hex(recv))[0:44]
        self.ser.flushInput()
        print('指纹模块初始化成功')

    def searchfig(self):
        time.sleep(0.1)
        self.sendcmd(cmd_search)
        time.sleep(0.1)
        count = self.ser.inWaiting()
        hc = self.ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        while hc == '2':
            time.sleep(0.1)
            self.sendcmd(cmd_search)
            time.sleep(0.1)
            count = self.ser.inWaiting()
            hc = self.ser.read(count)
            hc = str(binascii.b2a_hex(hc))[21:22]
            self.ser.flushInput()
            time.sleep(0.5)

    def disFinger(self):
        print('请按手指')
        self.searchfig()
        print('识别中')
        time.sleep(0.2)
        self.sendcmd(cmd_gen1)
        time.sleep(0.1)
        self.ser.flushInput()
        time.sleep(0.1)
        self.sendcmd(cmd_dis)
        time.sleep(0.1)
        count = self.ser.inWaiting()
        hc = self.ser.read(count)
        disno = str(binascii.b2a_hex(hc))[21:22]
        disid = str(binascii.b2a_hex(hc))[25:26]
        print("识别结果：")
        time.sleep(0.1)
        if disno == '9':
            return "未找到匹配指纹"
        else:
            return disid

    def waitFinger(self):
        time.sleep(0.1)
        self.sendcmd(cmd_search)
        time.sleep(0.1)
        count = self.ser.inWaiting()
        hc = self.ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        print('松开手指')
        while hc == '0':
            time.sleep(0.1)
            self.sendcmd(cmd_search)
            time.sleep(0.1)
            count = self.ser.inWaiting()
            hc = self.ser.read(count)
            hc = str(binascii.b2a_hex(hc))[21:22]
            self.ser.flushInput()

    def saveFinger(self, addr):
        print('请按手指')
        self.searchfig()
        self.sendcmd(cmd_gen1)
        print('请再按手指')
        time.sleep(3)
        self.searchfig()
        self.sendcmd(cmd_gen2)
        time.sleep(0.1)
        self.self.ser.flushInput()
        self.sendcmd(cmd_reg)
        time.sleep(0.1)
        count = self.ser.inWaiting()
        reg = self.ser.read(count)
        reg = str(binascii.b2a_hex(reg))[20:21]
        # print(reg)
        if reg == '0':
            add = cmd_save + bytearray([addr, 0, addr + 0xe])
            self.sendcmd(add)
            print('存入成功')
            name = str()
            name = input('请输入用户姓名')
            with open("finger.txt", "r") as r:
                lines = r.readlines()
            with open("finger.txt", "w") as w:
                for l in lines:
                    if str(addr) not in l:
                        w.write(l)
                w.writelines([str(addr), name, '\n'])
                w.close()
                r.close()

    def deleteFinger(self, addr):
        deletchar = cmd_deletchar + bytearray([addr, 0, 1, 0, addr + 0x15])
        self.sendcmd(deletchar)
        time.sleep(0.5)
        count = self.ser.inWaiting()
        reg = self.ser.read(count)
        self.ser.flushInput()
        with open("finger_identify/finger.txt", "r") as r:
            lines = r.readlines()
        with open("finger_identify/finger.txt", "w") as w:
            for l in lines:
                if str(addr) not in l:
                    w.write(l)
            w.close()
            r.close()
        print('删除命令执行完成')

    def close(self):
        self.ser.close()

    def search(self):
        try:
            while True:
                n = str
                n = self.disFinger()
                if n == "未找到匹配指纹":
                    print(n)
                else:
                    with open("finger.txt", "r") as f:
                        for line in f.readlines():
                            if line[0] == n:
                                line = line.strip('/n')
                                print("指纹的主人为", line.strip(n), "编号为", n)
                                f.close()
                                return 1
                # 等待手指松开
                self.waitFinger()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting Program")
            return 0
        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
            return 0
        finally:
            self.ser.close()
            pass

    def save(self):
        time.sleep(0.1)
        n = int(input('请输入要存储的位置'))
        # 录入指纹并存储在ID n
        self.saveFinger(n)
        self.ser.close()

if __name__ == '__main__':
    time.sleep(1)
    FingerPrint = Finger()
    FingerPrint.init()

    time.sleep(0.1)
    print('请输入需要删除的指纹编号:')
    n = input()
    FingerPrint.deleteFinger(int(n))
    FingerPrint.close()
