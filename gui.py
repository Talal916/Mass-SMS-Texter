import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
import pandas as pd

window = tk.Tk()
window.title("SMS Blaster")
window.geometry('800x800')
fileLoaded = 0


def main():
    print("Constructing GUI")
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


def createButtons():
    btn = tk.Button(
        window, text="Select customer file", command=fileButtonClicked)
    btn.grid(column=1, row=0)


def constructGui():
    createLabel()
    createButtons()
    window.mainloop()


if __name__ == '__main__':
    main()
