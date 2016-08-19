from proc_named_message import *

# adapted from multi_producer_multi_consumer.py
class Producer(NamedMessageProc):
    
    def main(self, *args):
        super().main()
        # self.registerOnNameServer("producer")
        
        # making a requirement that the buffer should exist,
        # because producer gives data to the buffer
        buffer = None
        while buffer == None:
            time.sleep(0.01)
            buffer = self.getProcPid("buffer", os.getpid())
        
        for i in range(1, 1001):
            self.give(buffer, 'put', i)
        self.give(buffer, 'stop')
        
if __name__ == "__main__":
    Producer().main()