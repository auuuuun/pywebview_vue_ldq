import ctypes
import os
import socket
import sys
import threading
from contextlib import redirect_stdout
from io import StringIO

import webview

from app.keyboard import keyboard_listener, key_press_thread


def get_free_port():
    # 创建一个临时套接字
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0))  # 绑定到本地地址，端口号为0表示由系统自动选择一个空闲端口
    _, port_number = temp_socket.getsockname()  # 获取分配的端口号
    temp_socket.close()  # 关闭套接字
    return port_number


# 关闭程序调用，关闭所有程序
def on_closed():
    os._exit(0)


def run_as_admin():
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, params, 1)


def run_all(is_open_debug):
    stream = StringIO()
    # 保证程序可以在关闭gui页面后确定退出
    with redirect_stdout(stream):
        # 获取一个空闲端口
        port = get_free_port()
        # 创建flask服务器
        from app.socket import run_server
        threading.Thread(target=run_server, args=(port, is_open_debug,)).start()
        # 创建一个线程来运行键盘监听器，设置线程为守护线程，防止退出主线程时，子线程仍在运行
        threading.Thread(target=keyboard_listener, args=(), daemon=True).start()

        # 创建一个线程来运行鼠标点击事件，设置线程为守护线程，防止退出主线程时，子线程仍在运行
        threading.Thread(target=key_press_thread, daemon=True).start()

        window = webview.create_window(title='鼠标连点器', width=545, height=300, url=f"http://127.0.0.1:{port}")
        window.events.closed += on_closed
        webview.start(debug=is_open_debug, private_mode=False)


# 程序入口
if __name__ == '__main__':
    from app.global_mouse import read_json, config_file_name

    config_dic = read_json(config_file_name)
    if config_dic.get('debug'):
        run_all(True)
    else:
        if ctypes.windll.shell32.IsUserAnAdmin():
            run_all(False)
        else:
            print("不是管理员，正在尝试提升权限...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit(0)
