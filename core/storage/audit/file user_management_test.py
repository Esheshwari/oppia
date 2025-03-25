from core.domain import user_management
import unittest

class UsernameChangeAuditTests(unittest.TestCase):
    """Tests for the UsernameChangeAudit domain object."""

    def test_validate_success(self):
        """Test that valid data passes validation."""
        audit = user_management.UsernameChangeAudit(
            committer_id="admin123", old_username="oldUser", new_username="newUser"
        )
        audit.validate()  # Should not raise an error

    def test_validate_invalid_types(self):
        """Test that invalid types raise ValueError."""
        with self.assertRaises(ValueError):
            user_management.UsernameChangeAudit(
                committer_id=123, old_username="oldUser", new_username="newUser"
            ).validate()

        with self.assertRaises(ValueError):
            user_management.UsernameChangeAudit(
                committer_id="admin123", old_username=None, new_username="newUser"
            ).validate()

        with self.assertRaises(ValueError):
            user_management.UsernameChangeAudit(
                committer_id="admin123", old_username="oldUser", new_username=""
            ).validate()


class DeletedUserTests(unittest.TestCase):
    """Tests for the DeletedUser domain object."""

    def test_validate_success(self):
        """Test valid user ID."""
        user = user_management.DeletedUser(user_id="user123")
        user.validate()  # Should not raise an error

    def test_validate_invalid_user_id(self):
        """Test invalid user ID."""
        with self.assertRaises(ValueError):
            user_management.DeletedUser(user_id=123).validate()


class UserEmailPreferencesTests(unittest.TestCase):
    """Tests for the UserEmailPreferences domain object."""

    def test_validate_success(self):
        """Test that valid data passes validation."""
        prefs = user_management.UserEmailPreferences(
            user_id="user123", email="test@example.com", preferences={"newsletter": True}
        )
        prefs.validate()  # Should not raise an error

    def test_validate_invalid_email(self):
        """Test invalid email formats."""
        with self.assertRaises(ValueError):
            user_management.UserEmailPreferences(
                user_id="user123", email="invalid-email", preferences={"newsletter": True}
            ).validate()

    def test_validate_invalid_preferences(self):
        """Test non-dictionary preferences."""
        with self.assertRaises(ValueError):
            user_management.UserEmailPreferences(
                user_id="user123", email="test@example.com", preferences="invalid_data"
            ).validate()
