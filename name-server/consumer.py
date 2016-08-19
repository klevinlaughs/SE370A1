from proc_named_message import *

# adapted from multiple_consumer.py
class Consumer(NamedMessageProc):
    
    def main(self, *args):
        super().main()
        
        print("consumer registering")
        self.registerOnNameServer("consumer")
        
        print("consumer getting buffer pid")
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
        # self.give(self.main_proc, 'completed', self.count)
        sys.exit()

if __name__ == "__main__":
    Consumer().main()