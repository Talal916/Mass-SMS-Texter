import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, askopenfilename
from gsmmodem.modem import GsmModem
from progressbar import ProgressBar
import pandas as pd
import serial.tools.list_ports
import logging
from tqdm import *
from multiprocessing import Process

import smsCommands
import config
import testingNumbers


window = tk.Tk()
window.title("Khao Dosa Messaging Application")
window.geometry('800x800')

fileLoaded = 0


def main():
    serialPortsList = detectSerialPorts()
    initializeModem()
    constructGui()


def detectSerialPorts():
    serialPortsList = (list(serial.tools.list_ports.comports()))
    if(len(serialPortsList) >= 1):
        print("Serial Port detected. Confirm if Modem")
        print(serialPortsList)
        return serialPortsList
    else:
        print("\nNo Modem detected! Program exiting!\n")
        messagebox.showerror(
            "No Modem!", "No Modem detected! Program exiting. Check if modem is connected and showing in device manager!")
        exit()


def createLabel():
    lbl = tk.Label(window, text="Built by @Talal916",
                   font=("Arial Bold", 14))
    lbl.grid(column=0, row=0)


def fileButtonClicked():
    print("Adding Customers")
    customerFileLocation = askopenfilename()
    print(customerFileLocation)
    global customerFileData
    customerFileData = 0
    customerFileData = pd.read_excel(
        customerFileLocation, "Sheet1", usecols=["Name", "Mobile"])
    print(customerFileData)


def initializeModem():
    print('Initializing modem...')
    global modem
    modem = GsmModem(config.PORT, config.BAUDRATE,
                     smsReceivedCallbackFunc=smsCommands.handleSms)
    # logging.basicConfig(format='%(levelname)s: %(message)s',
    #                     level=logging.DEBUG)
    modem.connect(config.PIN)
    print("Modem IMEI: ", modem.imei)
    testMessageRequest()


def testMessageRequest():
    if(messagebox.askyesno("Send test message?", "Would you like to send a test sms message?")):
        try:
            smsCommands.testSms(modem)
        except:
            print("Failed to send test message. Check modem")


def constructGui():
    print("Constructing GUI")
    createLabel()
    createButtons()
    createMessageField()
    window.mainloop()


def createMessageField():
    global message
    message = tk.Text(window, width=75, height=30)
    message.grid(column=1, row=10)


def createButtons():
    customerFileBtn = tk.Button(
        window, text="Select customer file", command=fileButtonClicked)
    customerFileBtn.grid(column=0, row=5)
    sendMessageBtn = tk.Button(
        window, text="Send Message", command=sendMessageButtonClicked)
    sendMessageBtn.grid(column=0, row=6)
#     cancelBtn = tk.Button(window, text="Cancel Send",
#                           command=cancelButtonClicked)


# def cancelButtonClicked():


def sendMessageButtonClicked():
    if (askConfirmation()):
        print("Calling message sender function")
        callMessageSender(message.get('1.0', END))
    else:
        print("Message not sent, user declined")


def callMessageSender(messageText):
    with tqdm(total=len(list(customerFileData.iterrows()))) as pbar:
        for index, row in customerFileData.iterrows():
            convertedNumber = "+92"+str(row['Mobile'])
            personalizedMessage = messageText.replace("NAME", row['Name'])
            print("Sending message: \n"+personalizedMessage +
                  "\n to: "+convertedNumber)
            smsCommands.sendSms(modem, convertedNumber, personalizedMessage)
            pbar.update(1)


def reinitializeModem():
    try:
        print('Reinitializing modem...')
        global modem
        modem = GsmModem(config.PORT, config.BAUDRATE,
                         smsReceivedCallbackFunc=smsCommands.handleSms)
        modem.connect(config.PIN)
        print("Modem IMEI: ", modem.imei)
    except:
        print("Failed to reinitialize modem")


def askConfirmation():
    res = messagebox.askyesnocancel(
        "Are you sure?", "Are you sure want to send this message to all your customers?")
    return res


if __name__ == '__main__':
    main()
