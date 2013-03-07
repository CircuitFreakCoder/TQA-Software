"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1.4
DATE CREATED: 3/6/2013 10:07PM
DATE TESTED:  3/7/2013 12:25PM 
REMARKS: Script is able to read all incoming text messages, return the number of the sender, text back to the sender
the corresponding keyword response, filter invalid keywords, geocoding and reverse geocoding
"""

import time, serial
from googlemaps import GoogleMaps
gmaps = GoogleMaps(api_key = 'AIzaSyD4qJM8Ai8dl3hTxvf_CiCimDWbFHdHey8')

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
                try:
                    address = message[65:-8].replace("\n","")
                    print address
                    LAT, LNG =  gmaps.address_to_latlng(address)
                    print LAT, LNG
                    SEND(address+"\nlat: "+str(LAT)+"\nlng: "+str(LNG), texter)
                except:
                    SEND("Invalid address", texter)
                    
                        
            elif keyword == "REV":
                try:
                    lat = float(text.split()[1])
                    lng = float(text.split()[2])
                    
                    print lat, lng
                    destination = gmaps.latlng_to_address(lat,lng)
                    print destination
                    SEND(destination, texter)
                except:
                    SEND("Invalid latitude or longitude", texter)

            else:
                if text == "INFO":
                    SEND("GET INFO", texter)

                elif text == "REG":
                    SEND("You are now registered", texter)

                else:
                    SEND("INVALID KEYWORD", texter)
                    
                
        except:
            print "NO INCOMING TEXT"
        print "---------------------------------------------"
        time.sleep(1)
