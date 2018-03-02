#!/usr/bin/env python3

import unittest
import sys
import copy
sys.path.append('../')

from incaffeine.runner import TestRunner

previous_instances = []


def check_instance(runner, af, args, arg):
    global previous_instances
    new_instance = {'af': copy.deepcopy(af), 'args': copy.deepcopy(args), 'arg': copy.deepcopy(arg)}
    result = True
    for other_instance in previous_instances:
        if af == other_instance['af'] \
                and args == other_instance['args'] \
                and arg == other_instance['arg']:
            result = False
            runner.log_af(other_instance['af'])
            if runner.use_extension:
                runner.log_extension(other_instance['args'])
            if runner.use_argument:
                runner.log_argument(other_instance['arg'])
            break
    previous_instances.append(new_instance)

    return result


def reference_check_instance(runner, af, args, arg):
    return True


class TestGeneratorCorrectness(unittest.TestCase):

    def test_1_2_F_F_F_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_F_F_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = False
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_F_F_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_F_F_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = False
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_T_F_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_T_F_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = True
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_F_T_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_F_T_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = False
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_F_F_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_F_F_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = False
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_T_F_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_T_F_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = True
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_F_T_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_F_T_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = False
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_F_F_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_F_F_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = False
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_T_T_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_T_T_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = True
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_T_F_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_T_F_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = True
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_F_T_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_F_T_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = False
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_T_T_F(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_T_T_F', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = True
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = False

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_T_F_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_T_F_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = True
        runner.use_uncertain_args = False
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_F_T_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_F_T_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = False
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_F_T_T_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_F_T_T_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = False
        runner.use_argument = True
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)

    def test_1_2_T_T_T_T(self):
        global previous_instances
        previous_instances = []
        runner = TestRunner('test_1_2_T_T_T_T', check_instance, reference_check_instance)

        # Config
        runner.use_extension = True
        runner.use_argument = True
        runner.use_uncertain_args = True
        runner.use_uncertain_attacks = True

        runner.log_results_to_stream = True
        runner.exit_on_failure = True

        runner.n_min = 1
        runner.n_max = 2

        # Run!
        runner.run()

        self.assertEqual(runner.current_count, runner.success_count)


if __name__ == "__main__":
    unittest.main()
