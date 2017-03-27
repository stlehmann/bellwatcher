import arrow
import json
import eventlet
from tinydb import TinyDB
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_mqtt import Flask_MQTT
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple


eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd784fa8b6d98d27699781bd9a7cf19f0'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'mqtt.mrl33h.de'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'mrl33h'
app.config['MQTT_PASSWORD'] = 'cz6qk3'
app.config['MQTT_REFRESH_TIME'] = 0.1
bootstrap = Bootstrap(app)
socketio = SocketIO(app)
db = TinyDB('db.json')
ring_table = db.table('rings')
log_table = db.table('logs')

# MQTTClient
mqtt = Flask_MQTT(app)
mqtt.connect()

@app.route('/')
def index():
    rings = reversed([x for x in ring_table.all()])
    logs = reversed([x for x in log_table.all()])
    return render_template('index.html', rings=rings, logs=logs)


@app.route('/api/add', methods=['POST'])
def add_data():
    json_data = json.loads(request.data.decode('utf-8'))
    ring_table.insert({
        'datetime': arrow.now().format('DD.MM.YYYY HH:mm:ss'),
        'count': json_data['count']
    })
    return 'ok'


@app.route('/api/log', methods=['POST'])
def log():
    json_data = json.loads(request.data.decode('utf-8'))
    log_table.insert({
        'datetime': arrow.now().format('DD.MM.YYYY HH:mm:ss'),
        'message': json_data['message']
    })
    return 'ok'


@app.route('/api/remove/<id_>')
def remove_data(id_):
    eid = int(id_)
    ring_table.remove(eids=[eid])
    return 'ok'


@app.route('/api/clear')
def clear_data():
    log_table.purge()
    ring_table.purge()
    return 'ok'

@mqtt.subscribe('/home/temperature')
def print_it(client, userdata, message):
    data = {'temperature': float(message.payload.decode())}
    socketio.emit('new temperature', data)


if __name__ == '__main__':
    application = DispatcherMiddleware(None, {
        '/bell': app
    })
    run_simple('0.0.0.0', 8081, application)
