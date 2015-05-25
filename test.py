import serial
import io
import time
import re
from sparse import sparse
class smserver(): 
    def __init__(self):
        try:
            self.ser = serial.Serial("COM15",9800,timeout=2)
            self.ser.write("AT+CMGF=1\r\n")
            print "Connected"

        except:
            print "Some kind of failure"


    def getmsg(self):
        self.ser.write('AT+CMGL="REC UNREAD"\r\n')
        s = self.ser.read(500)
        return s

    def sendMessage(self,number,message):
        self.ser.write('AT+CMGS="'+number+'"\r\n')
        self.ser.write(message)
        self.ser.write(chr(26))
        print "Message Sent"

    def killser(self):
        self.ser.close()

    def runserv(self):
    	try:
    		print "Server running."
	        while(1):
	            s = self.getmsg()
	            s = s[s.find('AT+CMGL="REC UNREAD"')+len('AT+CMGL="REC UNREAD"   '):]
	            if s.find("REC UNREAD")!=-1:
	                s = s[:s.find("\r\nOK\r")-1]
	                parsetring = sparse(s)
	                print i[1]
	                for i in parsetring:
	                    self.respondwithlove(i[0],"Your message: "+i[1])

	            else:
	                print "No message. Waiting 2s"
	                time.sleep(2)
        except KeyboardInterrupt:
            print "Interrupt received. Press enter to shut down."
            self.killser()
            n = raw_input("")

if __name__ == "__main__":
    s = smserver()

