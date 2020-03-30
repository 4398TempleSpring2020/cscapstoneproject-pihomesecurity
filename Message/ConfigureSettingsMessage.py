from Message.Constant import Constant
from Message.Imesssage import Imessage


class ConfigureSettingsMessage(Imessage):
    message_type = None
    bool_contact_police_on_threat_escalated_protocol = None
    bool_contact_police_on_no_reply_protocol = None
    bool_receive_face_recognized_alert_message_protocol = None
    bool_notify_all_when_threat_escalated_protocol = None
    bool_only_archive_face_not_recognized_data_protocol = None

    def __init__(self, bool_contact_police_on_threat_escalated_protocol, bool_contact_police_on_no_reply_protocol,
                 bool_receive_face_recognized_alert_message_protocol, bool_notify_all_when_threat_escalated_protocol,
                 bool_only_archive_face_not_recognized_data_protocol, message_type):
        self.bool_contact_police_on_threat_escalated_protocol = bool_contact_police_on_threat_escalated_protocol
        self.bool_contact_police_on_no_reply_protocol = bool_contact_police_on_no_reply_protocol
        self.bool_receive_face_recognized_alert_message_protocol = bool_receive_face_recognized_alert_message_protocol
        self.bool_notify_all_when_threat_escalated_protocol = bool_notify_all_when_threat_escalated_protocol
        self.bool_only_archive_face_not_recognized_data_protocol = bool_only_archive_face_not_recognized_data_protocol

        self.message_type = message_type

    def get_data(self):
        return self

    def set_data(self, configure_settings_data):
        # null check
        self.bool_contact_police_on_threat_escalated_protocol = \
            configure_settings_data.bool_contact_police_on_threat_escalated_protocol
        self.bool_contact_police_on_no_reply_protocol = \
            configure_settings_data.bool_contact_police_on_no_reply_protocol
        self.bool_receive_face_recognized_alert_message_protocol = \
            configure_settings_data.bool_receive_face_recognized_alert_message_protocol
        self.bool_notify_all_when_threat_escalated_protocol = \
            configure_settings_data.bool_notify_all_when_threat_escalated_protocol
        self.bool_only_archive_face_not_recognized_data_protocol = \
            configure_settings_data.bool_only_archive_face_not_recognized_data_protocol

    def get_message_type(self):
        return self.message_type

    def set_message_type(self, message_type):
        if message_type == Constant.RESPONSE_MESSAGE or message_type == Constant.AlertMessage \
                or message_type == Constant.PROFILE_UPDATE_MESSAGE or \
                message_type == Constant.CONFIGURE_SETTINGS_MESSAGE or message_type == Constant.Arm_MESSAGE:
            self.message_type = message_type

    # null check
    # protocol 1
    def get_bool_contact_police_on_threat_escalated_protocol(self):
        return self.bool_contact_police_on_threat_escalated_protocol

    def set_bool_contact_police_on_threat_escalated_protocol(self, data):
        self.bool_contact_police_on_threat_escalated_protocol = data

    # protocol 2

    def get_bool_contact_police_on_no_reply_protocol(self):
        return self.bool_contact_police_on_no_reply_protocol

    def set_bool_contact_police_on_no_reply_protocol(self, data):
        self.bool_contact_police_on_no_reply_protocol = data

    # protocol 3
    def get_bool_receive_face_recognized_alert_message_protocol(self):
        return self.bool_receive_face_recognized_alert_message_protocol

    def set_bool_receive_face_recognized_alert_message_protocol(self, data):
        self.bool_receive_face_recognized_alert_message_protocol = data

    # protocol 4
    def get_bool_notify_all_when_threat_escalated_protocol(self):
        return self.bool_notify_all_when_threat_escalated_protocol

    def set_bool_notify_all_when_threat_escalated_protocol(self, data):
        self.bool_notify_all_when_threat_escalated_protocol = data

    # protocol 5
    def get_bool_only_archive_face_not_recognized_data_protocol(self):
        return self.bool_only_archive_face_not_recognized_data_protocol

    def set_bool_only_archive_face_not_recognized_data_protocol(self, data):
        self.bool_only_archive_face_not_recognized_data_protocol = data
