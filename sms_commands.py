"""SMS command helpers for sending and receiving messages via a GSM modem."""

from __future__ import print_function

import logging

logger = logging.getLogger(__name__)


def handle_sms(sms):
    """Callback invoked when an SMS message is received.

    Logs the incoming message and sends an automatic reply.
    """
    logger.info(
        "SMS received from %s at %s: %s", sms.number, sms.time, sms.text
    )
    print(
        f"== SMS message received ==\n"
        f"From: {sms.number}\nTime: {sms.time}\nMessage:\n{sms.text}\n"
    )
    print("Replying to SMS...")
    sms.reply("Thank you for your message! We will get back to you shortly.")
    print("Reply sent.\n")


def send_sms(modem, destination, message, reinitialize_fn=None):
    """Send an SMS message to *destination*.

    Parameters
    ----------
    modem : GsmModem
        An initialised GSM modem instance.
    destination : str
        The phone number to send the message to.
    message : str
        The message body.
    reinitialize_fn : callable, optional
        A callback to reinitialise the modem on failure.
    """
    logger.info("Sending SMS to %s", destination)
    try:
        modem.sendSms(destination, message)
        logger.info("Message sent to %s", destination)
    except Exception as exc:
        logger.error("Failed to send SMS to %s: %s", destination, exc)
        if reinitialize_fn is not None:
            reinitialize_fn()


def send_test_sms(modem, test_number):
    """Send a test SMS to verify the modem is working.

    Parameters
    ----------
    modem : GsmModem
        An initialised GSM modem instance.
    test_number : str
        The phone number to send the test message to.
    """
    test_message = "Test SMS sent from Mass SMS Texter."
    logger.info("Sending test SMS to %s", test_number)
    modem.sendSms(test_number, test_message)
    logger.info("Test SMS sent successfully")
