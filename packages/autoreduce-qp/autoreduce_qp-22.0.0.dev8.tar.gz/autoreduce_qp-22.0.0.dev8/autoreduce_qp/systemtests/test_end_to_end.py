# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Linux only!
Tests that data can traverse through the autoreduction system successfully
"""
from typing import Union

from parameterized.parameterized import parameterized

from autoreduce_qp.systemtests.base_systemtest import (BaseAutoreduceSystemTest, REDUCE_SCRIPT,
                                                       SYNTAX_ERROR_REDUCE_SCRIPT, VARS_SCRIPT)


class TestEndToEnd(BaseAutoreduceSystemTest):
    """ Class to test pipelines in autoreduction"""
    @parameterized.expand([
        [222, 222],
        ["INVALID RB NUMBER CALIBRATION RUN PERHAPS",
         0]  # the expected_rb_number is 0 because the initial RB number is not an int
    ])
    def test_end_to_end_wish_invalid_rb_number_skipped(self, rb_number: Union[int, str], expected_rb_number: int):
        """
        Test that data gets skipped when the RB Number doesn't validate.
        """
        # Set meta data for test
        self.rb_number = rb_number
        self.data_ready_message.rb_number = self.rb_number

        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script='')
        self.data_ready_message.data = file_location
        results = self.send_and_wait_for_result(self.data_ready_message)

        # Validate
        self.assertEqual(self.instrument, results[0].instrument.name)
        self.assertEqual(expected_rb_number, results[0].experiment.reference_number)
        self.assertEqual(self.run_number, results[0].run_number)
        self.assertEqual("This is a system test", results[0].run_description)
        self.assertEqual('Skipped', results[0].status.value_verbose())

    def test_end_to_end_wish_completed(self):
        """
        Test that runs gets completed when everything is OK
        """
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script='')
        self.data_ready_message.data = file_location
        results = self.send_and_wait_for_result(self.data_ready_message)

        # Validate
        self.assertEqual(self.instrument, results[0].instrument.name)
        self.assertEqual(self.rb_number, results[0].experiment.reference_number)
        self.assertEqual(self.run_number, results[0].run_number)
        self.assertEqual("This is a system test", results[0].run_description)
        self.assertEqual('Completed', results[0].status.value_verbose(),
                         "Reduction log: %s\nAdmin log: %s" % (results[0].reduction_log, results[0].admin_log))

    def test_end_to_end_wish_bad_script_syntax_error(self):
        """
        Test that run gets marked as error when the script has a syntax error
        """
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=SYNTAX_ERROR_REDUCE_SCRIPT, vars_script='')
        self.data_ready_message.data = file_location
        results = self.send_and_wait_for_result(self.data_ready_message)

        # Validate
        self.assertEqual(self.instrument, results[0].instrument.name)
        self.assertEqual(self.rb_number, results[0].experiment.reference_number)
        self.assertEqual(self.run_number, results[0].run_number)
        self.assertEqual("This is a system test", results[0].run_description)
        self.assertEqual('Error', results[0].status.value_verbose())

        self.assertIn("Error encountered when running the reduction script", results[0].message)
        self.assertIn("SyntaxError('EOL while scanning string literal'", results[0].reduction_log)

    def test_end_to_end_wish_bad_script_raises_exception(self):
        """
        Test that WISH data goes through the system without issue
        """
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script="raise ValueError('hello from the other side')",
                                                    vars_script='')
        self.data_ready_message.data = file_location
        results = self.send_and_wait_for_result(self.data_ready_message)

        # Validate
        self.assertEqual(self.instrument, results[0].instrument.name)
        self.assertEqual(self.rb_number, results[0].experiment.reference_number)
        self.assertEqual(self.run_number, results[0].run_number)
        self.assertEqual("This is a system test", results[0].run_description)
        self.assertEqual('Error', results[0].status.value_verbose())
        self.assertIn('Error encountered when running the reduction script', results[0].message)
        self.assertIn('Exception in reduction script', results[0].reduction_log)
        self.assertIn('hello from the other side', results[0].reduction_log)

    def test_end_to_end_wish_vars_script_gets_new_variable(self):
        """Test running the same run twice, but the second time the reduce_vars has a new variable"""
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script='')
        self.data_ready_message.data = file_location
        result_one = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_one) == 1
        run_without_vars = result_one[0]

        self.data_archive.add_reduce_vars_script(self.instrument, VARS_SCRIPT)
        result_two = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_two) == 2
        assert run_without_vars == result_two[0]  # check that the first run is queried again

        run_with_vars = result_two[1]
        assert run_without_vars.run_variables.count() == 0
        assert run_with_vars.run_variables.count() == 1  # the one standard variable in the VARS_SCRIPT
        var = run_with_vars.run_variables.first().variable
        assert var.name == "variable1"
        assert var.value == "value1"

    def test_end_to_end_wish_vars_script_loses_variable(self):
        """Test running the same run twice, but the second time the reduce_vars has one less variable"""
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script=VARS_SCRIPT)
        self.data_ready_message.data = file_location
        result_one = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_one) == 1
        run_with_vars = result_one[0]
        assert run_with_vars.run_variables.count() == 1  # the one standard variable in the VARS_SCRIPT
        var = run_with_vars.run_variables.first().variable
        assert var.name == "variable1"
        assert var.value == "value1"

        self.data_archive.add_reduce_vars_script(self.instrument, "")
        result_two = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_two) == 2
        assert run_with_vars == result_two[0]
        run_without_vars = result_two[1]
        assert run_without_vars.run_variables.count() == 0

    def test_end_to_end_vars_script_has_variable_value_changed(self):
        """Test that reducing the same run after changing the reduce_vars updates the variable's value"""
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script=VARS_SCRIPT)
        self.data_ready_message.data = file_location
        result_one = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_one) == 1
        run_with_initial_var = result_one[0]
        assert run_with_initial_var.run_variables.count() == 1  # the one standard variable in the VARS_SCRIPT
        var = run_with_initial_var.run_variables.first().variable
        assert var.name == "variable1"
        assert var.value == "value1"

        self.data_archive.add_reduce_vars_script(self.instrument, 'standard_vars={"variable1": 123}')
        result_two = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_two) == 2
        assert run_with_initial_var == result_two[0]

        run_with_changed_var = result_two[1]

        assert run_with_initial_var.run_variables.count() == 1
        assert run_with_changed_var.run_variables.count() == 1

        initial_var = run_with_initial_var.run_variables.first().variable
        changed_var = run_with_changed_var.run_variables.first().variable

        assert initial_var == changed_var

    def test_end_to_end_wish_vars_script_has_variable_reused_on_new_run_number(self):
        """Test that the variables are reused on new run numbers, IF their value has not changed"""
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script=VARS_SCRIPT)
        self.data_ready_message.data = file_location
        result_one = self.send_and_wait_for_result(self.data_ready_message)

        run_with_initial_var = result_one[0]

        self.data_ready_message.run_number = 1234568
        result_two = self.send_and_wait_for_result(self.data_ready_message)
        run_with_different_run_number = result_two[0]

        assert run_with_initial_var.run_variables.count() == 1
        assert run_with_different_run_number.run_variables.count() == 1

        initial_var = run_with_initial_var.run_variables.first().variable
        new_var = run_with_different_run_number.run_variables.first().variable

        assert initial_var == new_var

    def test_end_to_end_wish_vars_script_has_variable_copied_on_new_run_number_when_value_changed(self):
        """Test that the variable is copied for a new run WHEN it's value has been changed"""
        # Create supporting data structures e.g. Data Archive, Reduce directory
        file_location = self._setup_data_structures(reduce_script=REDUCE_SCRIPT, vars_script=VARS_SCRIPT)

        self.run_number = 101
        self.data_ready_message.data = file_location
        result_one = self.send_and_wait_for_result(self.data_ready_message)

        assert len(result_one) == 1
        run_with_initial_var = result_one[0]
        assert run_with_initial_var.run_variables.count() == 1  # the one standard variable in the VARS_SCRIPT
        var = run_with_initial_var.run_variables.first().variable
        assert var.name == "variable1"
        assert var.value == "value1"

        # update the run number in the class because it's used to query for the correct run
        self.data_ready_message.run_number = self.run_number = 102
        self.data_archive.add_reduce_vars_script(self.instrument, 'standard_vars={"variable1": 123}')
        result_two = self.send_and_wait_for_result(self.data_ready_message)

        # making the run_number a list so that they can be deleted by the tearDown!
        self.run_number = [101, 102]

        assert len(result_two) == 1

        run_with_changed_var = result_two[0]

        assert run_with_initial_var.run_variables.count() == 1
        assert run_with_changed_var.run_variables.count() == 1

        initial_var = run_with_initial_var.run_variables.first().variable
        changed_var = run_with_changed_var.run_variables.first().variable

        assert initial_var != changed_var
        assert initial_var.name == changed_var.name
        assert initial_var.value != changed_var.value
        assert initial_var.type != changed_var.type
        assert initial_var.instrumentvariable.start_run < changed_var.instrumentvariable.start_run
