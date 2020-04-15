from abc import ABCMeta, abstractmethod


class Imessage(metaclass=ABCMeta):

    @property
    @abstractmethod
    def message_type(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def set_data(self, data):
        pass

    @abstractmethod
    def get_message_type(self):
        pass

    @abstractmethod
    def set_message_type(self, data_type):
        pass
