import threading
from BrickPi import *

##
# A class to start a thread that manage al the Bricpi taskes
##

class BrickPi_Thread:
    # Store the engines of the brickpi
    # Store the sensors of the brickpi
    # The thread is not yet going
    # There is no reference to a thread
    def __init__(self,engines):
        self.__engines = engines
        self.__going = False
        self.__thread = None
    # Turn the thread on
    # If the thread is already on, notthing happens
    # Else the thread is going and daemonised thread is started,
    # a reference to this thread is saved
    def on(self):
        if self.__thread == None:
            self.__going = True
            self.__thread = threading.Thread(target=self.thread)
            self.__thread.setDaemon('True')
            self.__thread.start()
        else:
            print 'First turn the ongoing thread off'
    # Turn the thread back off
    # If there is a thread it is no longer going
    def off(self):
        if self.__thread != None:
            self.__going = False
            self.__thread.join()
            self.__thread = None
        else:
            print 'No thread to turn off'
    # The actual thread that will run
    def thread(self):
        # WHILE the treath is running
        # update values of the engines
        while self.__going:
            for i in self.__engines:
                i.pulse()
            BrickPiUpdateValues()
            time.sleep(0.01)
