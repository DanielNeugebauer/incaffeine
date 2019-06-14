#!/usr/bin/env python3

import sys
import copy
from incaffeine.incaf import IncAF
from incaffeine.runner import TestRunner


def version1(af, arg):
    grounded = copy.deepcopy(af)

    # Exclude all possible attacks against arg
    for attacker in range(grounded.n):
        if grounded.R[attacker][arg] == IncAF.POSSIBLE_ATTACK:
            grounded.R[attacker][arg] = IncAF.NO_ATTACK

    # Include all possible attacks against definite attackers of arg
    definite_attackers_1 = []
    definite_defenders_1 = []
    for attacker in range(grounded.n):
        if grounded.R[attacker][arg] == IncAF.DEFINITE_ATTACK:
            definite_attackers_1.append(attacker)
            for defender in range(grounded.n):
                if grounded.R[defender][attacker] == IncAF.POSSIBLE_ATTACK:
                    grounded.R[defender][attacker] = IncAF.DEFINITE_ATTACK
                if grounded.R[defender][attacker] == IncAF.DEFINITE_ATTACK:
                    definite_defenders_1.append(defender)

    # Exclude all possible attacks against definite defenders of arg
    for defender in definite_defenders_1:
        for attacker in range(grounded.n):
            if grounded.R[attacker][defender] == IncAF.POSSIBLE_ATTACK:
                grounded.R[attacker][defender] = IncAF.NO_ATTACK

    # Include all possible attacks against level-2 attackers of arg
    definite_attackers_2 = []
    definite_defenders_2 = []
    for attacker in range(grounded.n):
        for defender in definite_defenders_1:
            if grounded.R[attacker][defender] == IncAF.DEFINITE_ATTACK:
                definite_attackers_2.append(attacker)
                for defender2 in range(grounded.n):
                    if grounded.R[defender2][attacker] == IncAF.POSSIBLE_ATTACK:
                        grounded.R[defender2][attacker] = IncAF.DEFINITE_ATTACK
                    if grounded.R[defender2][attacker] == IncAF.DEFINITE_ATTACK:
                        definite_defenders_2.append(defender2)

    # check if we are done?
    grounded = grounded.maximal_completion()

    return grounded.is_possibly_credulously_acceptable(arg, IncAF.SEMANTICS_GR)


def version2(af, arg):
    grounded = copy.deepcopy(af)

    attackers = set([])
    defenders = {arg}

    changes = True
    while changes:
        changes = False

        # Exclude all possible attacks against defenders
        for defender in defenders:
            for attacker in range(grounded.n):
                if grounded.R[attacker][defender] == IncAF.POSSIBLE_ATTACK:
                    grounded.R[attacker][defender] = IncAF.NO_ATTACK
                    changes = True
                elif grounded.R[attacker][defender] == IncAF.DEFINITE_ATTACK:
                    attackers.add(attacker)

        # Include all possible attacks against attackers
        for attacker in attackers:
            for defender in range(grounded.n):
                if grounded.R[defender][attacker] == IncAF.POSSIBLE_ATTACK:
                    grounded.R[defender][attacker] = IncAF.DEFINITE_ATTACK
                    changes = True
                if grounded.R[defender][attacker] == IncAF.DEFINITE_ATTACK:
                    defenders.add(defender)

    return grounded.is_possibly_credulously_acceptable(arg, IncAF.SEMANTICS_GR)


def check_instance(runner, af, args, arg):
    # return version1(af, arg)
    return version2(af, arg)


def reference_check_instance(runner, af, args, arg):
    return af.is_possibly_credulously_acceptable(arg, IncAF.SEMANTICS_GR)


def main(argv):
    runner = TestRunner('PosCredAttincGR', check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = False
    runner.use_argument = True
    runner.use_uncertain_args = False
    runner.use_uncertain_attacks = True

    runner.exit_on_failure = True

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])
