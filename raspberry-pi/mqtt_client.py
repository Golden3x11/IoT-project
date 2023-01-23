import paho.mqtt.client as mqtt
from config_pi import BROKER_IP, QOS


class Mqtt_Client():
    def __init__(self):
        self.client = mqtt.Client()
        self.broker_ip = BROKER_IP
        self.logs = []
        print("Created MQTT Client instance.")

    def connect_to_broker(self):
        self.client.connect(self.broker_ip, port=1833)
        self.client.on_message = self.process_message
        self.client.loop_start()
        self.client.subscribe("tickets/request/")
        print("Connected to broker.")

    def connect_to_broker_client(self):
        self.client.connect(self.broker_ip)
        # self.client.on_message = self.process_message_client
        # self.client.loop_start()
        # self.client.subscribe("tickets/response/")
        print("Connected to broker.")


    def disconnect_from_broker(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from broker.")


    def process_message(self, client, userdata, message):
        # TODO: jakies przetworzenie tej wiadomosci ale nie wiem jak wyglada wiadomosc
        print(message)

    def process_message_client(self, client, userdata, message):
        # TODO: jakies przetworzenie tej wiadomosci ale nie wiem jak wyglada wiadomosc
        print(message)

    def send_response_to_client(self, client_ip, time, msg=None):
        if msg is None:
            self.client.publish(f"tickets/response/{client_ip}", f"{time}")
        else:
            self.client.publish(f"tickets/response/{client_ip}", f"{time}@{msg}")

    def send_message_to_server(self, time, msg=None):
        payload = f'{msg}:{time}' # tutaj trzeba zobaczyc jak to sie wysyla
        self.client.publish(f"tickets/request/", payload)
