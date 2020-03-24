from flask import Flask, request
import datetime
from tabulate import tabulate
from _thread import *
import os
import time
import tensorflow as tf


MODEL_DIR = "saved_models"
CWD = os.getcwd()
app = Flask(__name__)

workers = []

class Logger(object):
    logger_dict = {}
    def __init__(self, worker_name):
        Logger.logger_dict[worker_name] = self
        logdir = os.path.join(CWD, f"logs/{worker_name}/scalars/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.writer = tf.summary.create_file_writer(logdir + "/metrics")
        self.step_rec = {}
        
    @staticmethod
    def get_logger(worker_name):
        if worker_name in Logger.logger_dict:
            return Logger.logger_dict[worker_name]
        else:
            return Logger(worker_name)

    def log_scalar(self, tag, value):
        self.step_rec[tag] = self.step_rec.get(tag, 0) + 1
        self.writer.set_as_default()
        tf.summary.scalar(tag, data=float(value), step=self.step_rec[tag])
        self.writer.flush()
        # summary = tf.Summary(value=[tf.Summary.Value(tag=tag, simple_value=value)])
        # self.writer.add_summary(summary, self.step_rec)


@app.route('/master/connect')
def connect():
    global workers
    worker = {k: v.replace("curr_time", str(datetime.datetime.now())) for k, v in request.args.items()}
    worker["connected_at"] = datetime.datetime.now()
    worker["updated_at"] = datetime.datetime.now()
    workers.append(worker)
    return str((len(workers) - 1))


@app.route('/master/update')
def update():
    global workers
    id = request.args['id']
    worker_name = workers[int(id)]["worker_name"]
    for arg in request.args.keys():
        if arg != 'id':
            temp = request.args[arg].replace("curr_time", str(datetime.datetime.now()))
            workers[int(id)][arg] = temp
            
            if arg in ["acc", "loss", "mse"]:
                Logger.get_logger(worker_name).log_scalar(arg, request.args[arg])
    workers[int(id)]["updated_at"] = datetime.datetime.now()
    return id
                
@app.route('/master/send_model', methods=['POST'])
def send_model():
    global workers
    id = request.args['id']
    worker_name = workers[int(id)]["worker_name"]

    if request.method == 'POST':
        if 'model' in request.files:
            file = request.files['model']
            file.save(os.path.join(MODEL_DIR, worker_name, file.filename))
    return id
                
                
    workers[int(id)]["updated_at"] = datetime.datetime.now()
    return id


def serve():
    app.run()
    
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
        start_new_thread(mainloop, ())
        serve()   
    except Exception as e:
        print(e)
        
    while True:
        pass