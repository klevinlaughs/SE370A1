import sys, os, queue, pickle

ANY = 'any'

# get a named pipe path with an integer pid
def getPipePath(pid):
    return "/tmp/pipe" + str(pid)


class MessageProc():

    def main(self, *args):
        pipePath = getPipePath(os.getpid())
        if not os.path.exists(pipePath):
            os.mkfifo(pipePath)
        # print("main:", os.getpid())
        self.queue = queue.Queue()

    def start(self, *args):
        pid = os.fork()
        if (pid == 0):
            self.main(*args)
        else:
            return pid

    def give(self, pid, message, *values):
        
        pipePath = getPipePath(pid)
        isExisting = os.path.exists(pipePath)
        # print("/tmp/pipe" + str(pid))
        while not isExisting:
            isExisting = os.path.exists(pipePath)
            # print(isExisting)
            
        pipe = open(pipePath, "wb")
        pickle.dump({message, values}, pipe)
        pipe.close()

    def receive(self, *args):
        print("receiving...")
        # something = self.queue.get()
        # pickle.load()


class Message():

    def __init__(self, data, action, guard=lambda: True):

        self.data = data
        self.action = action
        self.guard = guard


class TimeOut():

    def __init__(self, time, action):

        self.time = time
        self.action = action
