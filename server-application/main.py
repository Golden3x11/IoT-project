from mqtt_client import Mqtt_Client
from database_conn import init_database

if __name__ == "__main__":
    init_database()
    mqtt_client = Mqtt_Client()
    mqtt_client.connect_to_broker()
    while True:
        pass