from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.test import TestCase

from api.management.commands.create_admin import Command


class TestCreateAdminCommand(TestCase):
    def test_can_create_user(self):
        mock_out = MagicMock()
        command = Command(stdout=mock_out)
        command.handle(
            username="user",
            password="whoami",
            email="example@doccano.com",
            database="default",
            interactive=False,
            verbosity=0,
        )
        self.assertEqual(get_user_model().objects.count(), 1)
        mock_out.write.assert_called_once_with("Setting password for User user.\n")

    def test_raise_error_if_username_is_not_given(self):
        mock_err = MagicMock()
        command = Command(stderr=mock_err)
        with self.assertRaises(CommandError):
            command.handle(
                password="whoami", email="example@doccano.com", database="default", interactive=False, verbosity=0
            )
            mock_err.write.assert_called_once_with("Error: Blank username isn't allowed.\n")

    def test_raise_error_if_password_is_not_given(self):
        mock_err = MagicMock()
        command = Command(stderr=mock_err)
        with self.assertRaises(CommandError):
            command.handle(
                username="user", email="example@doccano.com", database="default", interactive=False, verbosity=0
            )
            mock_err.write.assert_called_once_with("Error: Blank password isn't allowed.\n")

    def test_warn_default_password(self):
        mock_out = MagicMock()
        command = Command(stdout=mock_out)
        command.handle(
            username="user",
            password="password",
            email="example@doccano.com",
            database="default",
            interactive=False,
            verbosity=0,
        )
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(mock_out.write.call_count, 2)
        mock_out.write.assert_any_call("Warning: You should change the default password.\n")
        mock_out.write.assert_any_call("Setting password for User user.\n")

    def test_warn_duplicate_username(self):
        get_user_model().objects.create(username="admin", password="pass")
        mock_err = MagicMock()
        command = Command(stderr=mock_err)
        command.handle(
            username="admin",
            password="whoami",
            email="example@doccano.com",
            database="default",
            interactive=False,
            verbosity=0,
        )
        self.assertEqual(get_user_model().objects.count(), 1)
        mock_err.write.assert_called_once_with("User admin already exists.\n")
