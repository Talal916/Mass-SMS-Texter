import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile, askopenfilename
from gsmmodem.modem import GsmModem
import pandas as pd

import smsCommands
import config
import testingNumbers


window = tk.Tk()
window.title("Khao Dosa Messaging Application")
window.geometry('800x800')

fileLoaded = 0


def main():
    initializeModem()
    constructGui()


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
    modem.connect(config.PIN)
    print("Modem IMEI: ", modem.imei)
    if(messagebox.askyesno("Send test message?","Would you like to send a test sms message?")):
        smsCommands.testSms(modem)


def constructGui():
    print("Constructing GUI")
    createLabel()
    createButtons()
    createMessageField()
    window.mainloop()


def createMessageField():
    global message
    message = tk.Entry(window, width=300)
    message.grid(column=1, row=10)


def createButtons():
    customerFileBtn = tk.Button(
        window, text="Select customer file", command=fileButtonClicked)
    customerFileBtn.grid(column=0, row=5)
    sendMessageBtn = tk.Button(
        window, text="Send Message", command=sendMessageButtonClicked)
    sendMessageBtn.grid(column=0, row=6)


def sendMessageButtonClicked():
    if (askConfirmation()):
        print("Calling message sender function")
        callMessageSender(message.get())
    else:
        print("Message not sent, user declined")


def callMessageSender(messageText):
    for index, row in customerFileData.iterrows():
        convertedNumber = "+92"+str(row['Mobile'])
        personalizedMessage = messageText.replace("NAME", row['Name'])
        print("Sending message: \n"+personalizedMessage+"\n to: "+convertedNumber)
        smsCommands.sendSms(modem, convertedNumber, personalizedMessage)


def askConfirmation():
    res = messagebox.askyesnocancel(
        "Are you sure?", "Are you sure want to send this message to all your customers?")
    return res


if __name__ == '__main__':
    main()
