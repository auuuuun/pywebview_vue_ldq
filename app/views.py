import os
from functools import wraps

import webview
from flask import Flask, jsonify, render_template, request

from app.global_mouse import ok, err

# development path
gui_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
if not os.path.exists(gui_dir):  # frozen executable path
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
# 替换flask和vue冲突的语法
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'


def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception('Authentication error')

    return wrapper


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
def landing():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    return render_template('index.html', token=webview.token)


@app.route('/test_get')
@verify_token
def test_get():
    test = request.args['test']
    print(test)
    return jsonify({'status': '0'})


@app.route('/test_post', methods=['POST'])
@verify_token
def test_post():
    test = request.json['test']
    print(test)
    return jsonify({'status': '0'})


# 更新鼠标位置方法
@app.route('/update_mouse_position', methods=['POST'])
@verify_token
def update_mouse_position():
    from app.keyboard import update_mouse_position
    result = update_mouse_position(request.json['x'], request.json['y'])
    return ok(result)


# 获取鼠标当前的位置
@app.route('/get_mouse_position', methods=['POST'])
@verify_token
def get_mouse_position():
    from app.keyboard import get_update_mouse_position
    result = get_update_mouse_position()
    return ok(result)


# 更新鼠标是否移动位置进行连点开关
@app.route('/update_mouse_position_enabled', methods=['POST'])
@verify_token
def update_mouse_position_enabled():
    from app.keyboard import update_mouse_position_enabled
    update_mouse_position_enabled(request.json['enabled'])
    return ok(None)


# 修改鼠标点击类型
@app.route('/update_mouse_type', methods=['POST'])
@verify_token
def update_mouse_type():
    from app.keyboard import update_mouse_type
    mouse_type = request.json['mouse_type']
    return ok(update_mouse_type(mouse_type))


# 修改鼠标点击延迟时间
@app.route('/update_mouse_property', methods=['POST'])
@verify_token
def update_mouse_property():
    from app.keyboard import update_mouse_property
    property_value = request.json['time_value']
    field_name = request.json['time_name']
    update_mouse_property(property_value, field_name)
    return ok(None)


# 获取初始信息
@app.route('/init_mouse_data')
@verify_token
def init_mouse_data():
    from app.keyboard import init_mouse_data
    return ok(init_mouse_data())
