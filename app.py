import arrow
import json
from tinydb import TinyDB
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
bootstrap = Bootstrap(app)
db = TinyDB('db.json')
ring_table = db.table('rings')
log_table = db.table('logs')


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
    db.remove(eids=[eid])
    return 'ok'


@app.route('/api/clear')
def clear_data():
    log_table.purge()
    ring_table.purge()
    return 'ok'


if __name__ == '__main__':
    application = DispatcherMiddleware(None, {
        '/bell': app
    })
    run_simple('0.0.0.0', 8081, application)
