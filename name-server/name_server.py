from process_message_system import *

class NameServer(MessageProc):
    
    # set up communication, use separate thread for reading from own pipe
    def main(self, *args):
        self.pipePath = "/tmp/pipe_name_server"
        if not os.path.exists(self.pipePath):
            os.mkfifo(self.pipePath)
        # incoming messages
        self.messages = []
        # open pipes
        self.pipeList = []
        
        # use dictionary/map for storage of addresses for names
        self.addressBook = {}
        
        # FROM ROBERT'S LECTURES
        self.arrived_condition = threading.Condition()
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon = True)
        transfer_thread.start()
        
        # register clean up method
        atexit.register(self.cleanUp)
        
        # TODO: while true, keep receiving messages like register, get, stop?
        while True:
            self.receive(
                Message(
                    'register',
                    action=lambda name, pid: self.register(name, pid)),
                Message(
                    'get',
                    action=lambda name, returnPid: self.give(returnPid, "response", self.getPid(name))),
                Message(
                    'stop',
                    action=lambda : self.finish))
        
    def register(self, name, pid):
        print("registering", name, pid)
        self.addressBook[name] = pid
        
    def getPid(self, name):
        return self.addressBook[name]
        
    def finish(self):
        sys.exit()
        
    # ADAPTED FROM ROBERT'S LECTURES
    def extract_from_pipe(self):
        pipePath = self.pipePath
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
            os.remove(self.pipePath)
        except FileNotFoundError:
            pass
        
if __name__ == "__main__":
    NameServer().main()