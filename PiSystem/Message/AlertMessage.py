from PiSystem.Message.Imesssage import Imessage


class AlertMessage(Imessage):
    message_type = None
    alert_type = None

    def __init__(self, alert_type, message_type):
        self.alert_type = alert_type
        self.message_type = message_type

    def get_data(self):
        return self.alert_type

    def set_data(self, alert_data):
        self.alert_type = alert_data.alert_type
        self.message_type = alert_data.message_type

    def get_message_type(self):
        return self.message_type

    def set_message_type(self, message_type):
        self.message_type = message_type
