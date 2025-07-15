########################################################################
# Filename    : LCD1602.py
# Description : 1602 LCD display driver for I2C interface using PCF8574
# Author      : Based on Freenove PCF8574 example
# modification: 2025/07/14
########################################################################
import smbus
import time

class PCF8574_I2C(object):
    OUTPUT = 0
    INPUT = 1
    
    def __init__(self, address):
        # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
        self.bus = smbus.SMBus(1)
        self.address = address
        self.currentValue = 0
        self.writeByte(0)   # I2C test.
        
    def readByte(self):  # Read PCF8574 all port of the data
        return self.currentValue
        
    def writeByte(self, value):  # Write data to PCF8574 port
        self.currentValue = value
        self.bus.write_byte(self.address, value)

    def digitalRead(self, pin):  # Read PCF8574 one port of the data
        value = self.readByte()  
        return (value & (1 << pin) == (1 << pin)) and 1 or 0
        
    def digitalWrite(self, pin, newvalue):  # Write data to PCF8574 one port
        value = self.currentValue
        if newvalue == 1:
            value |= (1 << pin)
        elif newvalue == 0:
            value &= ~(1 << pin)
        self.writeByte(value)   

class LCD1602:
    # LCD Commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # Entry flags
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Display control flags
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Function set flags
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    # PCF8574 pin mapping
    RS = 0  # Register select pin
    En = 2  # Enable pin
    D4 = 4  # Data pins
    D5 = 5
    D6 = 6
    D7 = 7
    BL = 3  # Backlight pin

    def __init__(self, address=0x27):
        self.pcf = PCF8574_I2C(address)
        self.address = address
        self.init_display()

    def init_display(self):
        """Initialize the LCD display"""
        # Turn on backlight
        self.pcf.digitalWrite(self.BL, 1)
        time.sleep(0.05)
        
        # Initialize in 4-bit mode
        self.write_4bits(0x30)
        time.sleep(0.005)
        self.write_4bits(0x30)
        time.sleep(0.005)
        self.write_4bits(0x30)
        time.sleep(0.002)
        self.write_4bits(0x20)  # Set to 4-bit mode
        
        # Function set: 4-bit mode, 2 lines, 5x8 dots
        self.command(self.LCD_FUNCTIONSET | self.LCD_4BITMODE | self.LCD_2LINE | self.LCD_5x8DOTS)
        
        # Display control: display on, cursor off, blink off
        self.command(self.LCD_DISPLAYCONTROL | self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF)
        
        # Clear display
        self.clear()
        
        # Entry mode: left to right, no shift
        self.command(self.LCD_ENTRYMODESET | self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT)

    def write_4bits(self, value):
        """Write 4 bits to the LCD"""
        for i in range(4, 8):
            self.pcf.digitalWrite(i, (value >> (i-4)) & 1)
        self.pulse_enable()

    def pulse_enable(self):
        """Pulse the enable pin"""
        self.pcf.digitalWrite(self.En, 0)
        time.sleep(0.0001)
        self.pcf.digitalWrite(self.En, 1)
        time.sleep(0.0001)
        self.pcf.digitalWrite(self.En, 0)
        time.sleep(0.0001)

    def command(self, value):
        """Send a command to the LCD"""
        self.pcf.digitalWrite(self.RS, 0)  # Command mode
        self.write_4bits(value >> 4)  # High nibble
        self.write_4bits(value & 0x0F)  # Low nibble
        if value < 4:
            time.sleep(0.002)  # Commands 1 and 2 need more time
        else:
            time.sleep(0.00005)

    def write_char(self, value):
        """Write a character to the LCD"""
        self.pcf.digitalWrite(self.RS, 1)  # Data mode
        self.write_4bits(value >> 4)  # High nibble
        self.write_4bits(value & 0x0F)  # Low nibble
        time.sleep(0.00005)

    def clear(self):
        """Clear the display"""
        self.command(self.LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def home(self):
        """Return cursor to home position"""
        self.command(self.LCD_RETURNHOME)
        time.sleep(0.002)

    def set_cursor(self, col, row):
        """Set cursor position"""
        row_offsets = [0x00, 0x40]
        if row >= len(row_offsets):
            row = len(row_offsets) - 1
        self.command(self.LCD_SETDDRAMADDR | (col + row_offsets[row]))

    def print(self, message):
        """Print a message to the LCD"""
        for char in str(message):
            self.write_char(ord(char))

    def print_line(self, line, message):
        """Print a message to a specific line (0 or 1)"""
        self.set_cursor(0, line)
        # Pad or truncate message to 16 characters
        formatted_message = str(message)[:16].ljust(16)
        self.print(formatted_message)

    def backlight_on(self):
        """Turn on backlight"""
        self.pcf.digitalWrite(self.BL, 1)

    def backlight_off(self):
        """Turn off backlight"""
        self.pcf.digitalWrite(self.BL, 0)
