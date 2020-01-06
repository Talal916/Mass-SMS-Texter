import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from gsmmodem.modem import GsmModem
import pandas as pd

import smsCommands
import config
import testingNumbers


window = tk.Tk()
window.title("SMS Blaster")
window.geometry('800x800')

fileLoaded = 0

def main():
    print("Constructing GUI")
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
    #modem = GsmModem(config.PORT, config.BAUDRATE, smsReceivedCallbackFunc=smsCommands.handleSms)
    #modem.connect(config.PIN)
    #print("Modem IMEI: ", modem.imei)
    #smsCommands.testSms(modem)

def constructGui():
    createLabel()
    createButtons()
    window.mainloop()

def createButtons():
    btn = tk.Button(
        window, text="Select customer file", command=fileButtonClicked)
    btn.grid(column=1, row=0)

if __name__ == '__main__':
    main()
