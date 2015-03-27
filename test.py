import serial
import io
import time
import re
from sparse import sparse
class smserver(): 
    def __init__(self):
        try:
            self.ser = serial.Serial("COM5",9800,timeout=2)
            self.ser.write("AT+CMGF=1\r\n")
            print "Connected"

        except Exception,e:
            print str(e)


    def getmsg(self):
        self.ser.write('AT+CMGL="REC UNREAD"\r\n')
        s = self.ser.read(500)
        return s

    def respondwithlove(self,number,message):
        self.ser.write('AT+CMGS="'+number+'"\r\n')
        self.ser.write(message)
        self.ser.write(chr(26))
        print "Response sent"

    def killser(self):
        self.ser.close()

    def runserv(self):
        while(1):
            s = self.getmsg()
            s = s[s.find('AT+CMGL="REC UNREAD"')+len('AT+CMGL="REC UNREAD"   '):]
            if s.find("REC UNREAD")!=-1:
                s = s[:s.find("\r\nOK\r")-1]
                parsetring = sparse(s)
                for i in parsetring:
                    self.respondwithlove(i[0],"Your message: "+i[1])

            else:
                print "No message. Waiting 2s"
                time.sleep(2)


if __name__ == "__main__":
    s = smserver()
    try:
        s.runserv()
        print "Server running."

    except KeyboardInterrupt:
        print "Interrupt received. Press enter to shut down."
        s.killser()
        n = raw_input("")
        exit()

