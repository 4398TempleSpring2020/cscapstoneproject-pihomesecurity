from Message.Imesssage import Imessage
from Message.Constant import Constant


class AlertMessage(Imessage):
    message_type = None
    alert_type = None

    def __init__(self, alert_type, message_type):
        self.alert_type = alert_type
        self.message_type = message_type

    def get_data(self):
        return self.alert_type

    def set_data(self, alert_data):
        if alert_data.alert_type == Constant.FACE_RECOGNIZED_ALERT or \
                alert_data.alert_type == Constant.FACE_NOT_RECOGNIZED_ALERT or alert_data.alert_type is None:
            self.alert_type = alert_data.alert_type

    def get_message_type(self):
        return self.message_type

    def set_message_type(self, message_type):
        if message_type == Constant.RESPONSE_MESSAGE or message_type == Constant.AlertMessage or \
                message_type == Constant.PROFILE_UPDATE_MESSAGE or message_type == Constant.CONFIGURE_SETTINGS_MESSAGE \
                or message_type == Constant.Arm_MESSAGE:
            self.message_type = message_type
