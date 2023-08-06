# ############################################################################
# Autoreduction Repository :
# https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################
"""
Tests message handling for the queue processor
"""

import random
from functools import partial
from unittest import main, mock
from unittest.mock import Mock, patch

from autoreduce_db.reduction_viewer.models import (Experiment, Instrument, Status)
from autoreduce_utils.message.message import Message
from django.db.utils import IntegrityError
from django.test import TestCase
from parameterized import parameterized

from autoreduce_qp.model.database.records import create_reduction_run_record
from autoreduce_qp.queue_processor.handle_message import HandleMessage
from autoreduce_qp.queue_processor.queue_listener import QueueListener
from autoreduce_qp.queue_processor.tests.test_instrument_variable_utils import FakeModule
from autoreduce_qp.systemtests.utils.data_archive import DefaultDataArchive

TEST_REDUCE_VARS_CONTENT = """
standard_vars = {
    "variable" : False
}
advanced_vars = {
    "advanced" : 123
}

variable_help = {
    "standard_vars" : {
        "variable" : "I am help"
    },
    "advanced_vars":{
        "advanced": "I am advanced help"
    }
}

"""


# pylint:disable=no-member
class FakeMessage:
    started_by = 0
    run_number = 1234567
    message = "I am a message"
    description = "This is a fake description"


