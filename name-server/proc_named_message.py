from process_message_system import *

# class with some reused methods
class NamedMessageProc(MessageProc):
        
    # custom give for registering on the name server
    def registerOnNameServer(self, name):
        pipePath = "/tmp/pipe_name_server"
        
        # wait for it to be created
        while not os.path.exists(pipePath):
            time.sleep(0.001)
            
        values = (name, os.getpid())
        
        pipe  = open(pipePath, "wb", buffering=0)
        pickle.dump(("register", values), pipe)
        
    # get pid from name server, and return it to sender
    def getProcPid(self, name, returnPid):
        pipePath = "/tmp/pipe_name_server"
        
        # wait for it to be created
        while not os.path.exists(pipePath):
            time.sleep(0.001)
            
        values = (name, returnPid)
        
        pipe  = open(pipePath, "wb", buffering=0)
        pickle.dump(("get", values), pipe)
        
        return self.receive(
            Message(
                "response",
                action=lambda pid: pid))