"""
PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
VERSION: 1.5
DATE CREATED: 3/6/2013 10:07PM
DATE TESTED: 3/7/2013 12:25PM
REMARKS: Database integration - Only registered users can access the system.
Script is able to read all incoming text messages, return the number of the sender, text back to the sender
the corresponding keyword response, filter invalid keywords, geocoding and reverse geocoding
"""

import time, serial, sqlite3
from googlemaps import GoogleMaps
gmaps = GoogleMaps(api_key = 'AIzaSyD4qJM8Ai8dl3hTxvf_CiCimDWbFHdHey8')

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''CREATE TABLE Users (number text)''')


try:
    SerialPort = serial.Serial("COM7",115200)
except:
    print "port in use"
  

while True:
    
    def SEND(mssg, sender):
        
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(0.5)
        SerialPort.write('AT+CMGS="'+sender+'"\r\n')
        time.sleep(0.5)
        SerialPort.write(mssg+'\x1A')
        time.sleep(0.5)
        print 'info message sent'

    if SerialPort.isOpen():
        SerialPort.flushOutput()
        SerialPort.flushInput()
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(0.5)
        OK = SerialPort.read(SerialPort.inWaiting())
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(0.5)
        message = SerialPort.read(SerialPort.inWaiting())
                
        try:
            texter = message.split(",")[1].replace("+","").replace('"',"")
            print "sender: " + texter
           
            text = message[61:-8].replace("\n","")
            print "text = " + text

            keyword = text.split()[0]
            print "keyword = " + keyword
            
            SerialPort.write('AT+CMGD=0\r\n')
            time.sleep(0.5)

            if keyword == "GEO":

                c.execute("SELECT * FROM Users WHERE number = '%s'" %texter)
                response = c.fetchone()
                print response
                if response != None:
                    print texter+" is registered"
                    
                    try:
                        address = message[65:-8].replace("\n","")
                        print address
                        LAT, LNG = gmaps.address_to_latlng(address)
                        print LAT, LNG
                        SEND(address+"\nlat: "+str(LAT)+"\nlng: "+str(LNG), texter)
                    except:
                        SEND("Invalid address", texter)
                 
                else:
                    print texter+" is NOT registered"
                    SEND("You are not registered",texter)

                   
                        
            elif keyword == "REV":

                c.execute("SELECT * FROM Users WHERE number = '%s'" %texter)
                response = c.fetchone()
                print response
                if response != None:
                    print texter+" is registered"
                        
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
                    print texter+" is NOT registered"
                    SEND("You are not registered",texter)
                
            else:
                if text == "INFO":
                    SEND("GET INFO", texter)

                elif text == "REG":
                    c.execute("INSERT INTO Users VALUES ("+texter+")")
                    conn.commit()
                    SEND("You are now registered", texter)

                else:
                    SEND("INVALID KEYWORD", texter)
                    
                
        except:
            print "NO INCOMING TEXT"
            print "REGISTERED USERS:"
            for row in c.execute('SELECT * FROM Users'):
                print row
        print "---------------------------------------------"
        time.sleep(1)
        
