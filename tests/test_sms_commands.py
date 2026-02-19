"""Tests for the sms_commands module."""

from unittest.mock import MagicMock, patch

import sms_commands


class TestHandleSms:
    """Tests for the handle_sms callback."""

    def test_replies_to_incoming_sms(self):
        sms = MagicMock()
        sms.number = "+15551234567"
        sms.time = "2024-01-01 12:00:00"
        sms.text = "Hello"

        sms_commands.handle_sms(sms)

        sms.reply.assert_called_once()


class TestSendSms:
    """Tests for the send_sms function."""

    def test_sends_message_via_modem(self):
        modem = MagicMock()

        sms_commands.send_sms(modem, "+15551234567", "Hello!")

        modem.sendSms.assert_called_once_with("+15551234567", "Hello!")

    def test_calls_reinitialize_on_failure(self):
        modem = MagicMock()
        modem.sendSms.side_effect = Exception("Modem error")
        reinit = MagicMock()

        sms_commands.send_sms(modem, "+15551234567", "Hello!", reinitialize_fn=reinit)

        reinit.assert_called_once()

    def test_does_not_crash_without_reinitialize_fn(self):
        modem = MagicMock()
        modem.sendSms.side_effect = Exception("Modem error")

        # Should not raise
        sms_commands.send_sms(modem, "+15551234567", "Hello!")


class TestSendTestSms:
    """Tests for the send_test_sms function."""

    def test_sends_test_message(self):
        modem = MagicMock()

        sms_commands.send_test_sms(modem, "+15559999999")

        modem.sendSms.assert_called_once()
        args = modem.sendSms.call_args
        assert args[0][0] == "+15559999999"
        assert "Test" in args[0][1]


class TestConfig:
    """Tests for config module."""

    def test_default_values(self):
        import config

        assert config.PORT == "COM5" or isinstance(config.PORT, str)
        assert isinstance(config.BAUDRATE, int)

    @patch.dict("os.environ", {"SMS_PORT": "/dev/ttyUSB0", "SMS_BAUDRATE": "9600"})
    def test_env_override(self):
        import importlib
        import config

        importlib.reload(config)

        assert config.PORT == "/dev/ttyUSB0"
        assert config.BAUDRATE == 9600
