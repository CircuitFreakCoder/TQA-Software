"""

    PROJECT NAME: SMS-BASED GEOCODING & REVERSE GEOCODING SERVER
    VERSION 2.0 RELEASE CANDIDATE


    Copyright (c) 2013 Jorick A. Caberio and contributors

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom
    the Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall
    be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

"""

import time, serial, sqlite3
import win32com.client
from datetime import datetime 
from googlemaps import GoogleMaps
gmaps = GoogleMaps(api_key = 'AIzaSyD4qJM8Ai8dl3hTxvf_CiCimDWbFHdHey8')

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''CREATE TABLE Users (id integer primary key, number text unique)''')

try:
    SerialPort = serial.Serial("COM7",115200)
except:
    print "port in use"
  

while True:
    
    def SEND(mssg, sender):
        
        #Send SMS to the user
        SerialPort.write('AT+CMGF=1\r')
        time.sleep(0.5)
        SerialPort.write('AT+CMGS="'+sender+'"\r\n')
        time.sleep(0.5)
        SerialPort.write(mssg+'\x1A')
        time.sleep(0.5)
        print 'info message sent'

    def GMAP(myLat, myLng):
        
        #open google earth to view destination
        ge =  win32com.client.Dispatch("GoogleEarth.ApplicationGE")
        print "Opening Google Earth, please wait... "
        time.sleep(5)
        altitude = 2500
        altMode = 1
        focusDistance = 3000
        tilt =0
        azimuth = 370
        speed = 0.5
        time.sleep(4)
        ge.SetCameraParams (myLat, myLng, altitude, altMode, focusDistance, tilt, azimuth, speed)

        

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
                        print "\nInput Location: " + address
                        LAT, LNG = gmaps.address_to_latlng(address)
                        print LAT, LNG
                        SEND(address+"\nlat: "+str(LAT)+"\nlng: "+str(LNG), texter)

                        GMAP(LAT, LNG)
                        
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
                        
                        print  lat
                        print  lng
                        destination = gmaps.latlng_to_address(lat,lng)
                        print destination

                        SEND(destination, texter)

                        GMAP(lat,lng)

                        
                    except:
                        SEND("Invalid latitude or longitude", texter)

                else:
                    print texter+" is NOT registered"
                    SEND("You are not registered",texter)
                
            else:
                if text == "INFO":
                    SEND("To access services, text REG to this number. For geocoding, text GEO LOCATION to this number. For reverse-geocoding, text REV LAT LNG to this number.", texter)

                elif text == "REG":

                    try: 
                        c.execute("INSERT INTO Users (number) VALUES ("+texter+")")
                        conn.commit()
                        SEND("You are now registered", texter)
                    except:
                        print texter + " tried to register again"
                        SEND("Invalid keyword. You are already registered.", texter)
                        
                        

                else:
                    SEND("Invalid keyword. Text INFO to this number for more details.", texter)
                    
                
        except:
            print "NO INCOMING TEXT\n"
            print "REGISTERED USERS:"
            print "id | phone number"
            for row in c.execute('SELECT * FROM Users'):
                print row
        print "---------------------------------------------"
        time.sleep(1)
        
