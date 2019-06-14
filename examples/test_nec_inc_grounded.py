#!/usr/bin/env python3

import sys
import copy
from incaffeine.incaf import IncAF
from incaffeine.runner import TestRunner


def ungrounded_completion(af, args):
    grounded = None
    grounded_new = set()
    ungrounded = copy.deepcopy(af)

    # pessimistic reduction for possible attacks
    for a in range(ungrounded.n):
        for b in range(ungrounded.n):
            if ungrounded.R[a][b] == IncAF.POSSIBLE_ATTACK:
                if b in args:
                    ungrounded.R[a][b] = IncAF.DEFINITE_ATTACK
                else:
                    ungrounded.R[a][b] = IncAF.NO_ATTACK

    while grounded_new != grounded:
        grounded = grounded_new
        grounded_new = set()
        maxi = ungrounded.maximal_completion()
        for a in args:
            if maxi.is_defended_by(a, grounded):
                if ungrounded.A[a] == IncAF.POSSIBLE_ARGUMENT:
                    ungrounded.A[a] = IncAF.NO_ARGUMENT
                elif ungrounded.A[a] == IncAF.DEFINITE_ARGUMENT:
                    grounded_new.add(a)
    return ungrounded.maximal_completion()


def ungrounded_simple_completion(af, args):
    ungrounded = copy.deepcopy(af)

    # pessimistic reduction for possible attacks
    for a in range(ungrounded.n):
        for b in range(ungrounded.n):
            if ungrounded.R[a][b] == IncAF.POSSIBLE_ATTACK:
                if b in args:
                    ungrounded.R[a][b] = IncAF.DEFINITE_ATTACK
                else:
                    ungrounded.R[a][b] = IncAF.NO_ATTACK

    # determine G
    # temp = ungrounded.maximal_completion() # variant 1
    temp = ungrounded.minimal_completion()  # variant 2
    grounded = temp.grounded_extension()

    for a in range(ungrounded.n):
        if ungrounded.A[a] == IncAF.POSSIBLE_ARGUMENT:
            if a in grounded:
                ungrounded.A[a] = IncAF.NO_ARGUMENT
            else:
                ungrounded.A[a] = IncAF.DEFINITE_ARGUMENT

    return ungrounded


def check_instance(runner, af, args, arg):
    if not af.necessary_verification(args, IncAF.SEMANTICS_CP):
        return False

    ungrounded = ungrounded_simple_completion(af, args)
    # ungrounded = ungrounded_completion(af, args)
    return ungrounded.is_grounded(args)


def reference_check_instance(runner, af, args, arg):
    return af.necessary_verification(args, IncAF.SEMANTICS_GR)


def main(argv):
    runner = TestRunner('testNecIncGR', check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = True
    runner.use_argument = False
    runner.use_uncertain_args = True
    runner.use_uncertain_attacks = True

    runner.log_on_success = False
    runner.logger_results = sys.stdout

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])
