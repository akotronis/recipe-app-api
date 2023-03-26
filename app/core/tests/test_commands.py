"""
Test custom django management commands.
"""


from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# `check` is from `BaseCommand` class and is used to check
# the status of he database
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready.
        """
        patched_check.return_value = True
        call_command('wait_for_db')
        # Checks we are calling the right thing from `test_wait_for_db_ready`
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError.
        """
        # The first 2 tiems we called the mocked method we want to raise
        #     `Psycopg2Error` etc (2, 3 are random for simulation)
        # `Psycopg2Error` -> db is not ready to accept connetions
        # `OperationalError` -> db is ready but hasn't created the
        #     needed database
        # True -> No exception
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
