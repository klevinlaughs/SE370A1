import sys, os, queue, pickle

ANY = 'any'


class MessageProc():

    def main(self, *args):
        os.mkfifo("/tmp/pipe" + str(os.getpid()))
        # print("main:", os.getpid())
        self.queue = queue.Queue()

    def start(self, *args):
        pid = os.fork()
        if (pid == 0):
            self.main(*args)
        else:
            return pid

    def give(self, pid, message, *values):
        isExisting = os.path.exists("/tmp/pipe" + str(pid))
        # print("/tmp/pipe" + str(pid))
        while not isExisting:
            isExisting = os.path.exists("/tmp/pipe" + str(pid))
            # print(isExisting)

        pipe = open("/tmp/pipe" + str(pid))
        pickle.dump({message, values}, pipe)
        pipe.close()

    def receive(self, *args):

        something = self.queue.get()
        # pickle.load()


class Message():

    def __init__(self, data, action, guard=None):

        self.data = data
        self.action = action
        self.guard = guard


class TimeOut():

    def __init__(self, time, action):

        self.time = time
        self.action = action
