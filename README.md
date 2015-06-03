# python-serial-sms
Python SMS library using USB GSM dongles
========================================

Confirmed working on Huawei E3531 USB GSM modem and the like. Only supports SMS functions (no internet, calls, etc.)

Requirements
------------
[pySerial 2.7](http://pyserial.sourceforge.net/)

Usage
-----

    from sms import SMServer
    s = SMServer("/dev/ttyUSB0")
    if s.connect():
      s.sendMessage("01234567890","Hello World!")
      for sender,message in s.getMessage():
        print sender,message
      s.kill()