class TestHandleMessage(TestCase):
    """
    Directly tests the message handling classes
    """
    fixtures = ["status_fixture"]

    def setUp(self):
        self.mocked_client = mock.Mock(spec=QueueListener)
        self.instrument_name = "ARMI"
        self.msg = Message()
        self.msg.populate({
            "run_number": 7654321,
            "rb_number": 1234567,
            "run_version": 0,
            "reduction_data": "/path/1",
            "started_by": -1,
            "data": "/path",
            "software": "6.0.0",
            "description": "This is a fake description",
            "instrument": self.instrument_name  # Autoreduction Mock Instrument
        })
        with patch("logging.getLogger") as patched_logger:
            self.handler = HandleMessage()
            self.mocked_logger = patched_logger.return_value

        self.experiment, _ = Experiment.objects.get_or_create(reference_number=1231231)
        self.instrument, _ = Instrument.objects.get_or_create(name=self.instrument_name)
        status = Status.get_queued()
        fake_script_text = "scripttext"
        self.reduction_run = create_reduction_run_record(self.experiment, self.instrument, FakeMessage(), 0,
                                                         fake_script_text, status)
        self.reduction_run.save()

    @parameterized.expand([
        ["reduction_error", 'e'],
        ["reduction_skipped", 's'],
    ])
    def test_reduction_with_message(self, function_to_call, expected_status):
        """
        Tests a reduction error where the message contains an error message
        """
        self.msg.message = "I am a message"
        getattr(self.handler, function_to_call)(self.reduction_run, self.msg)

        # pylint:disable=protected-access
        assert self.reduction_run.status == Status._get_status(expected_status)
        assert self.reduction_run.message == "I am a message"
        assert self.reduction_run.run_description == "This is a fake description"
        self.mocked_logger.info.assert_called_once()
        assert self.mocked_logger.info.call_args[0][1] == self.msg.run_number

    @parameterized.expand([
        ["reduction_error", 'e'],
        ["reduction_skipped", 's'],
    ])
    def test_reduction_without_message(self, function_to_call, expected_status):
        """
        Tests a reduction error where the message does not contain an error message
        """
        getattr(self.handler, function_to_call)(self.reduction_run, self.msg)

        # pylint:disable=protected-access
        assert self.reduction_run.status == Status._get_status(expected_status)
        self.mocked_logger.info.assert_called_once()
        assert self.mocked_logger.info.call_args[0][1] == self.msg.run_number

    def test_reduction_started(self):
        "Tests starting a reduction"
        assert self.reduction_run.started is None
        assert self.reduction_run.finished is None

        self.handler.reduction_started(self.reduction_run, self.msg)
        self.mocked_logger.info.assert_called_once()

        assert self.reduction_run.started is not None
        assert self.reduction_run.finished is None
        assert self.reduction_run.status == Status.get_processing()
        self.mocked_logger.info.assert_called_once()

    def test_reduction_complete(self):
        "Tests completing a reduction"
        self.msg.reduction_data = None
        assert self.reduction_run.finished is None
        self.handler.reduction_complete(self.reduction_run, self.msg)
        self.mocked_logger.info.assert_called_once()

        assert self.reduction_run.finished is not None
        assert self.reduction_run.status == Status.get_completed()
        self.mocked_logger.info.assert_called_once()
        assert self.reduction_run.software.name == "Mantid"
        assert self.reduction_run.software.version == self.msg.software
        assert self.reduction_run.reduction_location.count() == 0

    def test_reduction_complete_with_reduction_data(self):
        "Tests completing a reduction that has an output location at reduction_data"

        assert self.reduction_run.finished is None
        self.handler.reduction_complete(self.reduction_run, self.msg)
        self.mocked_logger.info.assert_called_once()

        assert self.reduction_run.finished is not None
        assert self.reduction_run.status == Status.get_completed()
        self.mocked_logger.info.assert_called_once()

        assert self.reduction_run.reduction_location.first().file_path == "/path/1"

    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_do_reduction_success(self, rpm):
        "Tests do_reduction success path"
        rpm.return_value.run = self.do_post_started_assertions

        self.handler.do_reduction(self.reduction_run, self.msg)
        assert self.reduction_run.status == Status.get_completed()
        assert self.reduction_run.started is not None
        assert self.reduction_run.finished is not None
        assert self.reduction_run.reduction_location.first().file_path == "/path/1"

    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_do_reduction_success_special_characters_in_script(self, rpm):
        "Tests do_reduction success path"
        rpm.return_value.run = self.do_post_started_assertions
        test_special_chars_script = 'print("✈", "’")'
        self.reduction_run.script = test_special_chars_script

        self.handler.do_reduction(self.reduction_run, self.msg)
        assert self.reduction_run.status == Status.get_completed()
        assert self.reduction_run.started is not None
        assert self.reduction_run.finished is not None
        assert self.reduction_run.reduction_location.first().file_path == "/path/1"
        assert self.reduction_run.script == test_special_chars_script

    def do_post_started_assertions(self, expected_info_calls=1):
        "Helper to capture common assertions between tests"
        assert self.reduction_run.status == Status.get_processing()
        assert self.reduction_run.started is not None
        assert self.reduction_run.finished is None
        assert self.mocked_logger.info.call_count == expected_info_calls
        # reset for follow logger calls
        self.mocked_logger.info.reset_mock()
        return self.msg

    # a bit of a nasty patch, but everything underneath should be unit tested separately
    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_do_reduction_fail(self, rpm):
        "Tests do_reduction failure path"
        self.msg.message = "Something failed"

        rpm.return_value.run = self.do_post_started_assertions

        self.handler.do_reduction(self.reduction_run, self.msg)
        assert self.reduction_run.status == Status.get_error()
        assert self.reduction_run.started is not None
        assert self.reduction_run.finished is not None
        assert self.reduction_run.message == "Something failed"

    def test_activate_db_inst(self):
        """
        Tests whether the function enables the instrument
        """
        self.instrument.is_active = False
        self.instrument.save()

        self.handler.activate_db_inst(self.instrument)

        assert self.instrument.is_active

    def test_find_reason_to_skip_run_empty_script(self):
        """
        Test find_reason_to_skip_run correctly captures validation failing on the message
        """
        self.reduction_run.script = ""
        assert "Script text for current instrument is empty" in self.handler.find_reason_to_skip_run(
            self.reduction_run, self.msg, self.instrument)

    def test_find_reason_to_skip_run_message_validation_fails(self):
        """
        Test find_reason_to_skip_run correctly captures validation failing on the message
        """
        self.msg.rb_number = 123  # invalid RB number, should be 7 digits
        assert "Validation error" in self.handler.find_reason_to_skip_run(self.reduction_run, self.msg, self.instrument)

    def test_find_reason_to_skip_run_instrument_paused(self):
        """
        Test find_reason_to_skip_run correctly captures that the instrument is paused
        """
        self.instrument.is_paused = True

        assert "is paused" in self.handler.find_reason_to_skip_run(self.reduction_run, self.msg, self.instrument)

    def test_find_reason_to_skip_run_doesnt_skip_when_all_is_ok(self):
        """
        Test find_reason_to_skip_run returns None when all the validation passes
        """
        assert self.handler.find_reason_to_skip_run(self.reduction_run, self.msg, self.instrument) is None

    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_send_message_onwards_ok(self, rpm):
        """
        Test that a run where all is OK is reduced
        """
        self.instrument.is_active = False
        rpm.return_value.run = partial(self.do_post_started_assertions, 2)

        self.handler.send_message_onwards(self.reduction_run, self.msg, self.instrument)

        assert self.reduction_run.status == Status.get_completed()
        assert self.instrument.is_active

    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_send_message_onwards_skip_run(self, rpm):
        """
        Test that a run that fails validation is skipped
        """
        self.msg.rb_number = 123

        self.handler.send_message_onwards(self.reduction_run, self.msg, self.instrument)

        rpm.return_value.run.assert_not_called()
        assert self.reduction_run.status == Status.get_skipped()
        assert "Validation error" in self.reduction_run.message
        assert "Validation error" in self.reduction_run.reduction_log

    @patch("autoreduce_qp.queue_processor.handle_message.ReductionScript")
    def test_create_run_records_multiple_versions(self, reduction_script: Mock):
        "Test creating multiple version of the same run"
        self.instrument.is_active = False

        self.msg.description = "Testing multiple versions"

        reduction_script.return_value.text.return_value = "print(123)"
        self.msg.run_number = random.randint(1000000, 10000000)
        db_objects_to_delete = []
        for i in range(5):
            reduction_run, message, instrument = self.handler.create_run_records(self.msg)
            db_objects_to_delete.append(reduction_run)

            assert reduction_run.run_number == self.msg.run_number
            assert reduction_run.experiment.reference_number == self.msg.rb_number
            assert reduction_run.run_version == i
            assert reduction_run.run_description == "Testing multiple versions"
            assert message.run_version == i
            assert instrument == self.instrument
            assert instrument.name == self.msg.instrument
            assert reduction_run.script == "print(123)"
            assert reduction_run.data_location.first().file_path == message.data
            assert reduction_run.status == Status.get_queued()

        for obj in db_objects_to_delete:
            obj.delete()

    def test_create_run_variables_no_variables_creates_nothing(self):
        "Test running a reduction run with an empty reduce_vars.py"
        expected_args = {'standard_vars': {}, 'advanced_vars': {}}

        self.handler.instrument_variable.create_run_variables = mock.Mock(return_value=[])

        message = self.handler.create_run_variables(self.reduction_run, self.msg, self.instrument)
        self.handler.instrument_variable.create_run_variables.assert_called_once_with(self.reduction_run, {})
        assert self.mocked_logger.info.call_count == 2
        self.mocked_logger.warning.assert_called_once()
        assert message.reduction_arguments == expected_args

    @patch('autoreduce_qp.queue_processor.reduction.service.ReductionScript.load', return_value=FakeModule())
    def test_create_run_variables(self, import_module: Mock):
        "Test the creation of RunVariables for the ReductionRun"
        expected_args = {'standard_vars': FakeModule().standard_vars, 'advanced_vars': FakeModule().advanced_vars}
        message = self.handler.create_run_variables(self.reduction_run, self.msg, self.instrument)
        assert self.mocked_logger.info.call_count == 2
        assert message.reduction_arguments == expected_args
        import_module.assert_called_once()

    def test_data_ready_other_exception_raised_ends_processing(self):
        "Test an exception being raised inside data_ready handler"
        self.handler.create_run_records = Mock(side_effect=RuntimeError)
        with self.assertRaises(RuntimeError):
            self.handler.data_ready(self.msg)
        self.mocked_logger.info.assert_called_once()
        self.mocked_logger.error.assert_called_once()

    def test_data_ready_variable_integrity_error_marks_reduction_error(self):
        "Test that an integrity error inside data_ready marks the reduction as errored"
        self.handler.create_run_records = Mock(return_value=(self.reduction_run, self.msg, self.instrument))
        self.handler.create_run_variables = Mock(side_effect=IntegrityError)
        with self.assertRaises(IntegrityError):
            self.handler.data_ready(self.msg)
        assert self.mocked_logger.info.call_count == 2
        self.mocked_logger.error.assert_called_once()
        assert self.reduction_run.status == Status.get_error()
        assert "Encountered error when saving run variables" in self.reduction_run.message

    def test_data_ready_no_reduce_vars(self):
        "Test data_ready when the reduce_vars script does not exist and throws a FileNotFoundError"
        self.handler.create_run_records = Mock(return_value=(self.reduction_run, self.msg, self.instrument))
        with self.assertRaises(FileNotFoundError):
            self.handler.data_ready(self.msg)
        assert self.mocked_logger.info.call_count == 3
        self.mocked_logger.error.assert_called_once()
        assert self.reduction_run.status == Status.get_error()
        assert "Encountered error when saving run variables" in self.reduction_run.message

    @patch('autoreduce_qp.queue_processor.reduction.service.ReductionScript.load', return_value=FakeModule())
    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_data_ready_sends_onwards_completed(self, rpm, load: Mock):
        "Test data_ready success path sends the message onwards for reduction"
        rpm.return_value.run = partial(self.do_post_started_assertions, 5)
        self.handler.create_run_records = Mock(return_value=(self.reduction_run, self.msg, self.instrument))
        self.handler.data_ready(self.msg)
        assert self.mocked_logger.info.call_count == 1
        assert self.reduction_run.finished is not None
        assert self.reduction_run.status == Status.get_completed()
        load.assert_called_once()

    @patch('autoreduce_qp.queue_processor.reduction.service.ReductionScript.load', return_value=FakeModule())
    @patch("autoreduce_qp.queue_processor.handle_message.ReductionProcessManager")
    def test_data_ready_sends_onwards_error(self, rpm, load: Mock):
        "Test data_ready error path sends the message onwards to be marked as errored"
        self.msg.message = "I am error"
        rpm.return_value.run = partial(self.do_post_started_assertions, 5)
        self.handler.create_run_records = Mock(return_value=(self.reduction_run, self.msg, self.instrument))
        self.handler.data_ready(self.msg)
        assert self.mocked_logger.info.call_count == 1
        assert self.reduction_run.finished is not None
        assert self.reduction_run.status == Status.get_error()
        assert self.reduction_run.message == "I am error"
        load.assert_called_once()

    def test_create_run_records_invalid_rb_number(self):
        """
        Test creating a run record when the rb number is invalid.
        """
        with DefaultDataArchive(self.instrument_name):
            self.msg.rb_number = "INVALID RB NUMBER CALIBRATION RUN PERHAPS"
            reduction_run, _, _ = self.handler.create_run_records(self.msg)
            assert reduction_run.experiment.reference_number == 0

    def test_create_run_records_valid_rb_number(self):
        """
        Test creating a run record when the rb number is invalid.
        """
        with DefaultDataArchive(self.instrument_name):
            reduction_run, _, _ = self.handler.create_run_records(self.msg)
            assert reduction_run.experiment.reference_number == self.msg.rb_number


if __name__ == '__main__':
    main()
