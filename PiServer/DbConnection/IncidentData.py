class IncidentData:

    def __init__(self, account_id, image_path, sensor_path):
        self.image_path = image_path
        self.sensor_path = sensor_path
        self.account_id = account_id

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


