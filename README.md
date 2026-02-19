# Mass SMS Texter

A desktop application for sending personalised bulk SMS messages to customers using a GSM modem. Load names and phone numbers from an Excel file, compose a message template, and send it to everyone in one click.

## Features

- **Auto-detect serial ports** for connected GSM modems
- **Load customers** from `.xlsx` Excel files (columns: `Name`, `Mobile`)
- **Personalise messages** using the `NAME` placeholder
- **Send a test SMS** before starting a bulk send
- **Auto-reply** to incoming SMS messages
- **Progress bar** while messages are being sent

## Requirements

- Python 3.8+
- A GSM modem connected via USB/serial
- A SIM card with SMS capability

## Installation

```bash
# Clone the repository
git clone https://github.com/Talal916/Mass-SMS-Texter.git
cd Mass-SMS-Texter

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Settings are read from environment variables with sensible defaults. You can also edit `config.py` directly.

| Variable | Default | Description |
|---|---|---|
| `SMS_PORT` | `COM5` | Serial port the GSM modem is connected to |
| `SMS_BAUDRATE` | `115200` | Baud rate for serial communication |
| `SMS_PIN` | *None* | SIM card PIN (if required) |

Example:

```bash
export SMS_PORT=/dev/ttyUSB0
export SMS_BAUDRATE=9600
```

## Usage

```bash
python gui.py
```

1. Click **Load Customer File** and select an `.xlsx` file with `Name` and `Mobile` columns.
2. Type your message in the text area. Use `NAME` as a placeholder for the customer's name.
3. Click **Send Messages** and confirm.

## Excel File Format

| Name | Mobile |
|---|---|
| Alice | +15551234567 |
| Bob | +15559876543 |

## Running Tests

```bash
python -m pytest tests/
```

## License

This project is provided as-is for educational purposes.
