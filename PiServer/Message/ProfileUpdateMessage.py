from PiServer.Constant import Constant
from PiServer.Message.Imesssage import Imessage


class ProfileUpdateMessage(Imessage):
    message_type = None
    update_type = None
    phone_number = None
    image_name = None
    image_array = None
    image_array_size = None

    def __init__(self, update_type, phone_number, image_name,image_array, image_array_size, message_type):
        self.update_type = update_type
        self.phone_number = phone_number
        self.image_name = image_name
        self.image_array = image_array
        self.image_array_size = image_array_size
        self.message_type = message_type

    def get_data(self):
        return self

    def set_data(self, profile_update_data):
        self.update_type = profile_update_data.update_type
        self.phone_number = profile_update_data.phone_number
        self.image_name = profile_update_data.image_name
        self.image_array = profile_update_data.image_array
        self.image_array_size = profile_update_data.image_array_size
        self.message_type = profile_update_data.message_type

    def get_message_type(self):
        return self.message_type

    def set_message_type(self, message_type):
        if message_type == Constant.RESPONSE_MESSAGE or message_type == Constant.AlertMessage or \
                message_type == Constant.PROFILE_UPDATE_MESSAGE or message_type == Constant.CONFIGURE_SETTINGS_MESSAGE \
                or message_type == Constant.Arm_MESSAGE:
            self.message_type = message_type
        else:
            self.message_type = None

    def get_update_type(self):
        return self.update_type

    def set_update_type(self, update_type):
        if update_type == Constant.PROFILE_ADD_MEMBER_FACE or update_type == Constant.PROFILE_ADD_MY_FACE or \
                update_type == Constant.PROFILE_ADD_NEW_MEMBER or update_type == Constant.PROFILE_REMOVE_MEMBER:
            self.update_type = update_type
        else:
            self.update_type = None
