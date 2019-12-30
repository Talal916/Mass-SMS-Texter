from __future__ import print_function

from gsmmodem.modem import GsmModem
import logging

PORT = 'COM5'
BAUDRATE = 9600
PIN = None  # SIM card PIN (if any)


def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(
        sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    sms.reply(u'SMS received: "{0}{1}"'.format(
        sms.text[:20], '...' if len(sms.text) > 20 else ''))
    print('SMS sent.\n')


def main():
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print("Modem IMEI: ", modem.imei)
    modem.sendSms()
    print('Waiting for SMS message...')
    try:
        # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
        modem.rxThread.join(2**15)
    finally:
        modem.close()


if __name__ == '__main__':
    main()
