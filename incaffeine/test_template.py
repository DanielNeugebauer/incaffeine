#!/usr/bin/env python3

import sys
from runner import TestRunner

print('Script start... ------------------------------------')
print('Testing dummy...')


def check_instance(runner, af, args, arg):
    # TODO implement instance test here!
    return True


def reference_check_instance(runner, af, args, arg):
    # TODO call reference instance test here!
    return True


def main(argv):
    runner = TestRunner(check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = False
    runner.use_argument = False
    runner.use_uncertain_args = False
    runner.use_uncertain_attacks = True

    runner.log_on_success = False
    runner.logger_results = sys.stdout

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])

print("...finished ----------------------------------------")