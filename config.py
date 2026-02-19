"""
Configuration for Mass SMS Texter.

Settings can be overridden via environment variables:
    SMS_PORT      - Serial port for the GSM modem (default: COM5)
    SMS_BAUDRATE  - Baud rate for serial communication (default: 115200)
    SMS_PIN       - SIM card PIN, if required (default: None)
"""

import os

PORT = os.environ.get("SMS_PORT", "COM5")
BAUDRATE = int(os.environ.get("SMS_BAUDRATE", "115200"))
PIN = os.environ.get("SMS_PIN", None)
