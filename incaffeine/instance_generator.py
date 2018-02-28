import math
from random import randrange

from incaf import IncAF
"""
Generate instances based on seeds!
  - for each instance feature (see below), seed space is a contiguous sequence [1 2 ... k], k = size of feature space
    - code of number n of args: [1 ... inf]
    - code of argument states: [1 ... 2^n]
    - code of attack states: [1 ... 3^(n^2)]
    - code argument set ("extension"): [0 ... n]
    - code of distinguished arg: [1 ... n]
  - generator yields concrete instances
    - internal function generates instance for a given seed
      - keeps one single mutable instance(?)
      - maybe use different generator implementations for exhaustive and specific generation?
  - randomization of instances can be done by pure numeric randomization of seed space

config of instance generator:
- number arguments (fixed!)
- number arguments
- include uncertain args?
  - randomize uncertain args?
- include incomplete attacks?
- include a set of args? (ranges from [1] to [1 ... n])
- include a single arg? (ranges from 1 to n)
"""


class InstanceGenerator:
    current_count = 0
    total_count = 0

    n = None
    af = None
    extension = None
    arg = None

    def __init__(self, n, randomize, use_extension, use_argument, use_uncertain_args, use_uncertain_attacks):
        self.n = n
        self.af = IncAF(n)
        self.randomize = randomize   # TODO
        self.use_extension = True if use_extension else False
        self.use_argument = True if use_argument else False
        self.use_uncertain_args = True if use_uncertain_args else False
        self.use_uncertain_attacks = True if use_uncertain_attacks else False

        self.number_of_extensions = (n + 1) if use_extension else 1
        self.number_of_single_args = n if use_argument else 1
        self.number_of_arguments = n
        self.number_of_argument_states = 2 if use_uncertain_args else 1
        self.number_of_attacks = (n ** 2)
        self.number_of_attack_states = 3 if use_uncertain_attacks else 2
        self.total_count += (self.number_of_extensions * self.number_of_single_args *
                             self.number_of_argument_states ** self.number_of_arguments *
                             self.number_of_attack_states ** self.number_of_attacks)
        self.current_count = 0

    def next(self):
        for args_state in range(0, self.number_of_argument_states ** self.number_of_arguments):
            for attacks_state in range(0, self.number_of_attack_states ** self.number_of_attacks):
                for extension_code in range(0, self.number_of_extensions):
                    for arg_code in range(0, self.number_of_single_args):
                        self.generate(args_state=args_state,
                                      attacks_state=attacks_state,
                                      extension=extension_code,
                                      argument=arg_code)
                        self.current_count += 1
                        yield self
                        print('DEBUG: args_state=' + str(args_state) + ' attacks_state=' + str(attacks_state) +
                              ' extension=' + str(extension_code) + ' argument=' + str(arg_code))

    def next_randomized(self):
        while True:  # TODO
            args_state = randrange(0, self.number_of_argument_states ** self.number_of_arguments)
            attacks_state = randrange(0, self.number_of_attack_states ** self.number_of_attacks)
            extension_code = randrange(0, self.number_of_extensions)
            arg_code = randrange(0, self.number_of_single_args)
            self.generate(args_state=args_state,
                          attacks_state=attacks_state,
                          extension=extension_code,
                          argument=arg_code)
            self.current_count += 1
            yield self

    def generate(self, **seed):
        """
        code of argument states: [0 ... (2^n - 1)]
        code of attack states: [0 ... (3^(n^2) - 1)]
        code argument set ("extension"): [0 ... n]
        code of distinguished arg: [0 ... (n-1)]

        :param seed: instance parameter seed
        :return: af representing the seed
        """
        args_state_code = seed['args_state']
        attacks_state_code = seed['attacks_state']
        extension_code = seed['extension']
        argument_code = seed['argument']

        # arg state
        # 0: all definite
        # 1: 1 possible, others definite
        # 2: 2 possible, others definite
        # 3: 1,2 possible, others definite
        # ...
        # 2^n - 1: all possible
        for arg in range(self.n):
            self.af.set_argument(arg, IncAF.DEFINITE_ARGUMENT)
            if self.use_uncertain_args:
                state = args_state_code % (2 ** (arg + 1))
                if state == 1:
                    self.af.set_argument(arg, IncAF.POSSIBLE_ARGUMENT)

        # attack state
        # 0: all attacks missing
        base = 3 if self.use_uncertain_attacks else 2
        for attacker in range(self.n):
            for target in range(self.n):
                # state = attacks_state_code % math.pow(base, (self.n * attacker) + target + 1)
                state = (attacks_state_code // math.pow(base, (self.n * attacker) + target)) % base
                if state == 0:
                    self.af.set_attack(attacker, target, IncAF.NO_ATTACK)
                elif state == 1:
                    self.af.set_attack(attacker, target, IncAF.DEFINITE_ATTACK)
                elif state == 2:
                    self.af.set_attack(attacker, target, IncAF.POSSIBLE_ATTACK)

        # extension
        if self.use_extension:
            # TODO does NOT generate all possible sets, assumes that symmetry from AF generation can be exploited
            self.extension = set([i + 1 for i in range(extension_code)])

        # argument
        self.arg = argument_code
