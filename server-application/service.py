import database_conn as db
import time
from config import INIT_BALANCE
from utils import count_price_and_duration

def client_exists(ip_address):
    if not db.client_exists_by_ip_address(ip_address):
        print(f"ADDING NEW CLIENT WITH IP: {ip_address}")
        db.save_client(ip_address, INIT_BALANCE)

def handle_ticket_usage(client_ip_address: str):
    print(f"HANDLE TICKET USAGE FOR CLIENT IP: {client_ip_address}")
    client_exists(client_ip_address)
    client_id = db.get_client_id_from_ip(client_ip_address)
    active_ride = db.get_active_ride(client_id)
    time_now = time.ctime()

    # if there is active ride then save out_time and price
    # else create new log
    if active_ride:
        active_ride = active_ride[0] # select first and only result
        time_in = active_ride[2]
        time_out = time_now
        (price, duration) = count_price_and_duration(time_in, time_out)
        db.update_client_log(client_id, time_out, price, duration)
        handle_payment(client_ip_address, -price)
    else:
        db.save_client_log(client_id, time_now)

def handle_payment(client_ip_address: str, payment_value: float):
    if(payment_value > 0):
        print(f"HANDLE PAYMENT FOR CLIENT IP: {client_ip_address}. VALUE: {payment_value}")
    
    client_exists(client_ip_address)
    client_id = db.get_client_id_from_ip(client_ip_address)
    client = db.get_client_by_id(client_id)[0]
    balance = float(client[2])
    balance += payment_value
    db.update_client_balance(client_id, balance)