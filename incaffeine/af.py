import copy
import sys
from random import randrange

from incaffeine.helpers import powerset


class AF(object):
    """
    Argumentation Framework.
    """

    NO_ATTACK = 0
    """constant that represents attack state 'no attack' between two arguments."""
    DEFINITE_ATTACK = 1
    """constant that represents attack state 'definite attack' between two arguments."""

    NO_ARGUMENT = 0
    """constant that represents argument state 'no argument' of an argument."""
    DEFINITE_ARGUMENT = 1
    """constant that represents argument state 'definite argument' of an argument."""

    SEMANTICS_CF = 1
    """conflict-free semantics."""
    SEMANTICS_AD = 2
    """admissible semantics."""
    SEMANTICS_CP = 3
    """complete semantics."""
    SEMANTICS_GR = 4
    """grounded semantics."""
    SEMANTICS_ST = 5
    """stable semantics."""
    SEMANTICS_PR = 6
    """preferred semantics."""

    def __init__(self, n):
        self.n = n
        """(int) number of arguments. The set of arguments is [0,...,n-1] implicitly."""
        self.A = [AF.DEFINITE_ARGUMENT for _ in range(n)]
        """(list) argument statuses for each argument"""
        self.R = [[AF.NO_ATTACK for _ in range(n)] for _ in range(n)]
        """(list) attack statuses for each pair of arguments"""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.n != other.n:
                return False
            for arg in range(self.n):
                if self.A[arg] != other.A[arg]:
                    return False
            for attacker in range(self.n):
                for target in range(self.n):
                    if self.R[attacker][target] != other.R[attacker][target]:
                        return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def restricted_extension(self, args):
        """
        Create a copy of the given set of arguments without those arguments that
        do not have status DEFINITE_ARGUMENT in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: set of arguments
        """
        return set(a for a in args if self.A[a] == AF.DEFINITE_ARGUMENT)

    def randomize_attacks(self):
        """
        Set all attack relations in self randomly to NO_ATTACK or DEFINITE_ATTACK.
        """
        for attacker in range(self.n):
            for target in range(self.n):
                self.R[attacker][target] = randrange(AF.NO_ATTACK, AF.DEFINITE_ATTACK + 1)

    def set_attack(self, attacker, target, value):
        """
        Set the attack state from the given attacking argument to the given target argument.

        :param attacker: attacking argument
        :type attacker: int
        :param target: target argument
        :type target: int
        :param value: attack state to be set
        :type value: int
        """
        self.R[attacker][target] = value

    def set_argument(self, argument, value):
        """
        Set the argument state of the given argument.

        :param argument: argument
        :type argument: int
        :param value: argument state to be set
        :type value: int
        """
        self.A[argument] = value

    def pretty_print(self, output_handle=sys.stdout):
        """
        Print a human readable representation of this AF to stdout.

        :param output_handle: output stream or file handle (default: stdout)
        :return:
        """
        for attacker in range(self.n):
            output_handle.write(str(self.R[attacker]))
            output_handle.write('\n')

    def attacks(self, attacker, target):
        """
        Indicates whether whether there is a definite attack from attacker to target in this AF.

        Both attacker and target may be a single argument (int) or an iterable over multiple arguments.

        :param attacker: single attacking argument or set of attacking arguments
        :type attacker: int or iterable
        :param target: single target argument or set of target arguments
        :type target: int or iterable
        :return: true if at least one attacker attacks at least one target, False otherwise
        """
        if type(attacker) is int:
            if self.A[attacker] != AF.DEFINITE_ARGUMENT:
                return False
            if type(target) is int:
                if self.A[target] != AF.DEFINITE_ARGUMENT:
                    return False
                return self.R[attacker][target] == AF.DEFINITE_ATTACK
            else:
                for b in target:
                    if (self.A[b] == AF.DEFINITE_ARGUMENT) \
                            and (self.R[attacker][b] == AF.DEFINITE_ATTACK):
                        return True
                return False
        else:
            if type(target) is int:
                for a in attacker:
                    if (self.A[a] == AF.DEFINITE_ARGUMENT) \
                            and (self.R[a][target] == AF.DEFINITE_ATTACK):
                        return True
                return False
            else:
                for a in attacker:
                    for b in target:
                        if (self.A[a] == AF.DEFINITE_ARGUMENT) \
                                and (self.A[b] == AF.DEFINITE_ARGUMENT) \
                                and (self.R[a][b] == AF.DEFINITE_ATTACK):
                            return True
                return False

    def grounded_extension(self):
        """
        Determine the grounded extension of this AF.

        :return: set of arguments representing the grounded extension
        """
        args = set()
        args_next = set()
        for a in range(self.n):
            if self.A[a] == AF.DEFINITE_ARGUMENT:
                if self.is_defended_by(a, args):
                    args_next.add(a)
        while args != args_next:
            args = args_next
            args_next = set()
            for a in range(self.n):
                if self.A[a] == AF.DEFINITE_ARGUMENT:
                    if self.is_defended_by(a, args):
                        args_next.add(a)
        return args

    def is_conflict_free(self, args):
        """
        Indicates whether the given set of arguments is conflict-free in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is conflict-free, False otherwise
        """
        args = self.restricted_extension(args)
        for attacker in args:
            for target in args:
                if self.R[attacker][target] == AF.DEFINITE_ATTACK:
                    return False
        return True

    def is_defended_by(self, a, args):
        """
        Indicates whether the given argument is defended by the given set of arguments in this AF.

        Always returns True if the argument does not have status DEFINITE_ARGUMENT in self.

        :param a: the argument to be checked
        :type a: int
        :param args: defending set of arguments
        :type args: iterable
        :return: True if a is acceptable with respect to args in self, False otherwise
        """
        args = self.restricted_extension(args)
        if self.A[a] == AF.DEFINITE_ARGUMENT:
            for attacker in range(self.n):
                if (self.A[attacker] == AF.DEFINITE_ARGUMENT) and (self.R[attacker][a] == AF.DEFINITE_ATTACK):
                    if not self.attacks(args, attacker):
                        return False
        return True

    def is_admissible(self, args):
        """
        Indicates whether the given set of arguments is admissible in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is admissible, False otherwise
        """
        args = self.restricted_extension(args)
        if not self.is_conflict_free(args):
            return False
        for a in args:
            if not self.is_defended_by(a, args):
                return False
        return True

    def is_stable(self, args):
        """
        Indicates whether the given set of arguments is stable in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is stable, False otherwise
        """
        args_restricted = self.restricted_extension(args)
        if not self.is_conflict_free(args_restricted):
            return False
        for target in range(self.n):
            if target not in args:
                if (self.A[target] == AF.DEFINITE_ARGUMENT) and not self.attacks(args_restricted, target):
                    return False
        return True

    def is_grounded(self, args):
        """
        Indicates whether the given set of arguments is grounded in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is grounded, False otherwise
        """
        args = self.restricted_extension(args)
        return self.grounded_extension() == args

    def is_complete(self, args):
        """
        Indicates whether the given set of arguments is complete in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is complete, False otherwise
        """
        args = self.restricted_extension(args)
        if not self.is_admissible(args):
            return False
        for a in range(self.n):
            if (self.A[a] == AF.DEFINITE_ARGUMENT) and (a not in args) and (self.is_defended_by(a, args)):
                return False
        return True

    def is_preferred(self, args):
        """
        Indicates whether the given set of arguments is preferred in this AF.

        :param args: set of arguments
        :type args: iterable
        :return: True if args is preferred, False otherwise
        """
        args = self.restricted_extension(args)
        if not self.is_admissible(args):
            return False
        args2 = copy.deepcopy(args)
        possible_args = []
        for argument in range(self.n):
            if self.A[argument] == AF.DEFINITE_ARGUMENT \
                    and argument not in args \
                    and not self.attacks(argument, args) \
                    and not self.attacks(args, argument):
                possible_args.append(argument)
        return not self.is_dominated(args, args2, possible_args, len(possible_args))

    def is_dominated(self, args1, args2, possible_args, k):
        """
        Indicates whether the first set of arguments is dominated by the second set of arguments in this AF.

        A set args1 is dominated by a set args2 if args2 is a strict admissible superset of args1.
        Intended for internal use in is_preferred!

        :param args1: first set
        :type args1: iterable
        :param args2: second set
        :type args2: iterable
        :param possible_args: candidates to be added to args2
        :type possible_args: iterable
        :param k: length of possible_args
        :type k: int
        :return: True if the first set is dominated by the second set in self, False otherwise
        """
        if k == 0:
            if args1 == args2:
                return False
            return self.is_admissible(args2)
        k -= 1
        possible_arg = possible_args[k]
        if self.is_dominated(args1, args2, possible_args, k):
            return True
        args2.add(possible_arg)
        if self.is_dominated(args1, args2, possible_args, k):
            return True
        args2.remove(possible_arg)
        return False

    def verification(self, args, semantics):
        if semantics == self.SEMANTICS_CF:
            return self.is_conflict_free(args)
        elif semantics == self.SEMANTICS_AD:
            return self.is_admissible(args)
        elif semantics == self.SEMANTICS_CP:
            return self.is_complete(args)
        elif semantics == self.SEMANTICS_GR:
            return self.is_grounded(args)
        elif semantics == self.SEMANTICS_ST:
            return self.is_stable(args)
        elif semantics == self.SEMANTICS_PR:
            return self.is_preferred(args)
        print('warning: unknown semantics used for verification: %d', int(semantics))
        return False

    def credulously_satisfied(self, condition):
        af = copy.deepcopy(self)
        args = set()
        n_current = 0
        n_max = self.n
        return af.credulously_satisfied_rec(condition, args, n_current, n_max)

    def credulously_satisfied_rec(self, condition, args, n_current, n_max):
        if n_current == n_max:
            return condition(self)
        n_current += 1
        if self.credulously_satisfied_rec(condition, args, n_current, n_max):
            return True
        args.add(n_current)
        if self.credulously_satisfied_rec(condition, args, n_current, n_max):
            return True
        args.remove(n_current)
        return False

    def skeptically_satisfied(self, condition):
        af = copy.deepcopy(self)
        args = set()
        n_current = 0
        n_max = self.n
        return af.skeptically_satisfied_rec(condition, args, n_current, n_max)

    def skeptically_satisfied_rec(self, condition, args, n_current, n_max):
        if n_current == n_max:
            return condition(self)
        n_current += 1
        if not self.skeptically_satisfied_rec(condition, args, n_current, n_max):
            return False
        args.add(n_current)
        if not self.skeptically_satisfied_rec(condition, args, n_current, n_max):
            return False
        args.remove(n_current)
        return True

    def is_credulously_acceptable(self, arg, semantics):
        def condition(af):
            # check all arg sets INCLUDING arg: if one of them is an extension, return True
            arg_range = [i for i in range(self.n)]
            arg_range.remove(arg)
            for base_tuple in powerset(arg_range):
                superset = set(base_tuple)
                superset.add(arg)
                if af.verification(superset, semantics):
                    return True
            return False
        return self.credulously_satisfied(condition)

    def is_skeptically_acceptable(self, arg, semantics):
        def condition(af):
            # check all arg sets EXCLUDING arg: if one of them is an extension, return False
            arg_range = [i for i in range(self.n)]
            arg_range.remove(arg)
            for base_tuple in powerset(arg_range):
                superset = set(base_tuple)
                if af.verification(superset, semantics):
                    return False
            return True
        return self.skeptically_satisfied(condition)
