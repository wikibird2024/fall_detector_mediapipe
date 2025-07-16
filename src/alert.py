class Alert:
    def __init__(self, config):
        self.method = config.get("alert_method", "console")

    def trigger(self, message):
        if self.method == "console":
            print(f"[ALERT] {message}")
        # Extend with SMS, email, MQTT, etc.
