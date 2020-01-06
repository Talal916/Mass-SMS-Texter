from __future__ import print_function

from gsmmodem.modem import GsmModem
import pandas as pd

import testingNumbers

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(
        sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    sms.reply(u'Please message us @KhaoDosa on IG and Facebook! ')
    print('SMS sent.\n')


def sendSms(destinationNumber, message):
    print("Sending SMS")

def testSms(modem):
    print("Sending test SMS")
    TESTSMS = "Test SMS sent from SMS Blaster. Contact @Talal916 for help"    
    modem.sendSms(testingNumbers.TESTNUM1, TESTSMS)