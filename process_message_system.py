import sys, os, queue, pickle, threading, time

# define ANY as 'any'
ANY = 'any'

class MessageProc():

    # set up communication, use separate thread for reading from own pipe
    def main(self, *args):
        pipePath = self.getPipePath(os.getpid())
        if not os.path.exists(pipePath):
            os.mkfifo(pipePath)
        # incoming messages
        self.messages = []
        # open pipes
        self.pipeMap = {}
        
        # FROM ROBERT'S LECTURES
        self.arrived_condition = threading.Condition()
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon = True)
        transfer_thread.start()

    # create child for other message procs
    def start(self, *args):
        pid = os.fork()
        if (pid == 0):
            self.main(*args)
        else:
            return pid

    def give(self, pid, message, *values):
        
        pipePath = self.getPipePath(pid)
        
        # TODO: swap for time.sleep(0.01) later
        time.sleep(0.001)
        # isExisting = os.path.exists(pipePath)
        # while not isExisting:
        #     isExisting = os.path.exists(pipePath)
        
        # store opened pipes. try to access pipe first...
        # if not there, create it
        try:
            pipe = self.pipeMap[pid]
        except KeyError:
            pipe  = open(pipePath, "wb")
            self.pipeMap[pid] = pipe
        
        # pipe = self.pipeMap.get(pid)
        
        # if pipe == None:
        #     pipe  = open(pipePath, "wb")
        #     self.pipeMap[pid] = pipe
        
        # pipe  = open(pipePath, "wb")
        # self.pipeMap[pid] = pipe
        
        pickle.dump((message, values), pipe)

    def receive(self, *args):
        
        # TODO: get first timeout, and use timeout time in wait
        # ignore timeout while looping?
        
        anyIndex = -1
        
        while True:
            
            print(args[0].data)
            
            for i, received in enumerate(self.messages):
                # retVal = None
                # action = False
                for msgIndex, msg in enumerate(args):
                    if msg.data == ANY:
                        anyIndex = msgIndex
                    else:
                        if received[0] == msg.data:
                            # retVal = msg.action(*received[1])
                            # action = True
                            # break
                            del self.messages[i]
                            return msg.action(*received[1])
                
                # if not anyIndex == -1 and not action:
                if not anyIndex == -1:
                    # retVal = args[anyIndex].action(*received[1])
                    # action = True
                    del self.messages[i]
                    return args[anyIndex].action(*received[1])
                    
                # if action:
                #     del self.messages[i]
                #     return retVal
                    
            with self.arrived_condition:
                self.arrived_condition.wait()
        
    # get a named pipe path with an integer pid
    def getPipePath(self, pid):
        return "/tmp/pipe" + str(pid)
    
	# ADAPTED FROM ROBERT'S LECTURES
    def extract_from_pipe(self):
        pipePath = self.getPipePath(os.getpid())
        with open(pipePath, 'rb') as pipe_rd:
            while True:
                try:
                    message = pickle.load(pipe_rd)
                    with self.arrived_condition:
                        self.messages.append(message)
                        self.arrived_condition.notify() #wake up waiters
                except EOFError:
                    #When the file hasn't been opened to write yet
                    time.sleep(0.01)
                        

class Message():

    def __init__(self, data, action, guard=lambda: True):

        self.data = data
        self.action = action
        self.guard = guard

class TimeOut():

    def __init__(self, time, action):

        self.time = time
        self.action = action
