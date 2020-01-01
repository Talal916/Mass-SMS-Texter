import tkinter
window = tkinter.Tk()
window.title("SMS Blaster")
window.geometry('800x800')


def main():
    print("Constructing GUI")
    constructGui()


def createLabel():
    lbl = tkinter.Label(window, text="Built by @Talal916",
                        font=("Arial Bold", 14))
    lbl.grid(column=0, row=0)


def buttonClicked():
    print("Adding Customers")


def createButtons():
    btn = tkinter.Button(
        window, text="Select customer file", command=buttonClicked)
    btn.grid(column=1, row=0)


def constructGui():
    createLabel()
    createButtons()
    window.mainloop()


if __name__ == '__main__':
    main()
