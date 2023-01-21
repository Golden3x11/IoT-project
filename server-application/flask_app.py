from flask import Flask, render_template, redirect
import database_conn as db
from utils import value_or_question_mark

app = Flask(__name__)

@app.route("/")
def main_page():
    return redirect("/clients")

def log_to_dto(log):
    return {
        'id': log[0],
        'client_id': log[1],
        'in_time': log[2],
        'out_time': value_or_question_mark(log[3]),
        'price': value_or_question_mark(log[4]),
        'duration': value_or_question_mark(log[5])
    }

@app.route("/logs")
def logs_page():
    logs = map(log_to_dto, db.get_all_clients_logs())
    return render_template('logs.html.j2', logs=logs)

def client_to_dto(client):
    return {
        'id': client[0],
        'ip_address': client[1],
        'balance': client[2] 
    }

@app.route("/clients")
def clients_page():
    clients = map(client_to_dto, db.get_all_clients())
    print(clients)
    return render_template('clients.html.j2', clients=clients)