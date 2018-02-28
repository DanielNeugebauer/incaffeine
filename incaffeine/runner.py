import sys


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

    generator = None
    test_instance = None
    reference_test_instance = None

    logger = sys.stdout
    logging_prefix = ""

    def __init__(self, generator, test_instance, reference_test_instance):
        self.generator = generator
        self.test_instance = test_instance
        self.reference_test_instance = reference_test_instance

    def set_logger(self, logger):
        self.logger = logger

    def set_logging_prefix(self, logging_prefix):
        self.logging_prefix = logging_prefix

    def run(self):
        for instance in self.generator.next():
            if not instance:
                return
            result = self.test_instance(instance.af, instance.extension, instance.arg)
            reference_result = self.reference_test_instance(instance.af, instance.extension, instance.arg)
            equivalent = (result == reference_result)
            if equivalent:
                # success
                pass
            else:
                # failure
                self.logger.write('-------------------------------\n')
                self.logger.write('instance number: ' + str(self.generator.current_count) + '/'
                                  + str(self.generator.total_count) + '\n')
                self.logger.write('AF:')
                self.logger.write('\n\tArguments: ')
                self.logger.write('\t' + str(instance.af.A))
                self.logger.write('\n\tAttacks:\n')
                for attacker in range(instance.af.n):
                    self.logger.write('\t' + str(instance.af.R[attacker]))
                    self.logger.write('\n')
                if self.generator.use_extension:
                    self.logger.write('extension: ' + str(instance.extension) + '\n')
                if self.generator.use_argument:
                    self.logger.write('arg: ' + str(instance.arg) + '\n')
                # self.logger.write('\theuristic result: ')
                # self.logger.write(str(result))
                # self.logger.write('\n\tbrute force result: ')
                # self.logger.write(str(reference_result))
                # self.logger.write('\n')
