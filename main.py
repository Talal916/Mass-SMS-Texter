from __future__ import print_function

from gsmmodem.modem import GsmModem
import logging
import pandas as pd
import gui


PORT = 'COM5'
BAUDRATE = 9600
PIN = None  # SIM card PIN (if any)
UMERBHAINUM = "+923333130814"
TALALNUM = "+9232111811642"


def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(
        sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    sms.reply(u'Please message us @KhaoDosa on IG and Facebook! ')
    print('SMS sent.\n')


def openCustomerSheet():
    print("OpenCustomerSheet")


def main():
    gui.main()
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG)
    modem.smsTextMode = False
    modem.connect(PIN)
    print("Modem IMEI: ", modem.imei)
    print("Sending SMS: Welcome to Khao Dosa")
   # modem.sendSms(TALALNUM, "Welcome to Khao Dosa!")
    print('Waiting for SMS message...')
    try:
        # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
        modem.rxThread.join(2**15)
    finally:
        modem.close()


if __name__ == '__main__':
    main()
