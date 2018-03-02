import sys
import getopt
import datetime
import threading
from incaffeine.instance_generator import InstanceGenerator


class TestRunner(object):
    """
    config of test runner (leaving out generator parameters)
    - test function (abstract method)
    - reference function (abstract method)
    - runner name (prepended to all progress messages, used in log file name)
    - config progress messages: one message after each X seconds
    - logging of status messages: to stream (stdout or other) and/or to log file
    - logging of result dumps: to stream (stdout or other) and/or to log file
    - when to log result dumps: on failed instances and/or on successful instances
    """

    # Tester functions
    test_instance = None
    reference_test_instance = None

    # config behaviour
    exit_on_failure = False  # Default: don't abort on first failure
    abort_now = False  # set for graceful abortion

    # instance generation configuration
    n_min = 1  # Default: start on instances with n=1
    n_max = 3  # Default: go until instances with n=3
    randomized = False  # Default: exhaustive, don't randomize over instance space
    use_extension = False  # Default: no extension
    use_argument = False  # Default: no single argument
    use_uncertain_args = False  # Default: no argument uncertainty
    use_uncertain_attacks = False  # Default: no attack uncertainty

    # logging configuration
    name = "unnamed"
    """Runner name, used as prefix in log messages and as default log file name"""
    log_stream = sys.stdout  # Default: use stdout as output stream
    log_file = None  # Default: do not log to file
    log_status_to_stream = True  # Default: post status messages to output stream
    log_status_to_file = True  # Default: if log file is specified, post status messages to log file
    log_results_to_stream = False  # Default: do not post result dumps to output stream
    log_results_to_file = True  # Default: if log file is specified, post result dumps to log file
    log_results_on_success = False  # Default: do not log successful instances
    log_results_on_failure = True  # Default: log failed instances
    log_status_interval = 3  # Default: print status log message every 3 seconds

    # progress counters
    current_count = 0
    total_count = 0
    success_count = 0

    def __init__(self, name, test_instance, reference_test_instance):
        self.name = str(name)
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
            print('available options:')
            print('\t--nMin=int\t\tset smallest AF size to be generated')
            print('\t--nMax=int\t\tset largest AF size to be generated')
            print('\t--rand=int\t\tuse random generation with given sample size instead of exhaustive generation')
            print('\t--log=<filename>\twrite log to file with specified name infix')
            sys.exit(0)
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
                prefix = arg if arg else self.name
                log_name = prefix + timestamp + '.log'
                self.log_file = open(log_name, 'w')

    def write_log_status(self, msg):
        status_msg = '[' + self.name + '] ' + str(msg) + '\n'
        if self.log_status_to_stream:
            self.log_stream.write(status_msg)
        if self.log_status_to_file and self.log_file:
            self.log_file.write(status_msg)

    def write_log_results(self, msg):
        if self.log_results_to_stream:
            self.log_stream.write(msg)
        if self.log_results_to_file and self.log_file:
            self.log_file.write(msg)

    def start_log_status_loop(self):
        if not self.abort_now:
            threading.Timer(self.log_status_interval, self.start_log_status_loop).start()
            self.log_status_progress()

    def log_status_progress(self):
        progress = 0
        equivalence = 100
        if self.total_count > 0:
            progress = ((self.current_count * 10000.0) // self.total_count) / 100
            equivalence = ((self.success_count * 10000.0) // self.current_count) / 100.0
        progress = "{:6.2f}".format(progress)
        equivalence = "{:6.2f}".format(equivalence)
        s = "[progress: " + str(progress) + "%] equivalent: " + str(equivalence) + \
            "% (#fails: " + str(self.current_count - self.success_count) + "/" + str(self.current_count) + ")"
        self.write_log_status(s)

    def run(self):
        self.abort_now = False
        self.write_log_status('Script start... ----------------------------------------------')
        self.write_log_status('Testing ' + self.name + '...')

        # Start periodic status messages
        self.start_log_status_loop()

        n = self.n_min
        while not self.abort_now and (n <= self.n_max):
            self.write_log_status('-------------------')
            self.write_log_status('Start testing n=' + str(n))
            generator = InstanceGenerator(n, self.randomized, self.use_extension, self.use_argument,
                                          self.use_uncertain_args, self.use_uncertain_attacks)
            self.total_count += generator.total_count
            self.write_log_status('number of instances: ' + str(generator.total_count))
            self.run_single(generator)
            self.log_status_progress()  # After finishing current n, post additional status message
            n += 1

        # Indicate end of run
        self.write_log_status('...finished --------------------------------------------------')
        self.abort_now = True

    def run_single(self, generator):
        """
        Run tests using the given instance generator.

        :param generator: InstanceGenerator to be used
        :return:
        """
        if self.abort_now:
            return

        for instance in generator.next():
            if not instance:
                return
            result = self.test_instance(self, instance.af, instance.extension, instance.arg)
            reference_result = self.reference_test_instance(self, instance.af, instance.extension, instance.arg)
            equivalent = (result == reference_result)
            self.current_count += 1
            if equivalent:
                # success
                self.success_count += 1
                if self.log_results_on_success:
                    self.log_result(generator, instance, result, reference_result)
            else:
                # failure
                if self.log_results_on_failure:
                    self.log_result(generator, instance, result, reference_result)
                if self.exit_on_failure:
                    self.abort_now = True
                    return

    def log_result(self, generator, instance, result, reference_result):
        if not (self.log_results_to_stream or (self.log_results_to_file and self.log_file)):
            return  # Fail early if no result logging is available

        self.write_log_results('-------------------------------\n')
        self.write_log_results('instance number: ' + str(generator.current_count) + '/'
                               + str(generator.total_count) + '\n')
        self.log_af(instance.af)
        if self.use_extension:
            self.log_extension(instance.extension)
        if self.use_argument:
            self.log_argument(instance.arg)
        self.write_log_results('\theuristic result: ')
        self.write_log_results(str(result))
        self.write_log_results('\n\tbrute force result: ')
        self.write_log_results(str(reference_result))
        self.write_log_results('\n')

    def log_af(self, af):
        self.write_log_results('AF:')
        self.write_log_results('\n\tArguments: ')
        self.write_log_results('\t' + str(af.A))
        self.write_log_results('\n\tAttacks:\n')
        for attacker in range(af.n):
            self.write_log_results('\t' + str(af.R[attacker]))
            self.write_log_results('\n')

    def log_extension(self, extension):
        self.write_log_results('extension: ' + str(extension) + '\n')

    def log_argument(self, arg):
        self.write_log_results('arg: ' + str(arg) + '\n')
