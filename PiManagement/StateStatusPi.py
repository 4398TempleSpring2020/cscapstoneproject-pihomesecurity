class StateStatusPi:

    def __init__(self, armS=1, levelS=0, panicS=False):
        self.armS = armS       #0 on boot, 1 is disarmed, 9 is armed
        self.levelS = levelS   #0 on boot, 1 is listening (no alert but is armed), 5 is beep alert, 9 is high alert
        self.panicS = panicS   #False unless somebody sent a panic button pressed message

    def set_armS(self,armS):
        if(armS == 1 or armS ==9):
            self.armS = armS

    def set_levelS(self,levelS):
        if (levelS == 1 or levelS ==5 or levelS ==9):
            self.levelS = levelS

    def set_panicS(self,panicS):
        if (panicS == True or panicS == False):
            self.panicS = panicS

    def get_armS(self):
        return self.armS

    def get_levelS(self):
        return self.levelS

    def get_panicS(self):
        return self.panicS