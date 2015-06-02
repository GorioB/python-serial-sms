import serial
import io
import time
import re
def sparse(d):
    r = []
    f = []
    e = d.splitlines()
    for i in e:
        if i[0:5] == "+CMGL":
            f.append(re.search("\+[0-9]{12}",i).group(0))
            
        else:
            f.append(i)
            r.append(f)
            f = []

    return r

class smserver(object): 
    def __init__(self,device):
        self.ser=None
        self.device = device

    def connect(self):
        try:
            self.ser = serial.Serial(self.device,9800,timeout=2)
            self.ser.write("AT+CMGF=1\r\n")
            print "[+] Connected"
            return True

        except Exception,e:
            print "[-] "+str(e)
            return False

    def getMessage(self):
        self.ser.write('AT+CMGL="REC UNREAD"\r\n')
        s = self.ser.read(500)
        s = s[s.find('AT+CMGL="REC UNREAD"')+len('AT+CMGL="REC UNREAD"   '):]
        if s.find("REC UNREAD")!=-1:
            s = s[:s.find("\r\nOK\r")-1]
            parsetring = sparse(s)
            return parsestring

        return []

    def sendMessage(self,number,message):
        self.ser.write('AT+CMGS="'+number+'"\r\n')
        self.ser.write(message)
        self.ser.write(chr(26))
        print "[+] Message Sent"

    def kill(self):
        self.ser.close()

    def run(self):
    	try:
    		print "[+] Server running."
	        while(1):
	            s = self.getMessage()
	            if s:
	                for i in s:
                        print "[+] Message received: "+i[1]
	                    self.sendMessage(i[0],"Your message: "+i[1])
	            else:
	                print "[*] No message. Waiting 2s"
	                time.sleep(2)

        except KeyboardInterrupt:
            print "[+] Interrupt received. Press enter to shut down."
            self.killser()
            n = raw_input("")

if __name__ == "__main__":
    s = smserver("/dev/ttyUSB0")
    while not s.connect():
        time.sleep(2)
    s.run()

