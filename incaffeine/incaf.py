import copy
from incaffeine.af import AF


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
        def condition(af):
            return af.verification(args, semantics)
        return self.possibly_satisfied(condition)

    def necessary_verification(self, args, semantics):
        def condition(af):
            return af.verification(args, semantics)
        return self.necessarily_satisfied(condition)

    def is_possibly_acceptable(self, args, arg):
        if self.A[arg] == IncAF.NO_ARGUMENT:
            # Excluded arguments cannot be possibly acceptable
            return False

        def condition(af):
            return af.is_defended_by(arg, args)
        return self.possibly_satisfied(condition)

    def is_necessarily_acceptable(self, args, arg):
        if self.A[arg] != IncAF.DEFINITE_ARGUMENT:
            # Only definite arguments can be necessarily acceptable
            return False

        def condition(af):
            return af.is_defended_by(arg, args)
        return self.necessarily_satisfied(condition)

    def is_possibly_credulously_acceptable(self, arg, semantics):
        if self.A[arg] == IncAF.NO_ARGUMENT:
            # Excluded arguments cannot be possibly acceptable
            return False

        def condition(af):
            return af.is_credulously_acceptable(arg, semantics)
        return self.possibly_satisfied(condition)

    def is_necessarily_credulously_acceptable(self, arg, semantics):
        if self.A[arg] != IncAF.DEFINITE_ARGUMENT:
            # Only definite arguments can be necessarily acceptable
            return False

        def condition(af):
            return af.is_credulously_acceptable(arg, semantics)
        return self.necessarily_satisfied(condition)

    def is_possibly_skeptically_acceptable(self, arg, semantics):
        if self.A[arg] == IncAF.NO_ARGUMENT:
            # Excluded arguments cannot be possibly acceptable
            return False

        def condition(af):
            return af.is_skeptically_acceptable(arg, semantics)
        return self.possibly_satisfied(condition)

    def is_necessarily_skeptically_acceptable(self, arg, semantics):
        if self.A[arg] != IncAF.DEFINITE_ARGUMENT:
            # Only definite arguments can be necessarily acceptable
            return False

        def condition(af):
            return af.is_skeptically_acceptable(arg, semantics)
        return self.necessarily_satisfied(condition)

    def possibly_satisfied(self, condition):
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
        return af.possibly_satisfied_rec(condition, possible_attacks, len(possible_attacks),
                                         possible_arguments, len(possible_arguments))

    def possibly_satisfied_rec(self, condition, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return condition(self)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if self.possibly_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if self.possibly_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
                return True
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return False

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if self.possibly_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if self.possibly_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
            return True
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return False

    def necessarily_satisfied(self, condition):
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
        return af.necessarily_satisfied_rec(condition, possible_attacks, len(possible_attacks),
                                            possible_arguments, len(possible_arguments))

    def necessarily_satisfied_rec(self, condition, possible_attacks, k_att, possible_arguments, k_arg):
        if k_att == 0:
            if k_arg == 0:
                return condition(self)

            k_arg -= 1
            possible_argument = possible_arguments[k_arg]
            self.set_argument(possible_argument, IncAF.DEFINITE_ARGUMENT)
            if not self.necessarily_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.NO_ARGUMENT)
            if not self.necessarily_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
                return False
            self.set_argument(possible_argument, IncAF.POSSIBLE_ARGUMENT)
            return True

        k_att -= 1
        possible_attack = possible_attacks[k_att]
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.DEFINITE_ATTACK)
        if not self.necessarily_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.NO_ATTACK)
        if not self.necessarily_satisfied_rec(condition, possible_attacks, k_att, possible_arguments, k_arg):
            return False
        self.set_attack(possible_attack[0], possible_attack[1], IncAF.POSSIBLE_ATTACK)
        return True
