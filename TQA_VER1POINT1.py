"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1.1
DATE CREATED: 3/6/2013 01:53PM
DATE TESTED:  3/6/2013 02:06PM 
REMARKS: Script is able to read all incoming text messages and return the number of the sender
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
        OK = SerialPort.read(SerialPort.inWaiting())
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        message = SerialPort.read(SerialPort.inWaiting())
        try:
            texter = message.split(",")[1]
            print texter
        except:
            print "no sender"
        print message
        print "---------------------------------------------"
        SerialPort.write('AT+CMGD=0\r\n')
        time.sleep(1)
        SerialPort.close()
        time.sleep(2)
    
