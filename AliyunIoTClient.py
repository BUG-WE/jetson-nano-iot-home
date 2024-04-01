import paho.mqtt.client as mqtt
import time
import hashlib
import hmac
import json


class AliyunIoTClient:
    def __init__(self, product_key, device_name, device_secret, region_id='cn-shanghai'):
        identifier = "moshengren"
        identifier2 = "moshengrenlaile"
        self.product_key = product_key
        self.device_name = device_name
        self.device_secret = device_secret
        self.region_id = region_id
        self.host = f"{product_key}.iot-as-mqtt.{region_id}.aliyuncs.com"
        self.port = 1883
        self.pub_topic = f"/sys/{product_key}/{device_name}/thing/event/property/post"
        self.get_topic = f"/sys/{product_key}/{device_name}/thing/service/property/set"
        self.alarm_topic = f"/sys/{product_key}/{device_name}/thing/event/{identifier}/post"
        self.alarm_topic_replay = f"/sys/jjpbLelFxW2/ubuntutest/thing/event/moshengren/post_reply"
        self.switch_topic = f"/sys/jjpbLelFxW2/{device_name}/thing/service/ToggleLightSwitch"
        self.switch_topic_replay = f"/sys/jjpbLelFxW2/{device_name}/thing/service/Lightchange_reply"
        self.record_topic = f"/sys/jjpbLelFxW2/{device_name}/thing/service/isRecord"
        self.record_topic_replay = f"/sys/jjpbLelFxW2/{device_name}/thing/service/endRecord_reply"
        self.finger_topic = f"/sys/jjpbLelFxW2/{device_name}/thing/service/importFinger"
        self.finger_topic_replay = f"/sys/jjpbLelFxW2/{device_name}/thing/service/endfinger_reply"
        self.yunCommand = "noMsg"
        self.client = None

    @staticmethod
    def hmacsha1(key, msg):
        return hmac.new(key.encode(), msg.encode(), hashlib.sha1).hexdigest()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        data = json.loads(payload)
        print("Received message:", data)  # 打印接收到的消息内容

        if msg.topic == self.alarm_topic_replay:
            # 获取事件的输出数据字段名称
            output_field_name = "moshengrenlaile"

            # 检查事件消息中是否包含输出数据字段
            if 'params' in data and output_field_name in data['params']:
                output_value = data['params'][output_field_name]
                print(f"{output_field_name} 状态：{output_value}")
                # 根据状态执行相应的操作
            else:
                print(f"未找到 {output_field_name} 字段")

        if msg.topic == self.switch_topic:
            print("收到消息，已回复")
            self.reply_service_switch()

        if msg.topic == self.record_topic:
            self.yunCommand = "开始录音"
            print("收到录音消息，已回复")
            self.reply_service_record()

        if msg.topic == self.finger_topic:
            self.yunCommand = "录入指纹"
            print("收到录音消息，已回复")
            self.reply_finger_record()

    def get_client(self):
        timestamp = str(int(time.time()))
        client_id = f"paho.py|securemode=3,signmethod=hmacsha1,timestamp={timestamp}|"
        content_str_format = f"clientIdpaho.pydeviceName{self.device_name}productKey{self.product_key}timestamp{timestamp}"
        user_name = f"{self.device_name}&{self.product_key}"
        password = self.hmacsha1(self.device_secret, content_str_format)

        self.client = mqtt.Client(client_id=client_id, clean_session=False)
        self.client.username_pw_set(user_name, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        return self.client

    def open_Service(self, acs):
        Service = {
            'id': int(time.time()),
            'params': {
                'ACStatus': acs,
            },
            'method': "thing.event.property.post"
        }
        payload_json = json.dumps(Service)
        print('send data to IoT server: ' + str(payload_json))
        self.client.publish(self.pub_topic, payload=str(payload_json), qos=1)

    def send_message(self, acs, act, it, ih, ls):
        data = {
            'id': int(time.time()),
            'params': {
                'ACStatus': acs,
                'ACTemperature': act,
                'IndoorTemperature': it,
                'IndoorHumidity': ih,
                'LightSwitch': ls
            },
            'method': "thing.event.property.post"
        }
        payload_json = json.dumps(data)
        print('send data to IoT server: ' + str(payload_json))
        self.client.publish(self.pub_topic, payload=str(payload_json), qos=1)

    def send_alarm(self):
        event_message = {
            "id": int(time.time()),
            "version": "1.0",
            "params": {
                "moshengrenlaile": 0
            }
        }
        payload_json = json.dumps(event_message)
        print(str(payload_json))
        self.client.publish(self.alarm_topic, payload=str(payload_json), qos=1)

    def reply_service_switch(self):
        service_message = {
            "id": int(time.time()),
            "params": {
                "Lightchange": 0
            }
        }
        payload_json = json.dumps(service_message)
        print("响应设备服务")
        print(str(payload_json))
        self.client.publish(self.switch_topic_replay, payload=str(payload_json), qos=1)

    def reply_service_record(self):
        service_message = {
            "id": int(time.time()),
            "params": {
                "endRecord": 0
            }
        }
        payload_json = json.dumps(service_message)
        print("响应设备服务")
        print(str(payload_json))
        self.client.publish(self.switch_topic_replay, payload=str(payload_json), qos=1)

    def reply_finger_record(self):
        service_message = {
            "id": int(time.time()),
            "params": {
                "endfinger": 0
            }
        }
        payload_json = json.dumps(service_message)
        print("响应设备服务")
        print(str(payload_json))
        self.client.publish(self.finger_topic_replay, payload=str(payload_json), qos=1)


    def subscribe(self):
        self.client.subscribe(self.get_topic, qos=1)
        self.client.subscribe(self.alarm_topic_replay, qos=1)  # 添加订阅 "moshengren" 事件回复消息的订阅
        self.client.subscribe(self.switch_topic, qos=1)  # 添加订阅 服务启动了的消息的订阅
        self.client.subscribe(self.record_topic_replay, qos=1)  # 添加订阅 服务启动了的消息的订阅
        self.client.subscribe(self.finger_topic_replay, qos=1)  # 添加订阅 服务启动了的消息的订阅

    def connect(self):
        self.client = self.get_client()
        self.client.connect(self.host, self.port, 300)
        self.client.loop_start()
        self.subscribe()


if __name__ == '__main__':
    options = {
        'productKey': 'jjpbLelFxW2',
        'deviceName': 'ubuntutest',
        'deviceSecret': 'df15f34d7d8d0dc9bb50f30d6e269ff9',
        'regionId': 'cn-shanghai'
    }

    client = AliyunIoTClient(options['productKey'], options['deviceName'], options['deviceSecret'], options['regionId'])
    client.connect()
    while 1:
        client.send_message(0, 26, 26.7, 86.6, 1)
        time.sleep(10)

    client.loop_forever()
