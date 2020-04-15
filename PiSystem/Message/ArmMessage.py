from PiSystem.Constant import Constant
from PiSystem.Message.Imesssage import Imessage


class ArmMessage(Imessage):
    message_type = None
    arm_type = None
# 1 arm
# 0 disarm

    def __init__(self, arm_type, message_type):
        self.arm_type = arm_type
        self.message_type = message_type

    def get_data(self):
        return self

    def set_data(self, arm_data):
        if arm_data.alert_type == Constant.FACE_RECOGNIZED_ALERT or \
                arm_data.alert_type == Constant.FACE_NOT_RECOGNIZED_ALERT or arm_data.alert_type is None:
            self.arm_type = arm_data.arm_type

    def get_message_type(self):
        return self.message_type

    def set_message_type(self, message_type):
        if message_type == Constant.RESPONSE_MESSAGE or message_type == Constant.AlertMessage or message_type == Constant.PROFILE_UPDATE_MESSAGE or \
                message_type == Constant.CONFIGURE_SETTINGS_MESSAGE or message_type == Constant.Arm_MESSAGE:
            self.message_type = message_type
        else:
            self.message_type = None

    def get_arm_status(self):
        return self.arm_type

    def set_arm_status(self, status):
        self.arm_type = status

