# Kelvin Chris Lau, klau158, 9682466

from proc_named_message import *

# adapted from multiple_consumer.py
class Buffer(NamedMessageProc):

    def main(self, name, *args):
        super().main(name, *args)
        buffer_space = []
        
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
        consumerPid = self.getProcPid("consumer")
        self.give(consumerPid, "stop")
        sys.exit()
        
if __name__ == "__main__":
    Buffer().main("buffer")