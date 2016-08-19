from proc_named_message import *

# adapted from multiple_consumer.py
class Buffer(NamedMessageProc):

    def main(self, *args):
        super().main()
        buffer_space = []
        
        self.registerOnNameServer("buffer")
        
        while True:
            self.receive(
                Message(
                    'put',
                    action=lambda data: buffer_space.append(data)),
                Message(
                    'get',
                    guard=lambda: len(buffer_space) > 0,
                    action=lambda consumer: self.give(consumer, 'data', buffer_space.pop(0))),
                Message(
                    'stop',
                    guard=lambda: len(buffer_space) == 0,
                    action=self.finish))
                    
    def finish(self):
        # self.give(self.main_proc, 'completed', self.count)
        sys.exit()
        
if __name__ == "__main__":
    Buffer().main()