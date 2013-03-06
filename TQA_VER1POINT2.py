"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1.2
DATE CREATED: 3/6/2013 10:07PM
DATE TESTED:  3/7/2013 12:16PM 
REMARKS: Script is able to read all incoming text messages, return the number of the sender, and text back to the sender
the corresponding keyword response
"""

import time, serial

SerialPort = serial.Serial("COM6",115200)




while True:
    
    texter = ""
    
    def SEND(mssg, sender):
        
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(2)
        SerialPort.write('AT+CMGS="'+sender+'"\r\n')
        time.sleep(2)
        SerialPort.write(mssg+'\x1A')
        time.sleep(2)
        print 'info message sent'


    if SerialPort.isOpen():
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(1)
        OK = SerialPort.read(SerialPort.inWaiting())
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        message = SerialPort.read(SerialPort.inWaiting())
        
        try:
            texter = message.split(",")[1].replace("+","").replace('"',"")
            print "sender: " + texter
            
            keyword = message.split()[3].upper()
            print "keyword = " + keyword
            SerialPort.write('AT+CMGD=0\r\n')
            time.sleep(1)

        
            if keyword == "INFO":
                SEND("GET INFO", texter)
                
            elif keyword == "REG":
                SEND("REG INFO", texter)
                
            elif keyword == "GEO":
                SEND("GEO INFO", texter)
                
            elif keyword == "REV":
                SEND("REV INFO", texter)
                
            else:
                SEND("INVALID KEYWORD", texter)
                print "INVALID KEYWORD"
            
        except:
            print "NO INCOMING TEXT"
        print "message = " + message
        print "---------------------------------------------"
