import sys, os, queue, pickle

class MessageProc():
    
    def main(self, *args):
        os.mkfifo("/tmp/pipe" + str(os.getpid()))
        print(os.getpid())
        self.queue = queue.Queue()
        
    def start(self, *args):
        pid = os.fork()
        if (pid == 0):
            self.main()
        else:
            return pid
        
    def give(self, pid, message, value):
        pipe = open("/tmp/pipe" + str(pid))
        pickle.dump({message, value}, pipe)
        
    def receive(self, *args):
        
        something = self.queue.get()
        #pickle.load()
        
        
class Message():
    
    def __init__(self, data, action, guard = None):
        
        self.data = data
        self.action = action
        self.guard = guard
        
class TimeOut():
    
    def __init__( self, time, action):
        
        self.time = time
        self.action = action