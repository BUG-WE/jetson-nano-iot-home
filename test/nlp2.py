import re

def process_command(text):
    pattern = r'(?:空调温度设置|空调设置).*?([一二三四五六七八九十百千]+)度'
    match = re.search(pattern, text)
    if match:
        temperature = convert_chinese_number(match.group(1))
        if temperature is not None:
            if temperature > 30:
                return "温度过高"
            elif temperature < 18:
                return "温度太低"
            else:
                return "设置温度为{}度".format(temperature)
    return "未匹配指令"

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

# 测试示例
text1 = "请将空调温度设置为二十六度"
text2 = "空调设置三十二度"
text3 = "请将空调设置为十六度"
text4 = "设置温度为二十五度"
text5 = "请打开窗户"
text6 = "空调设置二十度"

print(process_command(text1))  # 输出: 设置温度为26度
print(process_command(text2))  # 输出: 温度过高
print(process_command(text3))  # 输出: 温度太低
print(process_command(text4))  # 输出: 未匹配指令
print(process_command(text5))  # 输出: 未匹配指令
print(process_command(text6))  # 输出: 设置温度为20度
