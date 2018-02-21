from incaf import IncAF


class Test:
    currentCount = 0
    totalCount = 0

    def run_randomized(self, n_min, n_max, sample_size, test):
        self.currentCount = 0
        self.totalCount = 0
        for n in range(n_min, n_max + 1):
            number_of_extensions = (n + 1)
            number_of_arguments = n
            number_of_argument_states = 2
            self.totalCount += (number_of_extensions * sample_size * number_of_argument_states ** number_of_arguments)
        for n in range(n_min, n_max + 1):
            k2 = n
            af = IncAF(n)
            self.run_randomized_rec(af, n, sample_size, k2, test)

    def run_randomized_rec(self, af, n, sample_size, k2, test):
        if k2 == 0:
            S = set()
            for i in range(0, n + 1):
                for j in range(sample_size):
                    af.randomizeAttacks()
                    self.currentCount += 1
                    test(af, S, n, self.currentCount, self.totalCount)
                S.add(i)
            return

        k2 -= 1
        self.set_argument(af, n, k2, IncAF.POSSIBLE_ARGUMENT)
        self.run_randomized_rec(af, n, sample_size, k2, test)
        self.set_argument(af, n, k2, IncAF.DEFINITE_ARGUMENT)
        self.run_randomized_rec(af, n, sample_size, k2, test)
        return

    def run_exhaustive(self, n_min, n_max, test):
        self.currentCount = 0
        self.totalCount = 0
        for n in range(n_min, n_max + 1):
            number_of_extensions = (n + 1)
            number_of_attacks = (n ** 2)
            number_of_attack_states = 3
            number_of_arguments = n
            number_of_argument_states = 2
            self.totalCount += (number_of_extensions * number_of_attack_states ** number_of_attacks *
                                number_of_argument_states ** number_of_arguments)
        for n in range(n_min, n_max + 1):
            k1 = n ** 2
            k2 = n
            af = IncAF(n)
            self.run_exhaustive_rec(af, n, k1, k2, test)

    def run_exhaustive_rec(self, af, n, k1, k2, test):
        if k1 == 0:
            if k2 == 0:
                S = set()
                for i in range(0, n + 1):
                    self.currentCount += 1
                    test(af, S, n, self.currentCount, self.totalCount)
                    S.add(i)
                return

            k2 -= 1
            self.set_argument(af, n, k2, IncAF.POSSIBLE_ARGUMENT)
            self.run_exhaustive_rec(af, n, k1, k2, test)
            self.set_argument(af, n, k2, IncAF.DEFINITE_ARGUMENT)
            self.run_exhaustive_rec(af, n, k1, k2, test)
            return

        k1 -= 1
        self.set_attack(af, n, k1, IncAF.NO_ATTACK)
        self.run_exhaustive_rec(af, n, k1, k2, test)
        self.set_attack(af, n, k1, IncAF.DEFINITE_ATTACK)
        self.run_exhaustive_rec(af, n, k1, k2, test)
        self.set_attack(af, n, k1, IncAF.POSSIBLE_ATTACK)
        self.run_exhaustive_rec(af, n, k1, k2, test)

    @staticmethod
    def set_attack(af, n, code, state):
        attacker = code % n
        target = code // n
        af.set_attack(attacker, target, state)

    @staticmethod
    def set_argument(af, n, arg, state):
        af.set_argument(arg, state)
