"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1.3
DATE CREATED: 3/6/2013 10:07PM
DATE TESTED:  3/7/2013 10:31AM 
REMARKS: Script is able to read all incoming text messages, return the number of the sender, text back to the sender
the corresponding keyword response and filter invalid keywords
"""

import time, serial

try:
    SerialPort = serial.Serial("COM6",115200)
except:
    print "port in use"
  

while True:
    
    def SEND(mssg, sender):
        
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(1)
        SerialPort.write('AT+CMGS="'+sender+'"\r\n')
        time.sleep(1)
        SerialPort.write(mssg+'\x1A')
        time.sleep(1)
        print 'info message sent'


    if SerialPort.isOpen():
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(1)
        OK = SerialPort.read(SerialPort.inWaiting())
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        message = SerialPort.read(SerialPort.inWaiting())
        
        try:
            texter =  message.split(",")[1].replace("+","").replace('"',"")
            print "sender: " + texter
           
            text =  message[61:-8].replace("\n","")
            print "text = " + text

            keyword = text.split()[0]
            print "keyword = " + keyword
            
            SerialPort.write('AT+CMGD=0\r\n')
            time.sleep(1)

            if keyword == "GEO":
                SEND("Geocoding", texter)
                    
            elif keyword == "REV":
                SEND("Reverse Geocoding", texter)

            else:
                if text == "INFO":
                    SEND("SMS Based Geocoding and Reverse Geocoding", texter)

                elif text == "REG":
                    SEND("You are now registered", texter)

                else:
                    SEND("INVALID KEYWORD", texter)
                    
                
        except:
            print "NO INCOMING TEXT"
        print "---------------------------------------------"
        time.sleep(1)
