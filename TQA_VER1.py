"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1
DATE CREATED: 3/6/2013 12:16AM
DATE TESTED:  3/6/2013 12:06PM
REMARKS: Script is able to read all incoming text  
"""

import time, serial

#create serial object
try:
    SerialPort = serial.Serial("COM6",115200)
    SerialPort.close()
    
except:
    print "SerialPort ERROR"
else:
    
    while True:
        #function to read incoming text
        SerialPort.open()    
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(1)
        OK_RESPONSE = SerialPort.read(SerialPort.inWaiting())
        #print OK_RESPONSE
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        MESSAGE = SerialPort.read(SerialPort.inWaiting())
        print MESSAGE
        print "---------------------------------------------"
        SerialPort.write('AT+CMGD=0\r\n')
        time.sleep(1)
        SerialPort.close()
        time.sleep(2)
    
