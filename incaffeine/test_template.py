import sys
from runner import TestRunner

print('Script start... ------------------------------------')
print('Testing dummy...')


def test_instance(af, args, arg):
    # TODO implement instance test here!
    return True


def reference_test_instance(af, args, arg):
    # TODO call reference instance test here!
    return False


def main(argv):
    runner = TestRunner(test_instance, reference_test_instance)

    # Config
    runner.apply_params(argv)
    runner.use_extension = False
    runner.use_argument = False
    runner.use_uncertain_args = False
    runner.use_uncertain_attacks = True

    # Run!
    runner.run()


if __name__ == "__main__":
    main(sys.argv[1:])

print("...finished ----------------------------------------")
