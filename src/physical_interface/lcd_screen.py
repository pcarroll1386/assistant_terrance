import smbus2
import time

class PFCF574_12C(object):
    OUTPUT = 0
    InPUT = 1
    def __init__(self, address):
        self.bus=smbus2.smbus2.SMBus(1)
        self.address = address
        self.currentValue = 0
        self.writeBype(0)

    def readByte(self):
        return self.currentValue
    
    def writeByte(self,value):
        self.currentValue = value
        self.bus.write_byte(self.address, value)

    def digitalRead(self):
        return self.currentValue

    def digitalWrite(self,pin,newvalue):
        value = self.currentValue
        if(newvalue == 1):
            value |= (1<<pin)
        elif(newvalue == 0):
            self.writeByte(value)
def loop():
    mcp = PFCF574_12C(0x27)
    while True:
        mcp.digitialWrite(3,1)
        print(f"Is 0xff? {mcp.readByte()}")
        time.sleep(1)
        mcp.writeByte(0x00)
        print(f"I 0x077 {mcp.readByte()}")
        time.sleep(1)

class PCF8574_GPIO(object):
    OUT = 0
    IN = 1
    BCM = 0
    BOARD = 0
    
    def __init__(self,address):
        self.chip = PFCF574_12C(address)
        self.address = address
    def setmode(self,pin,mode):
        pass
    def setup(self,pin,mode):
        pass
    def input(self,pin):
        return self.chip.digitalRead(pin)
    def output(self,pin,value):
        self.chip.digitalWrite(pin,value)

def destroy():
    bus.close


if __name__ == '__main__':
    print('Program is starting ...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()