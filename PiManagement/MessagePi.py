class MessagePi:

    def __init__(self,arm,resp,panic):
        if(arm ==1 or arm ==9):
            self.arm = arm
        #else:
            #log invalid arm parameter
        if(resp ==1 or resp==9):
            self.resp = resp
        #else:
            #log invalid reponse parameter
        if(panic==True or panic==False):
            self.panic = panic
        #else:
            #log invalid: panic must be a boolean

    def get_arm(self):
        return self.arm

    def get_resp(self):
        return self.resp

    def get_panic(self):
        return self.panic
