from proc_named_message import *

# adapted from multiple_consumer.py
class Consumer(NamedMessageProc):
    
    def main(self, *args):
        super().main()
        
        self.registerOnNameServer("consumer")
        
        # making a requirement that the buffer should exist,
        # because consumer consumes from the buffer
        buffer = None
        while buffer == None:
            time.sleep(0.01)
            buffer = self.getProcPid("buffer", os.getpid())
        
        while True:
            self.give(buffer, 'get', os.getpid())
            self.receive(
                Message(
                    'stop',
                    action=self.finish),
                Message(
                    ANY,
                    action=self.handle_input))
                    
    def handle_input(self, data):
        print('{} from consumer'.format(data))
    
    def finish(self):
        # just for the purpose of the assignment, once the consumer has stopped,
        # tell the name server to stop
        pipePath = "/tmp/pipe_name_server"
        
        # wait for it to be created
        while not os.path.exists(pipePath):
            time.sleep(0.001)
        
        pipe  = open(pipePath, "wb", buffering=0)
        pickle.dump(("stop", ()), pipe)
        
        sys.exit()

if __name__ == "__main__":
    Consumer().main()