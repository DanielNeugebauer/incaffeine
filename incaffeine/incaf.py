import copy
from af import AF


class IncAF(AF):
    """
    Incomplete Argumentation Framework.
    """

    POSSIBLE_ARGUMENT = -1
    """constant that represents argument state 'possible argument' of an argument."""
    POSSIBLE_ATTACK = -1
    """constant that represents attack state 'possible attack' of an attack."""

    def maximal_completion(self):
        maxi = IncAF(self.n)
        for i in range(self.n):
            arg = self.A[i]
            if arg == IncAF.POSSIBLE_ARGUMENT:
                maxi.set_argument(i, IncAF.DEFINITE_ARGUMENT)
            else:
                maxi.set_argument(i, arg)
        for attacker in range(self.n):
            for target in range(self.n):
                att = self.R[attacker][target]
                if att == IncAF.POSSIBLE_ATTACK:
                    maxi.set_attack(attacker, target, IncAF.DEFINITE_ATTACK)
                else:
                    maxi.set_attack(attacker, target, att)
        return maxi

    def minimal_completion(self):
        mini = IncAF(self.n)
        for i in range(self.n):
            arg = self.A[i]
            if arg == IncAF.POSSIBLE_ARGUMENT:
                mini.set_argument(i, IncAF.NO_ARGUMENT)
            else:
                mini.set_argument(i, arg)
        for attacker in range(self.n):
            for target in range(self.n):
                att = self.R[attacker][target]
                if att == IncAF.POSSIBLE_ATTACK:
                    mini.set_attack(attacker, target, IncAF.NO_ATTACK)
                else:
                    mini.set_attack(attacker, target, att)
        return mini

    # ------------------------------------------------------------------------------------------------
    # Simple, polynomial solutions to possible/necessary problem variants.

    def possibly_attacks(self, attacker, target):
        if type(attacker) is int:
            if self.A[attacker] == IncAF.NO_ARGUMENT:
                return False
            if type(target) is int:
                if self.A[target] == IncAF.NO_ARGUMENT:
                    return False
                return self.R[attacker][target] != IncAF.NO_ATTACK
            else:
                for b in target:
                    if (self.A[b] != IncAF.NO_ARGUMENT) and (self.R[attacker][b] != IncAF.NO_ATTACK):
                        return True
                return False
        else:
            if type(target) is int:
                for a in attacker:
                    if (self.A[a] != IncAF.NO_ARGUMENT) and (self.R[a][target] != IncAF.NO_ATTACK):
                        return True
                return False
            else:
                for a in attacker:
                    for b in target:
                        if (self.A[a] != IncAF.NO_ARGUMENT) and (self.A[b] != IncAF.NO_ARGUMENT) and (
                                self.R[a][b] != IncAF.NO_ATTACK):
                            return True
                return False

    def necessarily_attacks(self, attacker, target):
        if type(attacker) is int:
            if self.A[attacker] != IncAF.DEFINITE_ARGUMENT:
                return False
            if type(target) is int:
                if self.A[target] != IncAF.DEFINITE_ARGUMENT:
                    return False
                return self.R[attacker][target] == IncAF.DEFINITE_ATTACK
            else:
                for b in target:
                    if (self.A[b] == IncAF.DEFINITE_ARGUMENT) and (self.R[attacker][b] == IncAF.DEFINITE_ATTACK):
                        return True
                return False
        else:
            if type(target) is int:
                for a in attacker:
                    if (self.A[a] == IncAF.DEFINITE_ARGUMENT) and (self.R[a][target] == IncAF.DEFINITE_ATTACK):
                        return True
                return False
            else:
                for a in attacker:
                    for b in target:
                        if (self.A[a] == IncAF.DEFINITE_ARGUMENT) and (self.A[b] == IncAF.DEFINITE_ARGUMENT) and (
                                self.R[a][b] == IncAF.DEFINITE_ATTACK):
                            return True
                return False

    def is_possibly_conflict_free(self, args):
        for attacker in args:
            for target in args:
                if self.A[attacker] == IncAF.DEFINITE_ARGUMENT \
                        and self.A[target] == IncAF.DEFINITE_ARGUMENT \
                        and self.R[attacker][target] == IncAF.DEFINITE_ATTACK:
                    return False
        return True

    def is_necessarily_conflict_free(self, args):
        for attacker in args:
            for target in args:
                if self.A[attacker] != IncAF.NO_ARGUMENT \
                        and self.A[target] != IncAF.NO_ARGUMENT \
                        and self.R[attacker][target] != IncAF.NO_ATTACK:
                    return False
        return True

    # ------------------------------------------------------------------------------------------------
    # Naive, exponential solutions to possible/necessary problems variants.

    def possible_verification(self, args, semantics):
        af = copy.deepcopy(self)
        possible_attacks = []
        for attacker in range(af.n):
            for target in range(af.n):
                if af.R[attacker][target] == IncAF.POSSIBLE_ATTACK:
                    possible_attacks.append((attacker, target))
        possible_arguments = []
        for arg in range(af.n):
            if af.A[arg] == IncAF.POSSIBLE_ARGUMENT:
                possible_arguments.append(arg)
        return af.possible_verification_rec(args, semantics, possible_attacks, len(possible_attacks),
                                            possible_arguments, len(possible_arguments))

    def possible_verification_rec(self, args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return self.verification(args, semantics)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if self.possible_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if self.possible_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return False

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if self.possible_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if self.possible_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return False

    def necessary_verification(self, args, semantics):
        af = copy.deepcopy(self)
        possible_attacks = []
        for attacker in range(af.n):
            for target in range(af.n):
                if af.R[attacker][target] == IncAF.POSSIBLE_ATTACK:
                    possible_attacks.append((attacker, target))
        possible_arguments = []
        for arg in range(af.n):
            if af.A[arg] == IncAF.POSSIBLE_ARGUMENT:
                possible_arguments.append(arg)
        return af.necessary_verification_rec(args, semantics, possible_attacks, len(possible_attacks),
                                             possible_arguments, len(possible_arguments))

    def necessary_verification_rec(self, args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return self.verification(args, semantics)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if not self.necessary_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if not self.necessary_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return True

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if not self.necessary_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if not self.necessary_verification_rec(args, semantics, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return True

    def is_possibly_acceptable(self, a, args):
        af = copy.deepcopy(self)
        possible_attacks = []
        for attacker in range(af.n):
            for target in range(af.n):
                if af.R[attacker][target] == IncAF.POSSIBLE_ATTACK:
                    possible_attacks.append((attacker, target))
        possible_arguments = []
        for arg in range(af.n):
            if af.A[arg] == IncAF.POSSIBLE_ARGUMENT:
                possible_arguments.append(arg)
        return af.is_possibly_acceptable_rec_incaf(a, args, possible_attacks, len(possible_attacks),
                                                   possible_arguments, len(possible_arguments))

    def is_possibly_acceptable_rec_incaf(self, a, args, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return self.is_acceptable(a, args)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if self.is_possibly_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if self.is_possibly_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return False

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if self.is_possibly_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if self.is_possibly_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return False

    def is_necessarily_acceptable(self, a, args):
        af = copy.deepcopy(self)
        possible_attacks = []
        for attacker in range(af.n):
            for target in range(af.n):
                if af.R[attacker][target] == IncAF.POSSIBLE_ATTACK:
                    possible_attacks.append((attacker, target))
        possible_arguments = []
        for arg in range(af.n):
            if af.A[arg] == IncAF.POSSIBLE_ARGUMENT:
                possible_arguments.append(arg)
        return af.is_necessarily_acceptable_rec_incaf(a, args, possible_attacks, len(possible_attacks),
                                                      possible_arguments, len(possible_arguments))

    def is_necessarily_acceptable_rec_incaf(self, a, args, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return self.is_acceptable(a, args)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if not self.is_necessarily_acceptable_rec_incaf(a, args, possible_attacks, k_att,
                                                            possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if not self.is_necessarily_acceptable_rec_incaf(a, args, possible_attacks, k_att,
                                                            possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return True

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if not self.is_necessarily_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if not self.is_necessarily_acceptable_rec_incaf(a, args, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return True
