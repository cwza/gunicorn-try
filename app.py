
from flask import Flask
from flask import request
import time
import datetime
# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)

def sim_io_block(sec):
    time.sleep(sec)

def sim_cpu_block(sec):
    start_time = datetime.datetime.now()
    while True:
        cur_time = datetime.datetime.now()
        if cur_time > start_time + datetime.timedelta(0,sec):
            break

print(f'{datetime.datetime.now()} server start')
# sim_cpu_block(10)
# sim_io_block(10)
print(f'{datetime.datetime.now()} server end')

@app.route('/')
def hello():
    print(f'{datetime.datetime.now()} hello start')
    print(f'{datetime.datetime.now()} hello end')
    return 'Hello, World!'


@app.route('/io-block')
def io_block():
    print(f'{datetime.datetime.now()} io-block start')
    sec = request.args.get('sec')
    if sec is None:
        sec = 15
    sec = int(sec)
    sim_io_block(sec)
    print(f'{datetime.datetime.now()} io-block end')
    return 'io-block end'

@app.route('/cpu-block')
def cpu_block():
    print(f'{datetime.datetime.now()} cpu-block start')
    sec = request.args.get('sec')
    if sec is None:
        sec = 15
    sec = int(sec)
    sim_cpu_block(sec)
    print(f'{datetime.datetime.now()} cpu-block end')
    return 'cpu-block end'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, threaded=False, processes=1)