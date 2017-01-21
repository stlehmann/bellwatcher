import arrow
from tinydb import TinyDB
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
bootstrap = Bootstrap(app)
db = TinyDB('db.json')


@app.route('/')
def index():
    rings = reversed([x['datetime'] for x in db.all()])
    return render_template('index.html', rings=rings)


@app.route('/api/add', methods=['POST'])
def add_data():
    db.insert({'datetime': arrow.now().format('DD.MM.YYYY HH:mm:ss')})
    return 'ok'


@app.route('/api/clear')
def clear_data():
    db.purge()
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
