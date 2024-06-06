from flask_socketio import SocketIO, emit
from app.views import app
# 对于python没什么用，但是对于pyinstaller有用
from engineio.async_drivers import eventlet
from eventlet.hubs import epolls, kqueue, selects
from dns import versioned, dnssec, e164, namedict, tsigkeyring, update, version, zone

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')


# 启动服务器
def run_server(port_number, is_open_debug):
    socketio.run(app, port=port_number, debug=is_open_debug, use_reloader=False)


@socketio.on('connect', namespace='/message')
def handle_connect():
    emit('message', {'message': 'Client connected'}, broadcast=True)
    print('Client connected')


@socketio.on('message', namespace='/message')
def handle_message(json):
    message = json['message']
    emit('message', {'message': message}, broadcast=True)


def send_message(msg):
    socketio.emit('message', msg, broadcast=True)
