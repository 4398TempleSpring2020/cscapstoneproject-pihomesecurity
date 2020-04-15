#!usr/bin/python3

from abc import ABCMeta, abstractmethod

class sensor_interface(metaclass=ABCMeta):    
    @classmethod
    def __subclasshook(cls, subclass):
        return (hasattr(subclass, 'initiate')
               and callable(subclass.initiate)
               and hasattr(subclass, 'connect')
               and callable(subclass.connect)
               and hasattr(subclass, 'test')
               and callable(subclass.test)
               and hasattr(subclass, '__init__')
               and callable(subclass.__init__)
               and hasattr(subclass, 'isActive')
               and hasattr(subclass, 'duration')
               and hasattr(subclass, 'frequency')
               or NotImplemented)
    
    @abstractmethod
    def initiate(self, thread_list):
        raise NotImplementedError

    @abstractmethod
    def __init__(self, duration, frequency):
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        raise NotImplementedError
        pass
    
    @abstractmethod
    def test(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def isActive(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def duration(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def frequency(self):
        raise NotImplementedError
