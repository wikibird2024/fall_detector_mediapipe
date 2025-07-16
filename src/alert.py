import json

import paho.mqtt.client as mqtt
import requests
from twilio.rest import Client


class Alert:
    def __init__(self, config):
        self.method = config.get("alert_method", "console")
        self.config = config

        if self.method == "mqtt":
            mqtt_config = config.get("mqtt", {})
            self.mqtt_client = mqtt.Client()
            try:
                self.mqtt_client.connect(
                    mqtt_config.get("broker", "localhost"),
                    mqtt_config.get("port", 1883),
                    keepalive=60,
                )
            except Exception as e:
                print(f"[MQTT ERROR] Could not connect to broker: {e}")
                self.method = "console"  # fallback

        elif self.method == "sms":
            sms_config = config.get("sms", {})
            try:
                self.twilio_client = Client(
                    sms_config.get("account_sid"), sms_config.get("auth_token")
                )
                self.sms_from = sms_config.get("from_number")
                self.sms_to = sms_config.get("to_number")
            except Exception as e:
                print(f"[SMS ERROR] Twilio setup failed: {e}")
                self.method = "console"

        elif self.method == "telegram":
            tg_config = config.get("telegram", {})
            self.bot_token = tg_config.get("bot_token")
            self.chat_id = tg_config.get("chat_id")
            if not self.bot_token or not self.chat_id:
                print("[TELEGRAM ERROR] Missing token or chat_id")
                self.method = "console"

    def trigger(self, message):
        try:
            if self.method == "console":
                print(f"[ALERT] {message}")

            elif self.method == "mqtt":
                topic = self.config["mqtt"]["topic"]
                self.mqtt_client.publish(topic, message)
                print(f"[MQTT] Message sent to {topic}")

            elif self.method == "sms":
                self.twilio_client.messages.create(
                    body=message, from_=self.sms_from, to=self.sms_to
                )
                print(f"[SMS] Message sent to {self.sms_to}")

            elif self.method == "telegram":
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                payload = {"chat_id": self.chat_id, "text": message}
                requests.post(url, json=payload)
                print("[TELEGRAM] Message sent.")

        except Exception as e:
            print(f"[ALERT ERROR] Failed to send alert via {self.method}: {e}")
            print("[FALLBACK] Logging to console")
            print(f"[ALERT] {message}")
