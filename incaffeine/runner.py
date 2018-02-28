import sys
import getopt
import datetime
from instance_generator import InstanceGenerator


class TestRunner(object):
    """
    config of test runner (leaving out generator parameters)
    - test function (abstract method)
    - reference function (abstract method)
    - config progress messages:
        - one message after each X instances
        - one message after each Y% of all instances
        - one message after each Z seconds
    - Prefix string (prepended to all progress messages)
    - logging stream:
        - None,
        - sys.stdout [default],
        - <any other stream> (including file handle: f = open("log/myfile.log", "w"))
    - which instance info (refer to instance generator) to log for positive/negative instances
        - default: none for positive instances, all for negative instances
    """

    # Tester functions
    test_instance = None
    reference_test_instance = None

    # config behaviour
    exit_on_failure = False  # Default: don't abort on first failure
    abort_now = False  # internal, is set for graceful abortion

    # instance generation configuration
    n_min = 1  # Default: start on instances with n=1
    n_max = 3  # Default: go until instances with n=3
    randomized = False  # Default: exhaustive, don't randomize over instance space
    use_extension = False  # Default: no extension
    use_argument = False  # Default: no single argument
    use_uncertain_args = False  # Default: no argument uncertainty
    use_uncertain_attacks = False  # Default: no attack uncertainty

    # logging configuration
    logger_status = sys.stdout  # Default: log status messages to stdout
    logger_results = None  # Default: do not log results
    logger_status_prefix = ""  # Optional prefix for status log messages
    log_on_success = False  # Default: do not log successful instances
    log_on_failure = True  # Default: log failed instances

    # internals
    success_count = 0
    total_count = 0

    def __init__(self, test_instance, reference_test_instance):
        self.test_instance = test_instance
        self.reference_test_instance = reference_test_instance

    def apply_params(self, argv):
        """
        Configure runner based on given command line parameters.

        :param argv: command line parameters
        :return:
        """
        try:
            opts, args = getopt.getopt(argv, "", ["nMax=", "nMin=", "rand=", "log="])
        except getopt.GetoptError:
            print("invalid option(s)")
            sys.exit(2)  # TODO better error handling!
        for opt, arg in opts:
            if opt == '--nMax':
                self.n_max = int(arg)
            elif opt == '--nMin':
                self.n_min = int(arg)
            elif opt == '--rand':
                self.randomized = True
            elif opt == '--log':
                now = datetime.datetime.now()
                timestamp = now.strftime("-%Y-%m-%d-%H-%M-%S")
                log_name = 'log/' + arg + timestamp + '.log'
                print(log_name)
                self.logger_results = open(log_name, 'w')

    def set_status_logger(self, logger):
        """
        Change the logger to be used by this runner for update messages.

        :param logger: stream or file handle to log to
        :return:
        """
        self.logger_status = logger

    def set_results_logger(self, logger):
        """
        Change the logger to be used by this runner for result output.

        :param logger: stream or file handle to log to
        :return:
        """
        self.logger_results = logger

    def set_logging_prefix(self, logging_prefix):
        self.logger_status_prefix = str(logging_prefix)

    def log_status(self, msg):
        self.logger_status.write(self.logger_status_prefix + str(msg) + '\n')

    def run(self):
        self.abort_now = False
        n = self.n_min
        while n <= self.n_max:
            self.log_status('Start testing n=' + str(n))
            generator = InstanceGenerator(n, self.randomized, self.use_extension, self.use_argument,
                                          self.use_uncertain_args, self.use_uncertain_attacks)
            self.log_status('\tnumber of instances: ' + str(generator.total_count))
            self.run_single(generator)
            if self.abort_now:
                return
            n += 1

    def run_single(self, generator):
        """
        Run tests using the given instance generator.

        :param generator: InstanceGenerator to be used
        :return:
        """
        for instance in generator.next():
            if not instance:
                return
            result = self.test_instance(self, instance.af, instance.extension, instance.arg)
            reference_result = self.reference_test_instance(self, instance.af, instance.extension, instance.arg)
            equivalent = (result == reference_result)
            self.total_count += 1
            if equivalent:
                # success
                self.success_count += 1
                if self.log_on_success:
                    self.log_result(generator, instance, result, reference_result)
            else:
                # failure
                if self.log_on_failure:
                    self.log_result(generator, instance, result, reference_result)
                if self.exit_on_failure:
                    self.abort_now = True
                    return

    def log_result(self, generator, instance, result, reference_result):
        if self.logger_results:
            self.logger_results.write('-------------------------------\n')
            self.logger_results.write('instance number: ' + str(generator.current_count) + '/'
                                      + str(generator.total_count) + '\n')
            self.log_af(instance.af)
            if self.use_extension:
                self.log_extension(instance.extension)
            if self.use_argument:
                self.log_argument(instance.arg)
            self.logger_results.write('\theuristic result: ')
            self.logger_results.write(str(result))
            self.logger_results.write('\n\tbrute force result: ')
            self.logger_results.write(str(reference_result))
            self.logger_results.write('\n')

    def log_af(self, af):
        self.logger_results.write('AF:')
        self.logger_results.write('\n\tArguments: ')
        self.logger_results.write('\t' + str(af.A))
        self.logger_results.write('\n\tAttacks:\n')
        for attacker in range(af.n):
            self.logger_results.write('\t' + str(af.R[attacker]))
            self.logger_results.write('\n')

    def log_extension(self, extension):
        self.logger_results.write('extension: ' + str(extension) + '\n')

    def log_argument(self, arg):
        self.logger_results.write('arg: ' + str(arg) + '\n')
