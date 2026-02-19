"""Mass SMS Texter – GUI application.

Provides a Tkinter interface for loading customer data from an Excel file
and sending personalised SMS messages via a connected GSM modem.
"""

import logging
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import pandas as pd
import serial.tools.list_ports
from gsmmodem.modem import GsmModem
from tqdm import tqdm

import config
import sms_commands

logger = logging.getLogger(__name__)


class Application:
    """Main application window for Mass SMS Texter."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mass SMS Texter")
        self.window.geometry("800x600")

        self.modem = None
        self.customer_data = None

        self._detect_serial_ports()
        self._initialize_modem()
        self._build_gui()

    # ------------------------------------------------------------------ #
    #  Modem helpers
    # ------------------------------------------------------------------ #

    def _detect_serial_ports(self):
        """Detect serial ports and alert the user if none are found."""
        ports = list(serial.tools.list_ports.comports())
        if ports:
            logger.info("Serial port(s) detected: %s", ports)
        else:
            logger.warning("No serial ports detected")
            messagebox.showerror(
                "No Modem",
                "No modem detected! Check that the modem is connected "
                "and visible in Device Manager.",
            )
            raise SystemExit("No modem detected")

    def _initialize_modem(self):
        """Connect to the GSM modem using settings from *config*."""
        logger.info("Initialising modem on %s …", config.PORT)
        self.modem = GsmModem(
            config.PORT,
            config.BAUDRATE,
            smsReceivedCallbackFunc=sms_commands.handle_sms,
        )
        self.modem.connect(config.PIN)
        logger.info("Modem connected – IMEI: %s", self.modem.imei)
        self._offer_test_message()

    def _reinitialize_modem(self):
        """Attempt to reconnect to the modem after a failure."""
        try:
            logger.info("Reinitialising modem …")
            self.modem = GsmModem(
                config.PORT,
                config.BAUDRATE,
                smsReceivedCallbackFunc=sms_commands.handle_sms,
            )
            self.modem.connect(config.PIN)
            logger.info("Modem reinitialised – IMEI: %s", self.modem.imei)
        except Exception as exc:
            logger.error("Failed to reinitialise modem: %s", exc)

    def _offer_test_message(self):
        """Prompt the user to send a test SMS after modem initialisation."""
        if messagebox.askyesno(
            "Test Message",
            "Modem connected. Would you like to send a test SMS?",
        ):
            number = tk.simpledialog.askstring(
                "Test Number", "Enter the phone number for the test SMS:"
            )
            if number:
                try:
                    sms_commands.send_test_sms(self.modem, number)
                    messagebox.showinfo("Success", "Test SMS sent!")
                except Exception as exc:
                    logger.error("Test SMS failed: %s", exc)
                    messagebox.showerror(
                        "Error", f"Failed to send test SMS:\n{exc}"
                    )

    # ------------------------------------------------------------------ #
    #  GUI construction
    # ------------------------------------------------------------------ #

    def _build_gui(self):
        """Lay out all widgets."""
        # Header
        header = tk.Label(
            self.window, text="Mass SMS Texter", font=("Arial", 16, "bold")
        )
        header.grid(column=0, row=0, columnspan=2, pady=(10, 5))

        # Buttons
        file_btn = tk.Button(
            self.window,
            text="Load Customer File",
            width=20,
            command=self._load_customer_file,
        )
        file_btn.grid(column=0, row=1, padx=10, pady=5)

        self.file_label = tk.Label(self.window, text="No file loaded")
        self.file_label.grid(column=1, row=1, sticky="w")

        send_btn = tk.Button(
            self.window,
            text="Send Messages",
            width=20,
            command=self._on_send,
        )
        send_btn.grid(column=0, row=2, padx=10, pady=5)

        # Message area
        msg_label = tk.Label(self.window, text="Message (use NAME as placeholder):")
        msg_label.grid(column=0, row=3, columnspan=2, sticky="w", padx=10, pady=(10, 0))

        self.message_text = tk.Text(self.window, width=80, height=20)
        self.message_text.grid(column=0, row=4, columnspan=2, padx=10, pady=5)

    # ------------------------------------------------------------------ #
    #  Actions
    # ------------------------------------------------------------------ #

    def _load_customer_file(self):
        """Open a file dialog and load the customer Excel file."""
        filepath = askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            self.customer_data = pd.read_excel(
                filepath, sheet_name="Sheet1", usecols=["Name", "Mobile"]
            )
            count = len(self.customer_data)
            self.file_label.config(text=f"{count} customers loaded from {filepath}")
            logger.info("Loaded %d customers from %s", count, filepath)
        except Exception as exc:
            logger.error("Failed to load customer file: %s", exc)
            messagebox.showerror("Error", f"Failed to load file:\n{exc}")

    def _on_send(self):
        """Validate inputs and send messages after user confirmation."""
        if self.customer_data is None or self.customer_data.empty:
            messagebox.showwarning("No Customers", "Please load a customer file first.")
            return

        message_body = self.message_text.get("1.0", tk.END).strip()
        if not message_body:
            messagebox.showwarning("No Message", "Please enter a message to send.")
            return

        count = len(self.customer_data)
        if not messagebox.askyesno(
            "Confirm",
            f"Send this message to {count} customer(s)?",
        ):
            return

        self._send_messages(message_body)

    def _send_messages(self, message_body):
        """Iterate over customers and send personalised SMS messages."""
        with tqdm(total=len(self.customer_data), desc="Sending") as pbar:
            for _, row in self.customer_data.iterrows():
                number = str(row["Mobile"])
                name = str(row["Name"])
                personalised = message_body.replace("NAME", name)
                logger.info("Sending to %s (%s)", name, number)
                sms_commands.send_sms(
                    self.modem,
                    number,
                    personalised,
                    reinitialize_fn=self._reinitialize_modem,
                )
                pbar.update(1)

        messagebox.showinfo("Done", "All messages have been sent!")

    # ------------------------------------------------------------------ #
    #  Run
    # ------------------------------------------------------------------ #

    def run(self):
        """Start the Tkinter main loop."""
        self.window.mainloop()


def main():
    """Entry-point for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    )
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
