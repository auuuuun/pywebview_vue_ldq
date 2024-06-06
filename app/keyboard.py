from pynput import keyboard
import time
import pyautogui

from app.socket import socketio

import app.global_mouse


# 格式化字符串为数字，如果报错或者无法解析，则为None
def convert_to_number(s):
    try:
        return int(s)
    except Exception as e:
        return None


# 更新鼠标延迟时间
def update_mouse_property(property_value, field_name):
    if field_name == 'move_time':
        app.global_mouse.move_time = property_value
    elif field_name == 'click_time':
        app.global_mouse.click_time = property_value
    elif field_name == 'start2_key':
        app.global_mouse.start2_key = property_value
    elif field_name == 'stop2_key':
        app.global_mouse.stop2_key = property_value
    app.global_mouse.update_json({field_name: property_value})


# 更新鼠标是否移动位置进行连点
def update_mouse_position_enabled(enabled):
    app.global_mouse.keyboard_xy_enabled = enabled
    app.global_mouse.update_json({'keyboard_xy_enabled': enabled})


# 直接更新鼠标位置全局变量
def update_mouse_position(x, y):
    app.global_mouse.keyboard_x = convert_to_number(x)
    app.global_mouse.keyboard_y = convert_to_number(y)
    # 通知websocket给前端
    result = {'x': convert_to_number(x), 'y': convert_to_number(y)}
    app.global_mouse.update_json(result)
    socketio.emit('message', {'msg': result, 'type': app.global_mouse.socket_type_001}, namespace='/message')
    return result


# 获取并且更新鼠标位置全局变量
def get_update_mouse_position():
    x, y = pyautogui.position()
    app.global_mouse.keyboard_x = x
    app.global_mouse.keyboard_y = y
    # 通知websocket给前端
    result = {'x': x, 'y': y}
    app.global_mouse.update_json(result)
    socketio.emit('message', {'msg': result, 'type': app.global_mouse.socket_type_001}, namespace='/message')
    return result


def update_mouse_type(mouse_type):
    app.global_mouse.mouse_type = mouse_type
    app.global_mouse.update_json({'mouse_type': mouse_type})
    return app.global_mouse.mouse_type


# 键盘监听器
def keyboard_listener():
    def on_press(key):
        try:
            if hasattr(key, 'char'):  # 判断是否是字符键
                handle_key(key.char)
            elif hasattr(key, 'name'):  # 判断是否是特殊按键
                handle_key(key.name)
        except Exception as e:
            pass

    def on_release(key):
        # 什么都不做
        pass

    def handle_key(key_value):
        # 先判断按的是f1还是f2
        # 进入循环全局变量，如果按了f2则取消
        # 然后判断 是左键还是右键
        if key_value == app.global_mouse.stop2_key:
            # 关闭键盘事件
            app.global_mouse.keyboard_enabled = 0
            socketio.emit('message', {'msg': {'keyboard_enabled': app.global_mouse.keyboard_enabled},
                                      'type': app.global_mouse.socket_type_001},
                          namespace='/message')
        elif key_value == app.global_mouse.start2_key:
            # 按下 F1 键，开启键盘事件
            app.global_mouse.keyboard_enabled = 1
            socketio.emit('message', {'msg': {'keyboard_enabled': app.global_mouse.keyboard_enabled},
                                      'type': app.global_mouse.socket_type_001},
                          namespace='/message')
        elif key_value == 'f3':
            get_update_mouse_position()

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


# 连点核心方法
def key_press_thread():
    while True:
        if app.global_mouse.keyboard_enabled == 1:
            if app.global_mouse.keyboard_xy_enabled == 1:
                if app.global_mouse.keyboard_x is not None and app.global_mouse.keyboard_y is not None:
                    # 将鼠标移动到屏幕的(100, 100)坐标处
                    pyautogui.moveTo(app.global_mouse.keyboard_x, app.global_mouse.keyboard_y,
                                     duration=app.global_mouse.move_time / 1000)
            if app.global_mouse.mouse_type == 1:
                pyautogui.click()
            else:
                pyautogui.rightClick()
        time.sleep(app.global_mouse.click_time / 1000)  # 添加一个小的延迟，以释放 CPU 资源


def init_mouse_data():
    # 获取本地文件中配置信息，更新本地缓存变量
    config_dic = app.global_mouse.read_json(app.global_mouse.config_file_name)
    if config_dic.get('x'):
        app.global_mouse.keyboard_x = config_dic.get('x')
    if config_dic.get('y'):
        app.global_mouse.keyboard_y = config_dic.get('y')
    if config_dic.get('move_time'):
        app.global_mouse.move_time = config_dic.get('move_time')
    if config_dic.get('click_time'):
        app.global_mouse.click_time = config_dic.get('click_time')
    if config_dic.get('keyboard_xy_enabled'):
        app.global_mouse.keyboard_xy_enabled = config_dic.get('keyboard_xy_enabled')
    if config_dic.get('start2_key'):
        app.global_mouse.start2_key = config_dic.get('start2_key')
    if config_dic.get('stop2_key'):
        app.global_mouse.stop2_key = config_dic.get('stop2_key')
    if config_dic.get('mouse_type'):
        app.global_mouse.mouse_type = config_dic.get('mouse_type')
    result_msg = {'x': convert_to_number(app.global_mouse.keyboard_x),
                  'y': convert_to_number(app.global_mouse.keyboard_y),
                  'move_time': app.global_mouse.move_time,
                  'click_time': app.global_mouse.click_time,
                  'start2_key': app.global_mouse.start2_key,
                  'stop2_key': app.global_mouse.stop2_key,
                  'mouse_type': app.global_mouse.mouse_type,
                  'keyboard_xy_enabled': app.global_mouse.keyboard_xy_enabled, }

    socketio.emit('message', {'msg': result_msg, 'type': app.global_mouse.socket_type_001}, namespace='/message')
    return result_msg
