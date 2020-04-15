class IncidentData:
#AccountID, IncidentID, FriendlyMatchFlag , ImagePaths, MicrophonePath, UltrasonicPath
    def __init__(self, account_id, incident_id, match_flag, image_path, mic_path, sonic_path):
        self.account_id = account_id
        self.incident_id = incident_id
        self.match_flag = match_flag
        self.image_path = image_path # list of images
        self.mic_path = mic_path
        self.sonic_path = sonic_path

    def get_image_path(self):
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path

    def get_sensor_path(self):
        return self.sensor_path

    def set_sensor_path(self, path):
        self.sensor_path = path

    def get_account_id(self):
        return self.account_id


