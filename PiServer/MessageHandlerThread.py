import threading
import time


class MessageHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources

    def run(self):
        while True:
            
            
            if len(self.shared_resources.message_q) > 0:
                with self.shared_resources.q_lock:
                    print("Message Handler aquired lock and something in queue")
                    
                    message = self.shared_resources.message_q.pop()
                    print("message received: " + message)

                    if message == "ARM":
                        if self.shared_resources.is_armed is False:
                            self.shared_resources.is_armed = True
                            print("\tResources Set:\tIs Armed: ",self.shared_resources.is_armed)
                            self.shared_resources.is_active_incident = False   # on arming from a disarmed state set to false
                            print("\tResources Set:\tIs Active Incident: ", self.shared_resources.is_active_incident)
                            
                        elif self.shared_resources.is_armed is True:
                            print("** DISREGARD MESAGE ** system already was armed")
                            
                    elif message == "DISARM":
                        if self.shared_resources.is_armed is True:
                            self.shared_resources.is_armed = False
                            print("\tResources Set:\tIs Armed: ", self.shared_resources.is_armed)
                            self.shared_resources.is_active_incident = False
                            print("\tResources Set:\tIs Acive Incident: ", self.shared_resources.is_active_incident)
                         
                        elif self.shared_resources.is_armed is False:
                            print("** DISREGARD MESAGE ** system already disarmed")
                          

                    elif message == "RESOLVE":
                        if self.shared_resources.is_active_incident is True:
                            self.shared_resources.is_active_incident = False
                            print("\tResources Set:\tIs Active Incident: ",self.shared_resources.is_active_incident)
                            self.shared_resources.is_armed = False
                            print("\tResources Set:\tIs Armed: ", self.shared_resources.is_armed)
                        elif self.shared_resources.is_active_incident is False:
                            print("** DISREGARD MESAGE ** no active incident")
                        

                    elif message == "ESCALATE":
                        if self.shared_resources.is_active_incident is True:
                            if self.shared_resources.is_max_alert is False:
                                self.shared_resources.is_max_alert = True
                                print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                                # contact police
                                # stop beep
                                # start siren
                            

                            elif self.shared_resources.is_max_alert is True:
                                print("** DISREGARD MESAGE ** already was escalated/Max Alert -- Police Notified")
                            
                        elif self.shared_resources.is_active_incident is False: # case of panic from non active alert or disarm state
                            self.shared_resources.is_active_incident = True
                            print("\tResources Set:\tIs Active Incident: ", self.shared_resources.is_max_alert)
                            self.shared_resources.is_max_alert = True
                            print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                            # contact police
                            # stop beep
                            # play siren
                        

                    elif message == "PANIC":
                        self.shared_resources.is_active_incident = True
                        print("\tResources Set:\tIs Active Incident: ", self.shared_resources.is_max_alert)
                        self.shared_resources.is_max_alert = True
                        print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                        # contact police
                        # stop beep
                        # play siren
                print("MessageHandler giving up lock end of loop")
                #self.shared_resources.q_lock.release()
          
