# Kelvin Chris Lau, klau158, 9682466

import sys, os, queue, pickle, threading, time, atexit

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
        self.pipeList = []
        
        # FROM ROBERT'S LECTURES
        self.arrived_condition = threading.Condition()
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon = True)
        transfer_thread.start()
        
        # register clean up method
        atexit.register(self.cleanUp)

    # create child for other message procs
    def start(self, *args):
        pid = os.fork()
        if (pid == 0):
            self.main(*args)
            sys.exit()
        else:
            return pid
            
            
    # giving messages
    def give(self, pid, message, *values):
        
        pipePath = self.getPipePath(pid)
        
        # if we are giving to a new pipe/process
        if pid not in self.pipeList:
            # wait for it to be created
            while not os.path.exists(pipePath):
                time.sleep(0.001)
            
            # add it to the list of opened pipes
            self.pipeList.append(pid)
        else:
            # if it was once opened, but now the pipe is gone, return
            if not os.path.exists(pipePath):
                return
        
        pipe  = open(pipePath, "wb", buffering=0)
        pickle.dump((message, values), pipe)
        
    # receiving messages
    def receive(self, *args):
        
        # get the first TimeOut object, if it exists
        timeOutObj = None
        for arg in args:
            if arg.__class__.__name__ == "TimeOut":
                timeOutObj = arg
                break
        
        # the index of ANY, if it's there
        anyIndex = -1
        # keep track of progress in the messages list/queue
        i = 0
        
        # wait for first message
        if len(self.messages) == 0:
            # time.sleep(0.01)
            with self.arrived_condition: 
                # handle whether there is a timeout
                if timeOutObj is None:
                    self.arrived_condition.wait()
                else:
                    timedOut = self.arrived_condition.wait(timeOutObj.time)
                    if not timedOut:
                        return timeOutObj.action()
        
        # keep looping until a match (or timeout if it exists)
        while True:
            if len(self.messages) > i:
                received = self.messages[i]
                
                # compare with the filters
                for msgIndex, msg in enumerate(args):
                    # only if the arg is a Message object, and not a TimeOut
                    if msg.__class__.__name__ == "Message":
                        # keep track of ANY message if it is present
                        if msg.data == ANY:
                            anyIndex = msgIndex
                        else:
                            # perform the matching message's action
                            if received[0] == msg.data:
                                # only peform if guard is matched, else continue
                                if msg.guard():
                                    del self.messages[i]
                                    return msg.action(*received[1])
                
                # if index of any is -1, it was never "initialized"
                if not anyIndex == -1:
                    if args[anyIndex].guard():
                        del self.messages[i]
                        return args[anyIndex].action(*received[1])
                i += 1
            else:
                with self.arrived_condition: 
                    # print("wait")
                    if timeOutObj is None:
                        self.arrived_condition.wait()
                    else:
                        timedOut = self.arrived_condition.wait(timeOutObj.time)
                        if not timedOut:
                            return timeOutObj.action()
                    # print("done waiting")
                    
            # i += 1
                    
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
                 
    # clean up method for atexit       
    def cleanUp(self):
        try:
            os.remove(self.getPipePath(os.getpid()))
        except FileNotFoundError:
            pass

class Message():

    def __init__(self, data, action=lambda: None, guard=lambda: True):

        self.data = data
        self.guard = guard
        self.action = action

class TimeOut():

    def __init__(self, time, action):

        self.time = time
        self.action = action
