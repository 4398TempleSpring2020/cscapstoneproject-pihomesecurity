import threading


class MessageHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources

    def run(self):
        while True:
            #print("q size: " + str(len(self.shared_resources.message_q)))
            self.shared_resources.q_lock.acquire()
            while len(self.shared_resources.message_q) > 0:
                message = self.shared_resources.message_q.pop()
                print("message received: " + message)
                if message == "ARM" and self.shared_resources.is_armed is False:
                    self.shared_resources.is_armed = True
                    break
                if message == "DISARM" and self.shared_resources.is_armed is True:
                    self.shared_resources.is_armed = False
                    self.shared_resources.is_ongoing_threat = False
                    break
                if message == "RESOLVE" and self.shared_resources.is_ongoing_threat is True:
                    self.shared_resources.is_ongoing_threat = False
                    break
                if message == "ESCALATE" and self.shared_resources.is_ongoing_threat is True:
                    # contact police?  # signal speaker? send alerts to mobile? record incident?
                    break
                if message == "ESCALATE" and self.shared_resources.is_ongoing_threat is False:
                    # contact police?  # signal speaker? send alerts to mobile? record incident?
                    self.shared_resources.is_ongoing_threat = True
                    break
                if message == "PANIC":
                    # contact police?  # signal speaker? send alerts to mobile? record incident?
                    self.shared_resources.is_ongoing_threat = True
                    break
            self.shared_resources.q_lock.release()

