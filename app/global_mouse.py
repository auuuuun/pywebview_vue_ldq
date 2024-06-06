from flask import jsonify
import json

# 连点开启标记
keyboard_enabled = 0
# 鼠标左键右键点击标记，1左键，2右键
mouse_type = 1
# 鼠标定位开启标记 0关闭 1开启
keyboard_xy_enabled = 0
# 鼠标定位参数
keyboard_x = None
keyboard_y = None

# 移动间隔
move_time = 100
# 点击间隔
click_time = 100
# 启动热键，两个都有则是组合键
start1_key = None
start2_key = 'f1'

# 停止热键，两个都有则是组合键
stop1_key = None
stop2_key = 'f2'

# 鼠标类型，socket使用
# 更新鼠标按钮vue数据
socket_type_001 = '001'

config_file_name = 'config.json'


def update_json(update_json_data):
    config_dic = read_json(config_file_name)
    json_keys = update_json_data.keys()
    for key in json_keys:
        config_dic[key] = update_json_data[key]
    save_json(config_file_name, config_dic)


# 读取文件生成配置信息
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            config_list = json.load(file)
            if len(config_list) == 0:
                return {}
            else:
                return config_list
    except FileNotFoundError:
        return {}


def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def ok(data):
    response = {'status': 0, 'data': data}
    return jsonify(response)


def err(msg):
    response = {'status': -1, 'msg': msg}
    return jsonify(response)
