#!/usr/bin/env python3

import sys
from incaffeine.incaf import IncAF
from incaffeine.runner import TestRunner


def check_instance(runner, af, args, arg):
    return af.is_possibly_skeptically_acceptable(arg, IncAF.SEMANTICS_ST)


def reference_check_instance(runner, af, args, arg):
    return True


def main(argv):
    runner = TestRunner('PSARatioST', check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = False
    runner.use_argument = True
    runner.use_uncertain_args = True
    runner.use_uncertain_attacks = True

    runner.exit_on_failure = False

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])
