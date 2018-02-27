import sys
import getopt
from test_runner import TestRunner
from instance_generator import InstanceGenerator

print('Script start... ------------------------------------')

print('Testing dummy...')

global equivalent_count


def test_instance(af, args, arg):
    return True


def reference_test_instance(af, args, arg):
    return False


def main(argv):
    global logfile
    n_min = 1
    n_max = 3
    randomized = False
    log_name = 'log/testCF.log'  # TODO
    try:
        opts, args = getopt.getopt(argv, "", ["nMax=", "nMin=", "rand=", "log="])
    except getopt.GetoptError:
        print("invalid option(s)")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--nMax':
            n_max = int(arg)
        elif opt == '--nMin':
            n_min = int(arg)
        elif opt == '--rand':
            randomized = True
        elif opt == '--log':
            log_name = 'log/testCF' + arg + '.log'
    logfile = open(log_name, 'w')

    # Config
    use_extension = False
    use_argument = True
    use_uncertain_args = False
    use_uncertain_attacks = True

    n = n_min
    while n <= n_max:
        print('Start testing n=' + str(n))
        generator = InstanceGenerator(n, randomized, use_extension, use_argument, use_uncertain_args,
                                      use_uncertain_attacks)
        runner = TestRunner(generator, test_instance, reference_test_instance)
        runner.run()
        n += 1


if __name__ == "__main__":
    equivalent_count = 0
    main(sys.argv[1:])

print("...finished ----------------------------------------")
