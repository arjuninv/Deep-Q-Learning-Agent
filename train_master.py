from flask import Flask, request
import datetime
from tabulate import tabulate
from _thread import *
import os
import time

app = Flask(__name__)

workers = []

@app.route('/master/connect')
def connect():
    global workers
    worker = {k: v for k, v in request.args.items()}
    worker["connected_at"] = datetime.datetime.now()
    worker["updated_at"] = datetime.datetime.now()
    workers.append(worker)
    return str((len(workers) - 1))

@app.route('/master/update')
def update():
    global workers
    id = request.args['id']
    for arg in request.args.keys():
        if arg != 'id':
            workers[int(id)][arg] = request.args[arg]
    workers[int(id)]["updated_at"] = datetime.datetime.now()
    return id

def serve():
    app.run(debug=True)
    
def mainloop():
    global workers
    workers_state = []
    while True:
        if (len(workers_state) != len(workers)) or (any([bool(hash(frozenset(worker.items())) != workers_state[i]) for i, worker in enumerate(workers)])):
            os.system('clear')
            print("Status: ")
            table = {}
            for worker in workers:
                for k, v in worker.items():
                    if k != "worker_name":
                        temp = table.get(k, [])
                        temp.append(v)
                        table[k] = temp
            print(tabulate([[attribute_name] + [attribute_value for attribute_value in table[attribute_name]] for attribute_name in table.keys()], headers=["Attribute"] + [x["worker_name"] for x in workers]), end='')
        workers_state = [hash(frozenset(worker.items())) for worker in workers]
        time.sleep(1)


if __name__ == '__main__':
    try:
        # start_new_thread(serve, ())
        start_new_thread(mainloop, ())
        serve()   
    except Exception as e:
        print(e)
        
    while True:
        pass