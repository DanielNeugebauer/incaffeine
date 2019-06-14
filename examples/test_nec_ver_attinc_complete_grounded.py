#!/usr/bin/env python3

import sys
import copy
from incaffeine.incaf import IncAF
from incaffeine.runner import TestRunner


def optimistic_completion(af, args):
    opt = copy.deepcopy(af)
    for attacker in range(af.n):
        for target in range(af.n):
            att = af.R[attacker][target]
            if att == IncAF.POSSIBLE_ATTACK:
                if target not in args:
                    opt.set_attack(attacker, target, IncAF.DEFINITE_ATTACK)
                else:
                    opt.set_attack(attacker, target, IncAF.NO_ATTACK)
            else:
                opt.set_attack(attacker, target, att)
    return opt


def unfixed_completion(af, args):  # for complete/grounded semantics
    # 1: Try to destroy conflict-freeness of args
    # 2: Try to make elements of args unacceptable w.r.t. args, i.e.:
    #    - use ALL attacks against args
    #    - do not use attacks from args that defend it against attackers
    # 3: Try to make elements outside of args acceptable w.r.t. args, i.e.:

    pess = copy.deepcopy(af)
    for attacker in range(af.n):
        for target in range(af.n):
            att = af.R[attacker][target]
            if att == IncAF.POSSIBLE_ATTACK:
                # cf: use attacks against args
                if target in args:
                    pess.set_attack(attacker, target, IncAF.DEFINITE_ATTACK)
                    # print attacker,"->",target," is used because it harms args"
                # acc: discard all attacks that defend args against possible external attacks
                elif (target not in args) and (pess.possibly_attacks(target, args)):
                    pess.set_attack(attacker, target, IncAF.NO_ATTACK)
                    # print attacker,"->",target," is NOT used because it defends args"
                # external conflicts: discard all external conflicts
                elif (target not in args) and (attacker not in args):
                    pess.set_attack(attacker, target, IncAF.NO_ATTACK)
                    # print attacker,"->",target," is NOT used because it is an external conflict"
            else:
                pess.set_attack(attacker, target, att)

    # check if we can achieve accepting external arguments: enable all attacks from args to targets outside of
    # args that are currently acceptable w.r.t. args
    # changedCount = 0
    changed = True
    while changed:
        changed = False
        for target in range(pess.n):
            mini = pess.minimal_completion()
            if target not in args:
                new_args = copy.deepcopy(args)
                new_args.add(target)
                opt = optimistic_completion(pess, new_args)
                if (not mini.is_possibly_acceptable(args, target)) and opt.is_possibly_acceptable(args, target):
                    # if (not pess.isCurrentlyAcceptable(target,args)):
                    # print target, "is not currently acceptable, but possibly acceptable"
                    # print "pess.is_possibly_acceptable(target,args)"
                    # print pess.is_possibly_acceptable(target,args)
                    # print "not pess.isCurrentlyAcceptable(target,args)"
                    # print not pess.isCurrentlyAcceptable(target,args)
                    for attacker in args:
                        for target2 in range(pess.n):
                            if pess.necessarily_attacks(target2, target):
                                att = pess.R[attacker][target2]
                                if att == IncAF.POSSIBLE_ATTACK:
                                    pess.set_attack(attacker, target2, IncAF.DEFINITE_ATTACK)
                                    # print attacker,"->",target2," is used because it defends an external argument"
                                    # changed = True
                                    # changedCount += 1
    # if changedCount > 0:
    #     print('changedCount: ' + changedCount)

    for attacker in range(pess.n):
        for target in range(pess.n):
            att = pess.R[attacker][target]
            if att == IncAF.POSSIBLE_ATTACK:
                pess.set_attack(attacker, target, IncAF.NO_ATTACK)
    return pess


def check_instance(runner, af, args, arg):
    unfixed = unfixed_completion(af, args)
    # return unfixed.verification(args, IncAF.SEMANTICS_CP)
    return af.necessary_verification(args, IncAF.SEMANTICS_CP)


def reference_check_instance(runner, af, args, arg):
    return af.necessary_verification(args, IncAF.SEMANTICS_CP)


def main(argv):
    runner = TestRunner('NecVerAttincGR', check_instance, reference_check_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = True
    runner.use_argument = False
    runner.use_uncertain_args = False
    runner.use_uncertain_attacks = True

    runner.exit_on_failure = True

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])
