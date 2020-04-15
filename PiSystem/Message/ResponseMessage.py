from PiSystem.Constant import Constant
from PiSystem.Message.Imesssage import Imessage


class ResponseMessage(Imessage):
    message_type = None

    bool_is_safe = None

    def __init__(self, is_safe, message_type):
        self.is_safe = is_safe
        self.message_type = message_type

    def get_data(self):
        return self

    def set_data(self, response_data):
        if (response_data.bool_is_safe is True) or \
                (response_data.bool_is_safe is False) or \
                (response_data.bool_is_safe is None):
            self.bool_is_safe = response_data.bool_is_safe

    def get_message_type(self):
        return self.bool_is_safe

    def set_message_type(self, message_type):
        if message_type == Constant.RESPONSE_MESSAGE or message_type == Constant.AlertMessage or message_type == Constant.PROFILE_UPDATE_MESSAGE or \
                message_type == Constant.CONFIGURE_SETTINGS_MESSAGE or message_type == Constant.Arm_MESSAGE:
            self.message_type = message_type

    def get_is_safe_status(self):
        return self.bool_is_safe

    def set_is_safe_status(self, status):
        if (status is True) or (status is False) or (status is None):
            self.is_safe = status
