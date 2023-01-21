#!/usr/bin/env python3

# pylint: disable=no-member

import time
from datetime import datetime

import RPi.GPIO as GPIO
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont
from mfrc522 import MFRC522

from config_pi import *  # pylint: disable=unused-wildcard-import
from mqtt_client import Mqtt_Client

executing = True
encoderLeftPreviousState = GPIO.input(encoderLeft)
encoderRightPreviousState = GPIO.input(encoderRight)
client = Mqtt_Client()
is_money_transfer = False
price = 5

disp = SSD1331.SSD1331()


def greenButtonPressedCallback(channel):
    global is_money_transfer
    is_money_transfer = True
    displayLED()


def redButtonPressedCallback(channel):
    global is_money_transfer, price
    is_money_transfer = False
    price = 5
    displayLED()


def buzzer_state(state):
    GPIO.output(buzzerPin, not state)  # pylint: disable=no-member


def buzzer():
    buzzer_state(True)
    time.sleep(1)
    buzzer_state(False)


def blink():
    GPIO.output(led1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led1, GPIO.LOW)
    time.sleep(1)


def rfidRead():
    global executing
    global is_money_transfer
    MIFAREReader = MFRC522()
    is_scanned = 0
    while executing:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK and is_scanned <= 1:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            last = is_scanned
            is_scanned = 2
            if status == MIFAREReader.MI_OK and last <= 0:
                dt = datetime.now()
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)

                if is_money_transfer:
                    send_message_to_broker(dt, uid, price)
                    is_money_transfer = False
                    displayLED()
                else:
                    send_message_to_broker(dt, uid)

                buzzer()
                blink()
        else:
            is_scanned -= 1


def turn_encoder(channel):
    global is_money_transfer
    if is_money_transfer:
        global encoderLeftPreviousState
        global encoderRightPreviousState
        global price
        encoder_left_current_state = GPIO.input(encoderLeft)
        encoder_right_current_state = GPIO.input(encoderRight)

        if (encoderLeftPreviousState == 1 and encoder_left_current_state == 0 and price < 100):
            price += 5
        if (encoderRightPreviousState == 1 and encoder_right_current_state == 0 and price > 0):
            price -= 5

        encoderLeftPreviousState = encoder_left_current_state
        encoderRightPreviousState = encoder_right_current_state


def displayLED():
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 13)

    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)

    if is_money_transfer:
        draw.text((8, 0), "Welcome!!", font=fontSmall, fill="BLACK")
        draw.text((12, 40), "EagleMPK", font=fontSmall, fill="BLACK")
    else:
        draw.text((8, 0), "Money Transfer", font=fontSmall, fill="BLACK")
        draw.text((12, 40), f"{price} $", font=fontSmall, fill="BLACK")
    disp.ShowImage(image1, 0, 0)


def send_message_to_broker(d_time, uid, price_current=None):
    if is_money_transfer:
        msg = f"T:{price_current}:{uid}"
        client.send_message_to_server(d_time, msg)
        global price
        price = 5
    else:
        client.send_message_to_server(d_time, msg="I/O:" + uid)


def start():
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=greenButtonPressedCallback, bouncetime=200)
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonPressedCallback, bouncetime=200)

    GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=turn_encoder, bouncetime=100)
    GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=turn_encoder, bouncetime=100)

    client.connect_to_broker_client()
    rfidRead()
    client.disconnect_from_broker()


if __name__ == "__main__":
    start()
    GPIO.cleanup()  # pylint: disable=no-member
