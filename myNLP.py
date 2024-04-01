import re


def check_command(text: str):
    metadata = 0
    patterns = [
        r'(开灯|开启灯|请开灯|打开灯|有点黑)',
        r'(关灯|关闭灯|请关灯|打开灯|有点亮)',
        r'(开|打开)空调|空调开机',
        r'(关|关闭)空调|空调关机',
        r'(调高|升高|提高)空调温度|太冷了',
        r'(调低|降低|减小)空调温度|太热了',
        r'(?:当前的)?湿度((?:是多少)?(?:也为)?[多少]|是)',
        r'(?:当前的)?温度((?:是多少)?(?:也为)?[多少]|是)',
        r'(?:空调温度设置|空调设置).*?([一二三四五六七八九十百千]+)度'
    ]

    matches = [re.search(pattern, text) for pattern in patterns]

    if matches[0] and matches[2]:
        return metadata, "开灯和开空调"
    elif matches[0]:
        return metadata, "开灯"
    elif matches[1]:
        return metadata, "关灯"
    elif matches[2]:
        return metadata, "开空调"
    elif matches[3]:
        return metadata, "关空调"
    elif matches[4]:
        return metadata, "调高空调温度"
    elif matches[5]:
        return metadata, "调低空调温度"
    elif matches[6]:
        return metadata, "获取湿度"
    elif matches[7]:
        return metadata, "获取温度"
    elif matches[8]:
        temperature = convert_chinese_number(matches[8].group(1))
        if temperature is not None:
            metadata = temperature
            if temperature > 30:
                return metadata, "温度过高"
            elif temperature < 18:
                return metadata, "温度太低"
            else:
                return metadata, "设置空调温度为{}度".format(temperature)
    else:
        metadata = 1
        return metadata, "未匹配命令"


def convert_chinese_number(number):
    num_mapping = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
        '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000
    }
    result = 0
    temp_num = 0
    for char in number:
        if char in num_mapping:
            if num_mapping[char] >= 10:
                if temp_num == 0:
                    temp_num = num_mapping[char]
                else:
                    temp_num *= num_mapping[char]
            else:
                temp_num += num_mapping[char]
        elif char == '零':
            temp_num *= 10
        elif char == '十':
            temp_num = 10
        else:
            return None
        if temp_num >= 10:
            result += temp_num
            temp_num = 0
    result += temp_num
    return result

# # 读取文本进行测试
# filename = "example"
# with open(filename, "rb") as file:
#     lines = file.readlines()
#
# for line in lines:
#     line = line.decode('utf-8').strip()  # 使用适当的编码进行解码
#     tempData, command = check_command(line)
#     print("原始文本: {}".format(line))
#     print("匹配指令: {}\n".format(command))
