import threading
import time
import requests
from Constant import Constant


class TimerCountdownThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources
    
    def run(self):
        auto_escalate = True
        for i in range(300): #300 seconds in 5 minutes
            if self.shared_resources.response_received == True:
                auto_escalate = False
                break; 
            sleep(1)
        #if auto_escalate == True:
            #do auto-escalation stuff here