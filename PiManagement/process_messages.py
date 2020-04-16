

from queue import Queue

from PiServer.MessagePi import MessagePi
from PiServer.StateStatusPi import StateStatusPi

def process_arm_sys(message, sysS):
    if(sysS.get_armS()==1 or sysS.get_armS()==0):
        # start sensor manager thread listening
        sysS.set_armS(9)
    #else:
        # possibly log that already was armed

def process_disarm_sys(message,sysS):
    if(sysS.get_armS()==9):
        sysS.set_armS(1)  #system disarmed
        #sensorManager doesn't create incidents


def escalate_alert(message,sysS):
    if (sysS.get_armS()==9 and sysS.getlevelS == 5):
        sysS.set_levelS(9)
        #police.notify()
        #sound.stop(beep)
        #sound.start(siren)
    #elif (sysS.get_arms()==9 and sysS.get_levelS()==1):
        #log that can't escalate from armed but no alert status
    #elif (sysS.get_armS()==9 and sysS.get_levelS()==9):
        #log that has already been escalated
    #else:
        #log ERROR: not a vaild state/status to call escalate


def resolve_alert(message,sysS):
    if (sysS.get_armS()==9 and sysS.getlevelS !=1):
        sysS.set_levelS(1)
        #sound.stop(beep)
        #sound.stop(siren)
        #stays armed

    # if the resolve message also takes down a panic alert, keep this code, otherwise comment out
    elif (sysS.get_armS() == 9) and (sysS.getlevelS() == 9) and (sysS.get_panicS() == True):
        sysS.set_levelS(1)
        sysS.set_panicS(False)
        # sound.stop(beep)
        # sound.stop(siren)
        # stays armed

    #else:
        #log that not a valid state to resolve from

def panic_alert(message,sysS):

    if not (sysS.get_panicS() == True):
        sysS.set_levelS(9)
        sysS.set_armS(9)
        sysS.set_panicS(True)
        #police.notify()
        #sound.stop(beep)
        #sound.start(siren)
        #sensorManager to record
    #else:
        #log that already a panic alert in progress


def process_messages(q):

    sysS = StateStatusPi()  # when first starts up sets to default (disarmed, no response, panic is False)
    while(not q.empty()):

        message = q.get()
        if message.arm == 9:
            process_arm_sys(message,sysS)
        elif message.arm ==1:
            process_disarm_sys(message,sysS)
        elif message.resp==1:
            resolve_alert(message,sysS)
        elif message.resp==9:
            escalate_alert(message,sysS)
        elif message.panic:
            panic_alert(message,sysS)


def main():     #for testing the Queue and processing

    mess_q = Queue()
    m1 = MessagePi(9,0)  # arm the system
    mess_q.put(m1)
    m2 = MessagePi(9,0)  # another user tried to arm very close in time to first message
    mess_q.put(m2)
    #sleep for some time to let system be armed
    m3 = MessagePi(1,0)  # user disarms the system
    #sleep for seconds
    m4 = MessagePi(0,0,True) # panic button pressed in app
    # show that police notified, state changes and siren sounds
    m5 = MessagePi(0,1) # does this resolve a panic button alarm as well?



if __name__ == '__main__':
    main()


#********* THE IMPORTED QUEUE IMPLEMENTATION'S FUNCTIONS ****************
# maxsize – Number of items allowed in the queue.
# empty() – Return True if the queue is empty, False otherwise.
# full() – Return True if there are maxsize items in the queue. If the queue was initialized with maxsize=0 (the default), then full() never returns True.
# get() – Remove and return an item from the queue. If queue is empty, wait until an item is available.
# get_nowait() – Return an item if one is immediately available, else raise QueueEmpty.
# put(item) – Put an item into the queue. If the queue is full, wait until a free slot is available before adding the item.
# put_nowait(item) – Put an item into the queue without blocking.
# qsize() – Return the number of items in the queue. If no free slot is immediately available, raise QueueFull.