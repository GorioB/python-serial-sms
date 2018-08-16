import serial
import time
import re


def sparse(d):
    r = []
    f = []
    e = d.splitlines()
    for i in e:
        if i[0:5] == "+CMGL":
            f.append(re.search("\+[0-9]{12}", i).group(0))
        else:
            f.append(i)
            r.append(f)
            f = []

    return r


class SMServer(object):
    def __init__(self, device):
        """ Initializes the server object and device for serial to try to connect to """
        self.ser = None
        self.device = device

    def connect(self):
        """ Initialize serial connection and send command to GSM modem to start communication. Returns True on success and False on any exception. """
        try:
            self.ser = serial.Serial(self.device, 9800, timeout=2)
            self.ser.write(str.encode("AT+CMGF=1\r\n"))
            print("[+] Connected")
            return True

        except Exception as e:
            print("[-] " + str(e))
            return False

    def getMessage(self):
        """ Returns list of [sender number,message] pairs"""
        self.ser.write(str.encode('AT+CMGL="REC UNREAD"\r\n'))
        s = self.ser.read(500)
        s = s[s.find(str.encode('AT+CMGL="REC UNREAD"'))+len('AT+CMGL="REC UNREAD"   '):]
        if s.find(str.encode("REC UNREAD")) != -1:
            s = s[:s.find("\r\nOK\r")-1]
            parsestring = sparse(s)
            return parsestring

        return []

    def sendMessage(self, number, message):
        """ Send message to number. Doesn't check if sending is successful """
        self.ser.write(str.encode('AT+CMGS="'+number+'"\r\n'))
        self.ser.write(str.encode(message))
        self.ser.write(str.encode(chr(26)))
        print("[+] Message Sent")

    def kill(self):
        """ Close Serial communication """
        self.ser.close()

    def run(self):
        """ Continuously checks for new messages and responds with 'Your message: <message>'. Quit with CTRL+C """
        try:
            print("[+] Server running.")
            while(1):
                s = self.getMessage()
                if s:
                    for i in s:
                        print("[+] Message received: " + i[1])
                        self.sendMessage(i[0], "Your message: " + i[1])
                else:
                    print("[*] No message. Waiting 2s")
                    time.sleep(2)

        except KeyboardInterrupt:
            print("[+] Interrupt received. Press enter to shut down.")
            self.kill()
            n = input("")


if __name__ == "__main__":
    s = SMServer("COM5")
    while not s.connect():
        time.sleep(2)
    s.run()
