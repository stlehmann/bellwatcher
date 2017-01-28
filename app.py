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


@app.route('/')
def index():
    rings = reversed([x for x in db.all()])
    return render_template('index.html', rings=rings)


@app.route('/api/add', methods=['POST'])
def add_data():
    json_data = json.loads(request.data)
    db.insert({
        'datetime': arrow.now().format('DD.MM.YYYY HH:mm:ss'),
        'count': json_data['count']
    })
    return 'ok'


@app.route('/api/remove/<id_>')
def remove_data(id_):
    eid = int(id_)
    db.remove(eids=[eid])
    return 'ok'


@app.route('/api/clear')
def clear_data():
    db.purge()
    return 'ok'


if __name__ == '__main__':
    application = DispatcherMiddleware(None, {
        '/bell': app
    })
    run_simple('0.0.0.0', 8081, application)
