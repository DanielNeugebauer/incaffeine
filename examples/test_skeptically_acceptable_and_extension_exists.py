#!/usr/bin/env python3

import sys
from incaffeine.af import AF
from incaffeine.runner import TestRunner
"""
Check if the implementation of ExSA provides the same answers as the conjunction of SA and CA
"""


def check_instance(runner, af, args, arg):
    """Compute ExSA"""
    return af.is_skeptically_acceptable_and_extension_exists(arg, AF.SEMANTICS_ST)


def reference_check_instance(runner, af, args, arg):
    """Compute SA && CA"""
    return af.is_skeptically_acceptable(arg, AF.SEMANTICS_ST) and af.is_credulously_acceptable(arg, AF.SEMANTICS_ST)


def main(argv):
    runner = TestRunner('ExSA', check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = False
    runner.use_argument = True
    runner.use_uncertain_args = False
    runner.use_uncertain_attacks = False

    runner.log_on_success = False
    runner.log_results_to_stream = True

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])
