import sqlite3
from config import INIT_BALANCE

def run_sql(sql: str):
    connection = sqlite3.connect("tickets.db")
    cursor = connection.cursor()

    try:
        result = cursor.execute(sql)
        connection.commit()
        return result
    except sqlite3.Error as error:
        print(f"Failed to run sql script: \n {sql} \n", error)
        return None

def init_database():
    print("Init database")
    run_sql(""" CREATE TABLE IF NOT EXISTS clients_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            in_time text,
            out_time text,
            price text,
            duration text
        )""")

    run_sql(""" CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address varchar(20) NOT NULL,
            balance REAL
        )""")
    
def save_client(ip_address: int, balance: float = None):
    if balance is None:
        balance = INIT_BALANCE
    
    ip_address = f"'{ip_address}'"
    SQL_CODE = f"""
        INSERT INTO clients (ip_address, balance) VALUES ({ip_address}, {balance});
    """        

    run_sql(SQL_CODE)

def get_all_clients() -> list:
    return list(run_sql("""
        SELECT * FROM clients;
    """))

def get_client_by_id(client_id: int) -> list:
    return list(run_sql(
        f"""SELECT * FROM clients WHERE id={client_id}"""
    ))

def update_client_balance(client_id: int, new_balance: float):
    run_sql(f"""
        UPDATE clients SET balance={new_balance} WHERE id={client_id};
    """)

def save_client_log(client_id, in_time: str, out_time: str = None , price: str =None, duration: str = None):    
    client_id = str(client_id)
    if out_time is None:
        out_time = "NULL"
    else:
        out_time = f"'{out_time}'"

    if price is None: 
        price = "NULL"
    else:
        price = f"'{price}'"

    if duration is None: 
        duration = "NULL"
    else:
        duration = f"'{price}'"

    in_time = f"'{in_time}'"
    client_id = f"'{client_id}'"

    run_sql(f"""
        INSERT INTO clients_logs (client_id, in_time, out_time, price, duration) VALUES ({client_id}, {in_time}, {out_time}, {price}, {duration})
    """)

def update_client_log(id: int, out_time: str, price: str, duration: str):
    run_sql(f"""
        UPDATE clients_logs 
        SET out_time='{out_time}', price='{price}', duration='{duration}'
        WHERE id={id};
    """)

def get_all_clients_logs() -> list:
    return list(run_sql("""
        SELECT * FROM clients_logs;
    """))    

def get_client_id_from_ip(client_ip: str):
    connection = sqlite3.connect("tickets.db")
    cursor = connection.cursor()
    SQL_CODE = f"SELECT * FROM clients WHERE ip_address = '{client_ip}'"
    cursor.execute(SQL_CODE)
    log_entries = cursor.fetchall()

    if log_entries:
        log_entry = log_entries[-1]
        return log_entry[0]
    else:
        return None

def client_exists_by_ip_address(client_ip: str):
    return get_client_id_from_ip(client_ip) is not None

def get_active_ride(client_id):
    return list(run_sql(f"""
        SELECT * FROM clients_logs WHERE client_id={client_id} AND out_time IS NULL;
    """))  
