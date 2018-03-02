from random import randrange
from incaffeine.incaf import IncAF


class InstanceGenerator:
    """
    Generate instances based on seeds!
      - for each instance feature (see below), seed space is a contiguous sequence [0 2 ... k-1], k = feature space size
        - code of argument states: [0 ... (2^n - 1)]
        - code of attack states: [0 ... (3^(n^2) - 1)]
        - code argument set ("extension"): [0 ... n]
        - code of distinguished arg: [0 ... (n-1)]
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

    current_count = 0
    total_count = 0

    randomize = False  # Default: Exhaustive generation, do not randomize
    randomize_sample_size = 1000  # Default: If randomizing, generate 1000 samples

    use_extension = False  # Default: Do not generate an extension
    use_argument = False  # Default: Do not generate a single argument
    use_uncertain_args = False  # Default: Generate AFs without uncertain arguments
    use_uncertain_attacks = False  # Default: Generate AFs without uncertain attacks

    n = None
    af = None
    extension = None
    arg = None

    def __init__(self, n, randomize, use_extension, use_argument, use_uncertain_args, use_uncertain_attacks):
        self.n = n
        self.af = IncAF(n)
        self.randomize = randomize
        self.use_extension = True if use_extension else False
        self.use_argument = True if use_argument else False
        self.use_uncertain_args = True if use_uncertain_args else False
        self.use_uncertain_attacks = True if use_uncertain_attacks else False

        # Determine state space depending on configuration
        self.number_of_extensions = (n + 1) if use_extension else 1
        self.number_of_single_args = n if use_argument else 1
        self.number_of_arguments = n
        self.number_of_argument_states = 2 if use_uncertain_args else 1
        self.number_of_attacks = (n ** 2)
        self.number_of_attack_states = 3 if use_uncertain_attacks else 2
        self.total_count = (self.get_argument_state_space_size() *
                            self.get_attack_state_space_size() *
                            self.get_extension_state_space_size() *
                            self.get_single_arg_state_space_size())
        self.current_count = 0

    def get_argument_state_space_size(self):
        """
        Returns the size of the possibility space for argument states (definite, possible) for this generator.

        :return: number of possible argument states
        """
        return self.number_of_argument_states ** self.number_of_arguments

    def get_attack_state_space_size(self):
        """
        Returns the size of the possibility space for attack states (definite, no, possible) for this generator.

        :return: number of possible attack states
        """
        return self.number_of_attack_states ** self.number_of_attacks

    def get_extension_state_space_size(self):
        """
        Returns the size of the possibility space for extensions (subsets of arguments) for this generator.

        :return: number of possible argument states
        """
        return self.number_of_extensions

    def get_single_arg_state_space_size(self):
        """
        Returns the size of the possibility space for single args for this generator.

        :return: number of possible single arguments
        """
        return self.number_of_single_args

    def next(self):
        for args_state in range(0, self.get_argument_state_space_size()):
            for attacks_state in range(0, self.get_attack_state_space_size()):
                for extension_code in range(0, self.get_extension_state_space_size()):
                    for arg_code in range(0, self.get_single_arg_state_space_size()):
                        self.generate(args_state=args_state,
                                      attacks_state=attacks_state,
                                      extension=extension_code,
                                      argument=arg_code)
                        self.current_count += 1
                        yield self
                        # print('DEBUG: args_state=' + str(args_state) + ' attacks_state=' + str(attacks_state) +
                        #       ' extension=' + str(extension_code) + ' argument=' + str(arg_code))

    def next_randomized(self):
        while self.current_count < self.randomize_sample_size:  # TODO
            args_state = randrange(0, self.get_argument_state_space_size())
            attacks_state = randrange(0, self.get_attack_state_space_size())
            extension_code = randrange(0, self.get_extension_state_space_size())
            arg_code = randrange(0, self.get_single_arg_state_space_size())
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
        base = self.number_of_argument_states  # number of possible values for argument statuses
        for arg in range(self.n):
            self.af.set_argument(arg, IncAF.DEFINITE_ARGUMENT)
            if self.use_uncertain_args:
                state = (args_state_code // (base ** arg)) % base
                if state == 1:
                    self.af.set_argument(arg, IncAF.POSSIBLE_ARGUMENT)

        # attack state
        base = self.number_of_attack_states  # number of possible values for attack statuses
        for attacker in range(self.n):
            for target in range(self.n):
                state = (attacks_state_code // (base ** ((self.n * attacker) + target))) % base
                if state == 0:
                    self.af.set_attack(attacker, target, IncAF.NO_ATTACK)
                elif state == 1:
                    self.af.set_attack(attacker, target, IncAF.DEFINITE_ATTACK)
                elif state == 2:
                    self.af.set_attack(attacker, target, IncAF.POSSIBLE_ATTACK)

        # extension
        if self.use_extension:
            # Does NOT generate all possible subsets of args, assumes that symmetry from AF generation can be exploited
            self.extension = set([i for i in range(extension_code)])

        # argument
        self.arg = argument_code
