# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #

import unittest
from subprocess import CalledProcessError

from unittest.mock import Mock, patch
from autoreduce_qp.queue_processor.reduction.process_manager import ReductionProcessManager
from autoreduce_qp.queue_processor.reduction.tests.common import add_data_and_message


class TestReductionProcessManager(unittest.TestCase):
    def setUp(self) -> None:
        self.data, self.message = add_data_and_message()

    def test_init(self):
        "Test that the constructor is doing what's expected"
        rpm = ReductionProcessManager(self.message)

        assert rpm.message == self.message

    @patch('queue_processor.reduction.process_manager.subprocess.run')
    def test_run_subprocess_error(self, subprocess_run: Mock):
        """Test proper handling of a subprocess encountering an error"""
        def side_effect(args, **_kwargs):
            raise CalledProcessError(1, args)

        subprocess_run.side_effect = side_effect
        rpm = ReductionProcessManager(self.message)
        rpm.run()

        subprocess_run.assert_called_once()
        assert "Processing encountered an error" in rpm.message.message

    @patch('queue_processor.reduction.process_manager.subprocess.run')
    def test_run(self, subprocess_run: Mock):
        """Tests success path - it uses side effect to set the expected output file rather than raise an exception"""
        def side_effect(args, **_kwargs):
            with open(args[-1], 'w') as tmpfile:
                tmpfile.write(self.message.serialize())

        subprocess_run.side_effect = side_effect
        rpm = ReductionProcessManager(self.message)
        result_message = rpm.run()

        assert result_message == self.message
