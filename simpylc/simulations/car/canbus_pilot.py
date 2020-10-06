import can
import time as tm
import simpylc as sp

class CanbusPilot:
    def __init__ (self):
        self.resetKeys ()
        bus = can.Bus(interface='socketcan', channel='vcan0', receive_own_messages=True)
        while True:
            self.msg = bus.recv (1)
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)
            
    def input (self):
        if self.msg is not None:
            print(self.msg.data)
            if(self.msg.data == bytearray(b'\x00edfefw\x88')):
                self.upKey = True
            elif(self.msg.data == bytearray(b'\x00edfefw\x89')):
                self.downKey = True
            elif(self.msg.data == bytearray(b'\x00edfefw\x86')):
                self.leftKey = True
            elif(self.msg.data == bytearray(b'\x00edfefw\x87')):
                self.rightKey = True
        
        self.targetVelocityStep = sp.world.control.targetVelocityStep
        self.steeringAngleStep = sp.world.control.steeringAngleStep
        
    def sweep (self):
        if self.leftKey:
            self.steeringAngleStep += 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.rightKey:
            self.steeringAngleStep -= 1
            print ('Steering angle step: ', self.steeringAngleStep)
        elif self.upKey:
            self.targetVelocityStep += 1
            print ('Target velocity step: ', self.targetVelocityStep)
        elif self.downKey:
            self.targetVelocityStep -= 1
            print ('Target velocity step: ', self.targetVelocityStep)
        
    def output (self):
        self.resetKeys ()
        sp.world.control.steeringAngleStep.set (self.steeringAngleStep)
        sp.world.control.targetVelocityStep.set (self.targetVelocityStep)

    def resetKeys (self):
        self.upKey = False
        self.downKey = False
        self.leftKey = False
        self.rightKey = False
