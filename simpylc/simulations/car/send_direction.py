import can
import time as tm
from getkey import getkey, keys

class SendDirection:
    def __init__ (self):
        print ('Use arrow keys to control speed and direction')

        self.bus = can.interface.Bus(interface='socketcan',
              channel='vcan0',
              receive_own_messages=True)
        
        while True:
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)
            
    def input (self):
        key = getkey ()
        
        self.leftKey = key == keys.LEFT
        self.rightKey = key == keys.RIGHT
        self.upKey = key == keys.UP
        self.downKey = key == keys.DOWN

    def sweep (self):
        self.result = can.Message(arbitration_id=0x1,
                      data=[0x0],
                      is_extended_id=True)

        if self.leftKey:
            self.result = can.Message(arbitration_id=0x1,
                      data=[0x0, 0x65, 0x64, 0x66, 0x65, 0x66, 0x77, 0x86],
                      is_extended_id=True)
        elif self.rightKey:
            self.result = can.Message(arbitration_id=0x1,
                      data=[0x0, 0x65, 0x64, 0x66, 0x65, 0x66, 0x77, 0x87],
                      is_extended_id=True)
        elif self.upKey:
            self.result = can.Message(arbitration_id=0x1,
                      data=[0x0, 0x65, 0x64, 0x66, 0x65, 0x66, 0x77, 0x88],
                      is_extended_id=True)
        elif self.downKey:
            self.result = can.Message(arbitration_id=0x1,
                      data=[0x0, 0x65, 0x64, 0x66, 0x65, 0x66, 0x77, 0x89],
                      is_extended_id=True)
        print(self.result)
        
    def output (self):
        self.bus.send(self.result)

if __name__ == '__main__':
    SendDirection()
