#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2023/05/15
########################################################################
from time import sleep, strftime
from datetime import datetime
from LCD1602 import CharLCD1602

lcd1602 = CharLCD1602()    
start_time = datetime.now()
def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C '

def stopwatch():
    elapsed_time = datetime.now() - start_time
    minutes, seconds = divmod(elapsed_time.seconds, 60)
    return f'{minutes:02}:{seconds:02}'  # Format as MM:SS
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    lcd1602.init_lcd()
    count = 0
    while(True):
        # lcd1602.clear()
        lcd1602.write(0, 0, f'HilaDress HW30752' )# display Project
        lcd1602.write(0, 1, stopwatch())   # display stopwatch
        print('tick')
        sleep(.1)
def destroy():
    lcd1602.clear()
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    